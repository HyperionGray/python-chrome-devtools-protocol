Getting Started
===============

The best way to understand how to use PyCDP is to look at how it converts the
machine-readable Chrome DevTools Protocol (CDP) spec into Python code. Once you
understand the code generation process, the usage of the API should be fairly
intuitive.

The CDP organizes all functionality into "domains", such as "Browser", "DOM",
and "Page". Each CDP domain corresponds to a Python module in this project, e.g.
``cdp.browser``, ``cdp.dom``, and ``cdp.page``. Note that all names in this
project are adjusted to match Pythonic idioms, such as camel casing class names
and snake casing module/function/variable names.

Within each domain, CDP specifies three things. Note that CDP types can be
further divided into three categories.

1. Types: Primitives, Enumerations, & Classes
2. Commands
3. Events

This section shows examples of the CDP specification for each of these
things, and then explains how that specification is used to generate Python
code.


Primitive Types
---------------

CDP defines several data types that are aliases for primitive types. For
example, CDP has the following primitive type that is just an alias for
``string``:

.. code-block:: json

    {
        "id": "ScriptIdentifier",
        "description": "Unique script identifier.",
        "type": "string"
    }

The CDP ``string`` type corresponds directly to the Python ``str`` type. A
wrapper class is generated that extends the built-in type and provides a helpful
``repr()``.

.. code-block:: python
    :linenos:

    class ScriptId(str):
        '''
        Unique script identifier.
        '''
        def to_json(self) -> str:
            return self

        @classmethod
        def from_json(cls, json: str) -> 'ScriptId':
            return cls(json)

        def __repr__(self):
            return 'ScriptId({})'.format(super().__repr__())

.. note::

  The ``to_json()`` and ``from_json()`` methods are used within the library to
  convert to and from JSON representations. Although these methods are trivial
  for a primitive type, more complex types also implement the same interface for
  converting JSON into Python instances.

Generally speaking, you won't need to instantiate primitive types directly.
Instead, you'll receive a primitive type (such as script identifier) from one
API call and then you'll send it back as an argument to a later API call.


Enumeration Types
-----------------

CDP specifies enumerations to provide named constants. Enumeration values are
always strings.

.. code-block:: json

    {
        "id": "ClientNavigationReason",
        "experimental": true,
        "type": "string",
        "enum": [
            "formSubmissionGet",
            "formSubmissionPost",
            "httpHeaderRefresh",
            "scriptInitiated",
            "metaTagRefresh",
            "pageBlockInterstitial",
            "reload"
        ]
    }

A CDP enumeration generates a native Python ``Enum`` where the names are upper
snake case (like Python constants) and the values contain the CDP constant.

.. code-block:: python
    :linenos:

    class ClientNavigationReason(enum.Enum):
        FORM_SUBMISSION_GET = "formSubmissionGet"
        FORM_SUBMISSION_POST = "formSubmissionPost"
        HTTP_HEADER_REFRESH = "httpHeaderRefresh"
        SCRIPT_INITIATED = "scriptInitiated"
        META_TAG_REFRESH = "metaTagRefresh"
        PAGE_BLOCK_INTERSTITIAL = "pageBlockInterstitial"
        RELOAD = "reload"

        def to_json(self) -> str:
            return self.value

        @classmethod
        def from_json(cls, json: str) -> 'ClientNavigationReason':
            return cls(json)

These enumerations are especially helpful for getting useful autocompletions!


Class Types
-----------

CDP can also specify more complex data structures that have nested properties.

.. code-block:: json

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
    }

These CDP data structures are converted into Python dataclasses, which provide
useful constructors, automatic ``repr()``, and other benefits.

.. code-block:: python
    :linenos:

    @dataclass
    class FrameTree:
        '''
        Information about the Frame hierarchy.
        '''
        #: Frame information for this tree item.
        frame: 'Frame'

        #: Child frames.
        child_frames: typing.Optional[typing.List['FrameTree']] = None

        def to_json(self) -> T_JSON_DICT:
            json: T_JSON_DICT = dict()
            json['frame'] = self.frame.to_json()
            if self.child_frames is not None:
                json['childFrames'] = [i.to_json() for i in self.child_frames]
            return json

        @classmethod
        def from_json(cls, json: T_JSON_DICT) -> 'FrameTree':
            return cls(
                frame=Frame.from_json(json['frame']),
                child_frames=[FrameTree.from_json(i) for i in json['childFrames']] if 'childFrames' in json else None,
            )

