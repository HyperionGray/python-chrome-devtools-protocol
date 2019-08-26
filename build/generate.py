from dataclasses import dataclass
from enum import Enum
import json
import logging
import operator
import os
from pathlib import Path
import typing

import inflection


log_level = getattr(logging, os.environ.get('LOG_LEVEL', 'info').upper())
logging.basicConfig(level=log_level)
logger = logging.getLogger('generate')

shared_header = '''DO NOT EDIT THIS FILE

This file is generated from the CDP definitions. If you need to make changes,
edit the generator and regenerate all of the modules.'''

init_header = '''\'\'\'
{}
\'\'\'

'''.format(shared_header)

module_header = '''\'\'\'
{}

Domain: {{}}
Experimental: {{}}
\'\'\'

from cdp.util import T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

'''.format(shared_header)


def clear_dirs(package_path):
    ''' Remove generated code. '''
    def rmdir(path):
        for subpath in path.iterdir():
            if subpath.is_file():
                subpath.unlink()
            elif subpath.is_dir():
                rmdir(subpath)
        path.rmdir()

    try:
        (package_path / '__init__.py').unlink()
    except FileNotFoundError:
        pass

    for subpath in package_path.iterdir():
        if subpath.is_dir():
            rmdir(subpath)


class CdpPrimitiveType(Enum):
    ''' All of the CDP types that map directly to Python types. '''
    any: typing.Any
    boolean = bool
    integer = int
    number = float
    object = dict
    string = str


@dataclass
class CdpProperty:
    ''' A property belonging to a non-primitive CDP type. '''
    name: str
    description: str
    type: str
    ref: str
    enum: typing.List[str]
    optional: bool

    @classmethod
    def from_json(cls, property):
        return cls(
            property['name'],
            property.get('description'),
            property.get('type'),
            property.get('$ref'),
            property.get('enum'),
            property.get('optional', False),
        )


@dataclass
class CdpType:
    ''' A top-level CDP type. '''
    id: str
    description: str
    type: str
    enum: typing.List[str]
    properties: typing.List[CdpProperty]

    @classmethod
    def from_json(cls, type):
        return cls(
            type['id'],
            type.get('description'),
            type['type'],
            type.get('enum'),
            type.get('properties'),
        )


class CdpParameter(CdpProperty):
    '''
    A parameter to a CDP command.

    This is an empty subclass of CdpProperty because they seem to share the same
    behavior, but I want to allow the flexibility to change the behavior later
    on.
    '''


class CdpReturn(CdpProperty):
    '''
    A return value from a CDP command.

    This is an empty subclass of CdpProperty because they seem to share the same
    behavior, but I want to allow the flexibility to change the behavior later
    on.
    '''


@dataclass
class CdpCommand:
    ''' A CDP command. '''
    name: str
    description: str
    experimental: bool
    parameters: typing.List[CdpParameter]
    returns: typing.List[CdpReturn]

    @classmethod
    def from_json(cls, command):
        parameters = command.get('parameters', list())
        returns = command.get('returns', list())

        return cls(
            command['name'],
            command.get('description'),
            command.get('experimental', False),
            [CdpParameter.from_json(p) for p in parameters],
            [CdpReturn.from_json(r) for r in returns],
        )

@dataclass
class CdpEvent:
    ''' A CDP event object. '''
    name: str
    description: str
    parameters: typing.List[CdpParameter]


@dataclass
class CdpDomain:
    ''' A CDP domain contains metadata, types, commands, and events. '''
    domain: str
    experimental: bool
    dependencies: typing.List[str]
    types: typing.List[CdpType]
    commands: typing.List[CdpCommand]
    events: typing.List[CdpEvent]

    @classmethod
    def from_json(cls, domain):
        types = domain.get('types', list())
        commands = domain.get('commands', list())
        events = domain.get('events', list())

        return cls(
            domain['domain'],
            domain.get('experimental', False),
            domain.get('dependencies', list()),
            [CdpType.from_json(type) for type in types],
            [CdpCommand.from_json(command) for command in commands],
            list(),
        )


