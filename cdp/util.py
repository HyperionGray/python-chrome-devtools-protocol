import cdp
import inflection
import typing


T_JSON_DICT = typing.Dict[str, typing.Any]


def parse_json_event(json: dict) -> typing.Tuple[str, str, typing.Any]:
    ''' Parse a JSON dictionary into a CDP event. '''
    domain, event_name = json['method'].split('.')
    module = getattr(getattr(cdp, inflection.underscore(domain)), 'events')
    cls_name = inflection.camelize(event_name, uppercase_first_letter=True)
    cls = getattr(module, cls_name)
    return cls._domain, cls._method, cls.from_json(json['params'])