Notice that all elements of the generated class are carefully annotated with
types. These types can improve autocompletion and also allow you to type check
your own code that uses PyCDP.


.. _getting-started-commands:

Commands
--------

CDP commands are the trickiest part of this library. Keep in mind, this library
does not perform any I/O, yet each command is actually a remote procedure call
over a network socket! This behavior is explained in detail in this section.
First, here is an example of a CDP command specification.

.. code-block:: json

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
    }

A CDP command is generated into a Python function with the same parameters and
return values as described in the specification:

.. code-block:: python
    :linenos:

    def get_target_info(
            target_id: typing.Optional['TargetID'] = None
        ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,'TargetInfo']:
        '''
        Returns information about a target.

        :param target_id:
        :returns:
        '''
        params: T_JSON_DICT = dict()
        if target_id is not None:
            params['targetId'] = target_id.to_json()
        cmd_dict: T_JSON_DICT = {
            'method': 'Target.getTargetInfo',
            'params': params,
        }
        json = yield cmd_dict
        return TargetInfo.from_json(json['targetInfo'])

The generated Python function takes the same arguments and returns the same
types as the CDP command. The tricky bit is that we have a single function that
can generate a CDP JSON command and then parse the response–without doing any
actual I/O in between!

In order to accommodate this goal, each command is actually a *generator
function*. To run a command, you should do the following:

1. Invoke the function to obtain a generator ``gen``.
2. Get the request by calling ``request = gen.send(None)``.
3. Send the request to Chrome using whatever I/O framework you want and wait for
   the response. (Notice that commands are multiplexed on a single WebSocket, so
   you will also need to do some bookkeeping to track which responses correspond
   to which requests. That logic is outside the scope of this explanation.)
4. Send the response back to the generator by calling ``gen.send(response)``.
5. The generator will raise ``StopIteration``. You should catch this exception,
   and the command's result is stored in the exception's ``value`` field.

Here's some sample code. This code sets the command ID to zero every time. As
mentioned above, you'll need to generate unique command IDs if you want to send
multiple commands concurrently.

.. code-block:: python
    :linenos:

    from cdp import target

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

    target_id = target.TargetID('F86FCB9B3890EB413FAC5DD9DD150E6F')
    target_info = run_command(target.get_target_info(target_id))
    print(target_info)

The script above prints something like this:

.. code-block:: python

    TargetInfo(target_id=TargetID('F86FCB9B3890EB413FAC5DD9DD150E6F'), type_='page',
    title='New Tab', url='chrome://newtab/', attached=False, opener_id=TargetID('None'),
    browser_context_id=BrowserContextID('B26C01EBDA29AC04BE3966B4E50F3F49'))

This calling convention is admittedly cumbersome. In practice, you'll probably
want to use a higher-level library that handles the I/O and the calling
convention transparently for you.


Events
------

While each command elicits a single response, the CDP protocol provides *events*
as a mechanism for the browser to send information to the client that is not
tied to a single command/response pair. Here's an example of a CDP event
definition:

.. code-block:: json

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

The following Python code is generated for this event:

.. code-block:: python
    :linenos:

    @event_class('Target.attachedToTarget')
    @dataclass
    class AttachedToTarget:
        '''
        Issued when attached to target because of auto-attach or `attachToTarget` command.
        '''
        #: Identifier assigned to the session used to send/receive messages.
        session_id: 'SessionID'
        target_info: 'TargetInfo'
        waiting_for_debugger: bool

        @classmethod
        def from_json(cls, json: T_JSON_DICT) -> 'AttachedToTarget':
            return cls(
                session_id=SessionID.from_json(json['sessionId']),
                target_info=TargetInfo.from_json(json['targetInfo']),
                waiting_for_debugger=bool(json['waitingForDebugger'])
            )

The generated code resembles the data classes used for the class types seen
above. One important difference is that event classes are decorated with the
``@event_class`` decorator. This decorator registers this function as the parser
for CDP events named ``Target.attachedToTarget``. When you receive an event, use
the following API to look up the correct parser in the registry and return an
instance of the correct class.

.. autofunction:: cdp.util.parse_json_event