def parse(json_path, output_path):
    '''
    Parse JSON protocol description and generate module files.

    :param Path json_path: path to a JSON CDP schema
    :param Path output_path: a directory path to create the modules in
    :returns: a list of 2-tuples containing (module name, list of exported
        symbols)
    '''
    with json_path.open() as json_file:
        schema = json.load(json_file)
    version = schema['version']
    assert (version['major'], version['minor']) == ('1', '3')
    modules = list()
    domains = list()
    for domain in schema['domains']:
        domains.append(CdpDomain.from_json(domain))
        modules.append(
            generate_domain_module(domain, output_path))
    return modules


def generate_domain_module(domain, output_path):
    '''
    Generate a Python module for a given CDP domain.

    :param dict domain: domain schema
    :param Path output_path: a directory path to create the module in
    :returns: module name and a list of exported names
    '''
    name = domain['domain']
    module_name = inflection.underscore(name)
    logger.info('Generating module: %s → %s.py', name, module_name)
    experimental = domain.get('experimental', False)

    # The dependencies listed in the JSON don't match the actual dependencies
    # encountered when building the types. So we ignore the declared
    # dependencies and compute it ourself.
    type_dependencies = set()
    domain_types = domain.get('types', list())
    for type_ in domain_types:
        for prop in type_.get('properties', list()):
            dependency = get_dependency(prop)
            if dependency:
                type_dependencies.add(dependency)
    if type_dependencies:
        logger.debug('Computed type_dependencies: %s', ','.join(
            type_dependencies))

    event_dependencies = set()
    domain_events = domain.get('events', list())
    for event in domain_events:
        for param in event.get('parameters', list()):
            dependency = get_dependency(param)
            if dependency:
                event_dependencies.add(dependency)
    if event_dependencies:
        logger.debug('Computed event_dependencies: %s', ','.join(
            event_dependencies))

    command_dependencies = set()
    domain_commands = domain.get('commands', list())
    for command in domain_commands:
        for param in command.get('parameters', list()):
            dependency = get_dependency(param)
            if dependency:
                command_dependencies.add(dependency)
        for return_ in command.get('returns', list()):
            dependency = get_dependency(return_)
            if dependency:
                command_dependencies.add(dependency)
    if command_dependencies:
        logger.debug('Computed command_dependencies: %s', ','.join(
            command_dependencies))

    # Generate code for this module.
    module_path = output_path / module_name
    module_path.mkdir(parents=True, exist_ok=True)
    init_path = module_path / '__init__.py'
    with init_path.open('w'):
        # Zero out this file
        pass

    types_path = module_path / 'types.py'
    with types_path.open('w') as types_file:
        types_file.write(module_header.format(module_name, experimental))
        for dependency in sorted(type_dependencies):
            types_file.write(import_dependency(dependency))
        if type_dependencies:
            types_file.write('\n')
        type_exports, type_code = generate_types(domain_types)
        types_file.write(type_code)

    events_path = module_path / 'events.py'
    with events_path.open('w') as events_file:
        events_file.write(module_header.format(module_name, experimental))
        events_file.write('from .types import *\n')
        for dependency in sorted(event_dependencies):
            events_file.write(import_dependency(dependency))
        if event_dependencies:
            events_file.write('\n')
        event_exports, event_code = generate_events(name, domain_events)
        events_file.write(event_code)

    commands_path = module_path / 'commands.py'
    with commands_path.open('w') as commands_file:
        commands_file.write(module_header.format(module_name, experimental))
        commands_file.write('from .types import *\n')
        for dependency in sorted(command_dependencies):
            commands_file.write(import_dependency(dependency))
        if command_dependencies:
            commands_file.write('\n')
        command_exports, command_code = generate_commands(name, domain_commands)
        commands_file.write(command_code)

    return module_name, type_exports, event_exports, command_exports


