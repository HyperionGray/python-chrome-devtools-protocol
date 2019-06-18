# Chrome Devtools Protocol (CDP) for Python

_Status: this library is very alpha. Do not use it! It is not on PyPI yet but
when we get a little more stable it will be published there._

## Overview

This repository contains Python type wrappers for the Chrome DevTools Protocol
(CDP), which is a JSON RPC protocol used for driving Chrome in headless browsing
mode. This code is all generated from the CDP specification, which is itself a
set of JSON documents that define the protocols base types, events, and
commands.

**This library does not perform any I/O!** This library generates Pythonic
wrappers for all of the items defined in the protocol. These wrappers make it
easy to generate the JSON messages that are sent to the browser and parse the
responses. The benefits of using this library versus writing JSON directly are:

* Writing in Python is less tedious: there are fewer braces and quotes to worry
  about balancing than in JSON.
* Python will help avoid typos: it knows what types are defined and will raise
  `AttributeError` if you make a typo.
* It can also help your IDE to autocomplete type names, commands, arguments,
  etc.

Most developers should use a higher level library that wraps this library and
handles the protocol I/O. You should only use this library if you want to write
such a wrapper library yourself.

## Basic Types

CDP has several primitive types such as `string`, `integer`, and `object`. For
basic types like `string` and `integer`, this library generates a trivial
wrapper around the type. For example, CDP has the following basic type:

```
{
    "types": [
        {
            "id": "ScriptIdentifier",
            "description": "Unique script identifier.",
            "type": "string"
        },
        ...
    ]
}
```

This CDP type corresponds to the following Python code:

```python
class ScriptIdentifier(str):
    '''
    Unique script identifier.
    '''
    @classmethod
    def from_json(cls, json):
        return cls(json)

    def __repr__(self):
        return 'ScriptIdentifier({})'.format(str.__repr__(self))
```

The type extends a built-in type (`str`) and adds a `repr()` that is helpful
when debugging or logging. It also creates a `from_json()` method that is
used for generating instances of the type from JSON representations. Although
this method is trivial for these basic types, more complex types also implement
the same interface for converting JSON into Python instances.

TODO: explain enum

CDP uses the `object` type to describe more complicated data types. Here's an
example:

```
{
    "types": [
        {
            "id": "FrameTree",
            "description": "Information about the Frame hierarchy.",
            "type": "object",
            "properties": [
                {
                    "name": "frame",
                    "description": "Frame information for this tree item.",
                    "$ref": "Frame"
                },
                {
                    "name": "childFrames",
                    "description": "Child frames.",
                    "optional": true,
                    "type": "array",
                    "items": {
                        "$ref": "FrameTree"
                    }
                }
            ]
        },
        ...
    ]
}
```

This corresponds to the following Python code:

```python3
@dataclass
class FrameTree:
    '''
    Information about the Frame hierarchy.
    '''
    #: Frame information for this tree item.
    frame: Frame

    #: Child frames.
    child_frames: typing.List['FrameTree']

    @classmethod
    def from_json(cls, json):
        return cls(
            frame=Frame.from_json(json.get('frame')),
            child_frames=[FrameTree.from_json(i) for i in json.get('childFrames')],
        )
```

The generated Python code is a dataclass, complete with docstring, type
annotations, and a non-trivial `from_json()` method. Notice that protocol
fields like `child_frames` are snake-cased: it is automatically converted to
camel-case when generating JSON and vice-versa.

## Commands

The CDP commands are the trickiest part of this library, because each "command"
is really a remote procedure call over a network socket! Here's an example of a
CDP command specification from the `Target` domain:

```
{
    "commands": [
        {
            "name": "getTargetInfo",
            "description": "Returns information about a target.",
            "experimental": true,
            "parameters": [
                {
                    "name": "targetId",
                    "optional": true,
                    "$ref": "TargetID"
                }
            ],
            "returns": [
                {
                    "name": "targetInfo",
                    "$ref": "TargetInfo"
                }
            ]
        },
        ...
    ]
}
```

This leads to the following generated Python code:

```python3
  def get_target_info(target_id: TargetID) -> typing.Generator[dict,dict,TargetInfo]:
      '''
      Returns information about a target.

      :param target_id:
      :returns:
      '''

      cmd_dict = {
          'method': 'Target.getTargetInfo',
          'params': {
              'targetId': target_id,
          }
      }
      response = yield cmd_dict
      return TargetInfo.from_json(response['targetInfo'])
```