def get_dependency(cdp_meta):
    if 'type' in cdp_meta and cdp_meta['type'] != 'array':
        return None

    if 'items' in cdp_meta and 'type' in cdp_meta['items']:
        return None

    if '$ref' in cdp_meta:
        type_ = cdp_meta['$ref']
    elif 'items' in cdp_meta and '$ref' in cdp_meta['items']:
        type_ = cdp_meta['items']['$ref']
    else:
        raise Exception('Cannot get dependency: {!r}'.format(cdp_meta))

    try:
        dependency, _ = type_.split('.')
        return dependency
    except ValueError:
        # Not a dependency on another module.
        return None


def import_dependency(dependency):
    module_name = inflection.underscore(dependency)
    return 'from ..{} import types as {}\n'.format(module_name, module_name)


def generate_types(types):
    '''
    Generate type definitions as Python code.

    :param list types: a list of CDP type definitions
    :returns: a tuple (list of types, code as string)
    '''
    code = '\n'
    exports = list()
    classes = list()
    emitted_types = set()
    for type_ in types:
        cdp_type = type_['type']
        type_name = type_['id']
        exports.append(type_name)
        description = type_.get('description')
        logger.debug('Generating type %s: %s', type_name, cdp_type)
        if 'enum' in type_:
            code += generate_enum_type(type_)
            emitted_types.add(type_name)
        elif cdp_type == 'object':
            classes.append(generate_class_type(type_))
        else:
            code += generate_basic_type(type_)
            emitted_types.add(type_name)

    # The classes have dependencies on each other, so we have to emit them in
    # a specific order. If we can't resolve these dependencies after a certain
    # number of iterations, it suggests a cyclical dependency that this code
    # cannot handle.
    tries_remaining = 1000
    while classes:
        class_ = classes.pop(0)
        if not class_['children']:
            code += class_['code']
            emitted_types.add(class_['name'])
            continue
        if all(child in emitted_types for child in class_['children']):
            code += class_['code']
            emitted_types.add(class_['name'])
            continue
        classes.append(class_)
        tries_remaining -= 1
        if not tries_remaining:
            logger.error('Class resolution failed. Emitted these types: %s',
                emitted_types)
            logger.error('Class resolution failed. Cannot emit these types: %s',
                json.dumps(classes, indent=2))
            raise Exception('Failed to resolve class dependencies.'
                ' See output above.')

    return exports, code


def inline_doc(description, indent=0):
    '''
    Generate an inline doc, e.g. ``#: This type is a ...``

    :param str description:
    :returns: a string
    '''
    if not description:
        return ''

    i = ' ' * indent
    lines = ['{}#: {}\n'.format(i, l) for l in description.split('\n')]
    return ''.join(lines)


def docstring(description, indent=4):
    '''
    Generate a docstring from a description.

    :param str description:
    :param int indent: the number of spaces to indent the docstring
    '''
    if not description:
        return ''

    i = ' ' * indent
    start_stop = "{}'''".format(i)
    lines = [start_stop]
    for line in description.split('\n'):
        lines.append('{}{}'.format(i, line))
    lines.append(start_stop)
    return '\n'.join(lines) + '\n'


def generate_enum_type(type_):
    '''
    Generate an "enum" type.

    Enums are handled by making a python class that contains only class members.
    Each class member is upper snaked case, e.g. ``MyTypeClass.MY_ENUM_VALUE``
    and is assigned a string value from the CDP metadata.

    :param dict type_: CDP type metadata
    '''
    code = ''
    if type_['type'] != 'string':
        raise Exception('Unexpected enum type: {!r}'.format(type_))
    code += 'class {}(enum.Enum):\n'.format(type_['id'])
    description = type_.get('description')
    code += docstring(description)
    for enum_member in type_['enum']:
        snake_case = inflection.underscore(enum_member).upper()
        code += '    {} = "{}"\n'.format(snake_case, enum_member)
    code += '\n'
    code += '    def to_json(self) -> str:\n'
    code += '        return self.value\n'
    code += '\n'
    code += '    @classmethod\n'
    code += "    def from_json(cls, json: str) -> '{}':\n".format(type_['id'])
    code += '        return cls(json)\n'
    code += '\n\n'
    return code


def get_python_type(cdp_meta):
    '''
    Generate a name for the Python type that corresponds to the the given CDP
    type.

    :param dict cdp_meta: CDP metadata for a type or property
    :returns: Python type as a string
    '''
    if 'type' in cdp_meta:
        cdp_type = cdp_meta['type']
        if cdp_type == 'array':
            py_type = 'typing.List'
            try:
                cdp_nested_type = get_python_type(cdp_meta['items'])
                if '.' in cdp_nested_type:
                    domain, subtype = cdp_nested_type.split('.')
                    cdp_nested_type = '{}.{}'.format(
                        inflection.underscore(domain), subtype)
                py_type += "['{}']".format(cdp_nested_type)
            except KeyError:
                # No nested type: ignore.
                pass
        else:
            py_type = {
                'any': 'typing.Any',
                'boolean': 'bool',
                'integer': 'int',
                'object': 'dict',
                'number': 'float',
                'string': 'str',
            }[cdp_type]
        return py_type

    if '$ref' in cdp_meta:
        prop_type = cdp_meta['$ref']
        if '.' in prop_type:
            # If the type lives in another module, then we need to
            # snake_case the module name and it should *not* be added to the
            # list of child classes that is used for dependency resolution.
            other_module, other_type = prop_type.split('.')
            prop_type = '{}.{}'.format(inflection.underscore(other_module),
                other_type)
        return prop_type

    raise Exception('Cannot get python type from CDP metadata: {!r}'.format(
        cdp_meta))


def is_builtin_type(python_type):
    return python_type in ('bool', 'int', 'dict', 'float', 'str')