First, notice that all commands in the `Target` domain are generated as
functions inside of the module `cdp.target.commands` on a class called `Target`.
Therefore, a fully-qualified CDP command command like `Target.getTargetInfo`
translates to a Python function called `cdp.target.commands.get_target_info`.

Second, notice that the command has the proper type annotations and docstring
derived from the CDP metadata. Depending on your IDE, this should help with
autocompletion.

Third—and this is the tricky bit—we have a single function that can both
generate a CDP JSON command and also parse the response without doing any actual
I/O in between! In order to accommodate this goal, each command is actually a
_generator function_. To run a command, you should do the following:

1. Invoke the function to obtain a generator `gen`.
2. Get the request by calling `request = gen.send(None)`.
3. Send the request to Chrome using whatever I/O framework you want and wait for
   the response. (Notice that commands are multiplexed on a single WebSocket, so
   you will also need to do some bookkeeping to track which responses correspond
   to which requests. That logic is outside the scope of this explanation.)
4. Send the response back to the generator by calling `gen.send(response)`.
5. The generator will raise `StopIteration`. You should catch this exception,
   and the command's result is stored in the exception's `value` field.

Here's some sample code. This code sets the command ID to zero every time. As
mentioned above, you'll need to generate unique command IDs if you want to send
multiple commands concurrently.

```python
from cdp import Target, TargetID

def run_command(cmd):
    # Run the generator once to get a request.
    request_dict = cmd.send(None)
    request_dict['id'] = 0
    request_str = json.dumps(request_dict)
    # vvv Use whatever I/O framework you want. vvv
    mysock.send(request_str)
    response_str = mysock.recv()
    # ^^^ Use whatever I/O framework you want. ^^^
    response_dict = json.loads(response_str)
    try:
        cmd.send(response_dict)
        raise Exception('Should not reach this line!')
    except StopIteration as exit:
        response = exit.value
    return response

target_id = TargetID('F86FCB9B3890EB413FAC5DD9DD150E6F')
target_info = run_command(Target.get_target_info(target_info))
print(target_info)
```

The script above prints something like this:

```
TargetInfo(target_id=TargetID('F86FCB9B3890EB413FAC5DD9DD150E6F'), type_='page',
title='New Tab', url='chrome://newtab/', attached=False, opener_id=TargetID('None'),
browser_context_id=BrowserContextID('B26C01EBDA29AC04BE3966B4E50F3F49'))
```

## Events

While each command elicits a single response, the CDP protocol provides _events_
as a mechanism for the browser to send information to the client that is not
necessarily tied to a single command/response pair. Here's an example of a CDP
event definition:

```json
{
    "name": "attachedToTarget",
    "description": "Issued when attached to target because of auto-attach or `attachToTarget` command.",
    "experimental": true,
    "parameters": [
        {
            "name": "sessionId",
            "description": "Identifier assigned to the session used to send/receive messages.",
            "$ref": "SessionID"
        },
        {
            "name": "targetInfo",
            "$ref": "TargetInfo"
        },
        {
            "name": "waitingForDebugger",
            "type": "boolean"
        }
    ]
}
```

This gets translated into the following Python code:

```python
@dataclass
class AttachedToTarget:
    '''
    Issued when attached to target because of auto-attach or `attachToTarget` command.
    '''
    #: Issued when attached to target because of auto-attach or `attachToTarget` command.
    session_id: SessionID

    #: Issued when attached to target because of auto-attach or `attachToTarget` command.
    target_info: TargetInfo

    #: Issued when attached to target because of auto-attach or `attachToTarget` command.
    waiting_for_debugger: bool

    @classmethod
    def from_json(cls, json: dict) -> 'AttachedToTarget':
        return cls(
            session_id=SessionID.from_json(response['sessionId']),
            target_info=TargetInfo.from_json(response['targetInfo']),
            waiting_for_debugger=bool(response['waitingForDebugger']),
        )
```

The generated code consists of a dataclass the contains the event's attributes.
The dataclass also contains a `from_json()` class method (similar to the
`from_json()` class method that each type has) to construct an instance of the
object from a JSON dictionary. The library also has a convenience function
`cdp.parse_json_event(json: dict)` that will take a JSON dictionary, look up the
corresponding event class, instantiate it with the parameters contained in
the JSON dictionary, and return the instance.

## Build

The protocol specifications and a build tool are stored in the `build`
directory. Before running the build tool, install the build requirements in
requirements.txt.

Run the build tool as follows:

```
$ python build/generate.py
```

This will write all of the generated files into the `cdp` package directory.