def generate_class_type(type_):
    '''
    Generate a class type.

    Top-level types that are defined as a CDP ``object`` are turned into Python
    dataclasses.

    :param dict type_: CDP type metadata
    '''
    description = type_.get('description')
    type_name = type_['id']
    children = set()
    class_code = '@dataclass\n'
    class_code += 'class {}:\n'.format(type_name)
    class_code += docstring(description)
    from_json = list()
    properties = list()
    to_json = list()
    for prop in type_.get('properties', []):
        prop_name = prop['name']
        optional = prop.get('optional', False)
        snake_name = inflection.underscore(prop_name)
        prop_code = ''
        prop_description = prop.get('description')
        if prop_description:
            prop_code += inline_doc(prop_description, indent=4)
        prop_type = get_python_type(prop)
        prop_decl = prop_type
        if prop_type == type_name:
            # If a type refers to itself, e.g. StackTrace has a member
            # called ``parent`` that is itself a StackTrace, then the type
            # name must be quoted or else Python will not be able to compile
            # the module.
            prop_decl = "'{}'".format(prop_decl)
        elif '$ref' in prop and '.' not in prop_type:
            # If the type lives in this module and is not a type that refers
            # to itself, then add it to the set of children so that
            # inter-class dependencies can be resolved later on.
            children.add(prop_type)
        if optional:
            prop_decl = 'typing.Optional[{}] = None'.format(prop_decl)
        prop_code += '    {}: {}\n\n'.format(snake_name, prop_decl)
        properties.append((prop_code, optional))
        getter = "json['{}']".format(prop_name)
        if 'type' in prop:
            if prop['type'] != 'array':
                from_json.append((snake_name, "{}".format(getter), prop_name,
                    optional))
                to_json.append((snake_name, prop_name, optional,
                    'self.{}'.format(snake_name)))
            elif '$ref' in prop['items']:
                subtype = get_python_type(prop['items'])
                from_json.append((snake_name, "[{}.from_json(i) for i in {}]".format(
                    subtype, getter), prop_name, optional))
                to_json.append((snake_name, prop_name, optional,
                    '[i.to_json() for i in self.{}]'.format(snake_name)))
            elif 'type' in prop['items']:
                subtype = get_python_type(prop['items'])
                from_json.append((snake_name, "[i for i in {}]".format(getter),
                    prop_name, optional))
                to_json.append((snake_name, prop_name, optional,
                    '[i for i in self.{}]'.format(snake_name)))
        else:
            from_json.append((snake_name, "{}.from_json({})".format(
                prop_type, getter), prop_name, optional))
            to_json.append((snake_name, prop_name, optional,
                'self.{}.to_json()'.format(snake_name)))
    # Sort properties so that optional properties come after required
    # properties, otherwise the dataclass will raise an error.
    properties.sort(key=operator.itemgetter(1))
    for prop_code, _ in properties:
        class_code += prop_code
    class_code += '    def to_json(self) -> T_JSON_DICT:\n'
    class_code += '        json: T_JSON_DICT = {\n'
    for snake_name, prop_name, optional, code in to_json:
        if optional:
            continue
        class_code += "            '{}': {},\n".format(prop_name, code)
    class_code += '        }\n'
    for snake_name, prop_name, optional, code in to_json:
        if not optional:
            continue
        class_code += "        if self.{} is not None:\n".format(snake_name)
        class_code += "            json['{}'] = {}\n".format(prop_name, code)
    class_code += '        return json\n'
    class_code += '\n'
    class_code += '    @classmethod\n'
    class_code += "    def from_json(cls, json: T_JSON_DICT) -> '{}':\n".format(type_name)
    for snake_name, code, prop_name, optional in from_json:
        if not optional:
            continue
        class_code += "        {} = {} if '{}' in json else None\n".format(
            snake_name, code, prop_name)
    class_code += '        return cls(\n'
    for snake_name, code, prop_name, optional in from_json:
        if optional:
            class_code += "            {}={},\n".format(snake_name, snake_name)
        else:
            class_code += "            {}={},\n".format(snake_name, code)
    class_code += '        )\n'
    class_code += '\n'

    return {
        'name': type_name,
        'code': class_code,
        # Don't emit children that live in a different module. We assume that
        # modules do not have cyclical dependencies on each other.
        'children': [c for c in children if '.' not in c],
    }


def generate_basic_type(type_):
    '''
    Generate one of the "basic" types, i.e. type aliases for Python built-ins.

    :param dict type_: CDP type metadata
    '''
    code = ''
    cdp_type = type_['id']
    py_type = get_python_type(type_)
    description = type_.get('description')
    code += 'class {}({}):\n'.format(cdp_type, py_type)
    code += docstring(description)
    code += '    def to_json(self) -> {}:\n'.format(py_type)
    code += '        return self\n'
    code += '\n'
    code += '    @classmethod\n'
    code += "    def from_json(cls, json: {}) -> '{}':\n".format(
        py_type, cdp_type)
    code += '        return cls(json)\n'
    code += '\n'
    code += '    def __repr__(self):\n'
    code += "        return '{}({{}})'.format(super().__repr__())\n".format(
        cdp_type, py_type)
    code += '\n\n'
    return code


def generate_events(domain, events):
    exports = list()
    code = '\n'
    for event in events:
        event_name = inflection.camelize(event['name'],
            uppercase_first_letter=True)
        parameters = event.get('parameters', list())
        code += '\n@dataclass\n'
        code += 'class {}:\n'.format(event_name)
        description = event.get('description')
        code += docstring(description)
        from_json = list()
        for parameter in parameters:
            name = parameter['name']
            snake_name = inflection.underscore(name)
            param_description = parameter.get('description')
            code += inline_doc(description, indent=4)
            if 'type' in parameter:
                param_decl = get_python_type(parameter)
            elif '$ref' in parameter:
                param_decl = parameter['$ref']
                if '.' in param_decl:
                    # If the type lives in another module, then we need to
                    # snake_case the module name and it should *not* be
                    # added to the list of child classes that is used for
                    # dependency resolution.
                    other_module, other_type = param_decl.split('.')
                    param_decl = '{}.{}'.format(
                        inflection.underscore(other_module), other_type)
            else:
                raise Exception('Cannot determing event parameter type:'
                    ' {!r}'.format(parameter))
            optional = parameter.get('optional', False)
            if optional:
                param_decl = 'typing.Optional[{}] = None'.format(param_decl)
            code += '    {}: {}\n\n'.format(snake_name, param_decl)
            from_json.append((name, snake_name, optional, make_return_code(parameter)))
        code += '    # These fields are used for internal purposes and are not part of CDP\n'
        code += "    _domain = '{}'\n".format(domain)
        code += "    _method = '{}'\n".format(event['name'])
        code += '\n'
        code += '    @classmethod\n'
        code += "    def from_json(cls, json: dict) -> '{}':\n".format(event_name)
        for name, snake_name, optional, snippet in from_json:
            if not optional:
                continue
            code += "        {} = {} if '{}' in json else None\n".format(
                snake_name, snippet, name)
        code += '        return cls(\n'
        for name, snake_name, optional, snippet in from_json:
            if optional:
                code += '            {}={},\n'.format(snake_name, snake_name)
            else:
                code += '            {}={},\n'.format(snake_name, snippet)
        code += '        )\n\n'
        exports.append(event_name)
    return exports, code


def generate_commands(domain_name, commands):
    '''
    Generate command definitions as Python code.

    :param str domain_name: the CDP domain name
    :param list commands: a list of CDP command definitions
    :returns: a tuple (list of exported types, code as string)
    '''
    code = '\n\n'
    for command in commands:
        command_name = command['name']
        method_name = inflection.underscore(command_name)
        description = command.get('description', '')
        arg_list = list()
        to_json = list()
        params = command.get('parameters', list())
        if params:
            description += '\n'
        for param in params:
            param_name = param['name']
            snake_name = inflection.underscore(param_name)
            param_type = get_python_type(param)
            param_decl = param_type
            if param.get('optional', False):
                param_decl = 'typing.Optional[{}] = None'.format(param_decl)
            arg_list.append('{}: {}'.format(snake_name, param_decl))
            description += '\n:param {}: {}'.format(snake_name,
                param.get('description', ''))
            if 'type' in param:
                if param['type'] != 'array':
                    json_code = '{}'.format(snake_name)
                elif '$ref' in param['items']:
                    subtype = get_python_type(param['items'])
                    json_code = '[i.to_json() for i in {}]'.format(snake_name)
                elif 'type' in param['items']:
                    subtype = get_python_type(param['items'])
                    json_code = '[i for i in {}]'.format(snake_name)
            else:
                json_code = '{}.to_json()'.format(snake_name)
            # convert = '' if is_builtin_type(param_type) else '.to_json()'
            to_json.append((param_name, snake_name, json_code,
                param.get('optional', False)))
        returns = command.get('returns', list())
        if len(returns) == 0:
            return_type = 'None'
        elif len(returns) == 1:
            return_type = get_python_type(returns[0])
            description += '\n:returns: {}'.format(
                returns[0].get('description', ''))
        else:
            return_type = 'dict'
            description += '\n:returns: a dict with the following keys:'
            for return_ in returns:
                optstr = '(Optional) ' if return_.get('optional', False) else ''
                description += '\n    * {}: {}{}'.format(return_['name'],
                    optstr, return_.get('description', ''))
        code += 'def {}('.format(method_name)
        if arg_list:
            code += '\n'
            for arg in arg_list:
                code += '        {},\n'.format(arg)
            code += '    '
        code += ') -> typing.Generator[T_JSON_DICT,T_JSON_DICT,{}]:\n'.format(return_type)
        code += docstring(description, indent=4)
        if to_json:
            code += '    params: T_JSON_DICT = {\n'
            for param_name, snake_name, json_code, optional in to_json:
                if optional:
                    continue
                code += "        '{}': {},\n".format(param_name, json_code)
            code += '    }\n'
            for param_name, snake_name, json_code, optional in to_json:
                if not optional:
                    continue
                code += '    if {} is not None:\n'.format(snake_name)
                code += "        params['{}'] = {}\n".format(param_name,
                    json_code)
        code += '    cmd_dict: T_JSON_DICT = {\n'
        code += "        'method': '{}.{}',\n".format(domain_name,
            command_name)
        if to_json:
            code += "        'params': params,\n"
        code += '    }\n'
        code += '    json = yield cmd_dict\n'
        if len(returns) == 1:
            return_ = returns[0]
            return_type = get_python_type(return_)
            code += '    return {}\n'.format(make_return_code(return_))
        elif len(returns) > 1:
            # we should be able to refactor the first part of this if block to have something
            # reusable, then we call that new thing inside of a loop in this elif block
            # the only difference here is printing key names and dict syntax
            code += '    result: T_JSON_DICT = {\n'
            # code += '    return {\n'
            for return_ in returns:
                if return_.get('optional', False):
                    continue
                return_type = get_python_type(return_)
                code += "        '{}': {},\n".format(return_['name'],
                    make_return_code(return_))
            code += '    }\n'
            for return_ in returns:
                if not return_.get('optional', False):
                    continue
                code += "    if '{}' in json:\n".format(return_['name'])
                code += "        result['{}'] = {}\n".format(return_['name'],
                    make_return_code(return_))
            code += '    return result\n'
        code += '\n\n'
    return [domain_name], code


def make_return_code(return_):
    '''
    Make a snippet of code that retuns a value inside of a ``from_json()``
    method.

    :param dict return_: the CDP metadata for the item to return
    :returns: a string
    '''
    return_name = return_['name']
    return_type = get_python_type(return_)
    if 'typing.List' in return_type:
        subtype = get_python_type(return_['items'])
        if subtype.startswith('typing.Any'):
            code = "[i for i in json['{}']]".format(return_name)
        elif 'type' in return_['items'] or is_builtin_type(subtype):
            code = "[{}(i) for i in json['{}']]".format(subtype, return_name)
        else:
            code = "[{}.from_json(i) for i in json['{}']]".format(subtype, return_name)
    elif is_builtin_type(return_type):
        code = "{}(json['{}'])".format(return_type, return_name)
    elif return_type.startswith('typing.Any'):
        code = "json['{}']".format(return_name)
    else:
        code = "{}.from_json(json['{}'])".format(return_type, return_name)
    return code


def generate_init(init_path, modules):
    '''
    Generate an ``__init__.py`` that exports the specified modules.

    :param Path init_path: a file path to create the init file in
    :param list[tuple] modules: a list of modules each represented as tuples
        of (name, list_of_exported_symbols)
    '''
    modules = [module[0] for module in modules]
    modules.sort()
    with init_path.open('w') as init_file:
        init_file.write(init_header)
        for submodule in ('types', 'events', 'commands'):
            for module in modules:
                init_file.write('import cdp.{}.{}\n'.format(module, submodule))
            init_file.write('\n')
        init_file.write('import cdp.util\n')


def main():
    ''' Main entry point. '''
    here = Path(__file__).parent.resolve()
    json_paths = [
        here / 'browser_protocol.json',
        here / 'js_protocol.json',
    ]
    output_path = here.parent / 'cdp'
    clear_dirs(output_path)

    modules = list()
    for json_path in json_paths:
        logger.info('Parsing JSON file %s', json_path)
        modules.extend(parse(json_path, output_path))

    init_path = output_path / '__init__.py'
    generate_init(init_path, modules)

    py_typed_path = output_path / 'py.typed'
    py_typed_path.touch()


if __name__ == '__main__':
    main()
