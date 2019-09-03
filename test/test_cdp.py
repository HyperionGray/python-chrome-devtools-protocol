'''
Some basic tests for the generated CDP modules.
'''
from cdp import dom, io, page, tracing, util


def test_primitive_type():
    frame_id = page.FrameId('foo')
    assert repr(frame_id) == "FrameId('foo')"
    assert frame_id.to_json() == 'foo'
    assert page.FrameId.from_json('foo') == frame_id


def test_enum_type():
    tran_type = page.TransitionType.ADDRESS_BAR
    assert tran_type.name == 'ADDRESS_BAR'
    assert tran_type.value == 'address_bar'
    assert tran_type.to_json() == 'address_bar'
    assert page.TransitionType.from_json('address_bar') == tran_type


def test_class_type():
    blue = dom.RGBA(51, 153, 255)
    assert blue.a is None
    assert blue.to_json() == {'r': 51, 'g': 153, 'b': 255}
    assert dom.RGBA.from_json({'r': 51, 'g': 153, 'b': 255}) == blue

    trans_violet = dom.RGBA(51, 153, 255, 0.8)
    assert trans_violet.a == 0.8
    assert trans_violet.to_json() == {'r': 51, 'g': 153, 'b': 255, 'a': 0.8}
    assert dom.RGBA.from_json({'r': 51, 'g': 153, 'b': 255, 'a':0.8}) == trans_violet


def test_event_type():
    event = page.WindowOpen.from_json({
        'url': 'https://foo.com',
        'windowName': 'Window 1',
        'windowFeatures': ['feature1', 'feature2'],
        'userGesture': False
    })
    assert event.url == 'https://foo.com'
    assert event.window_name == 'Window 1'
    assert event.window_features == ['feature1', 'feature2']
    assert not event.user_gesture


def test_event_type_with_dependency():
    ''' This tracing event has a dependency on the io module. '''
    event = tracing.TracingComplete.from_json({
        'stream': 'Foo Stream',
        'traceFormat': tracing.StreamFormat.JSON,
        'dataLossOccurred': False,
    })
    assert isinstance(event.stream, io.StreamHandle)
    assert repr(event.stream) == "StreamHandle('Foo Stream')"
    assert event.trace_format.value == 'json'
    assert event.stream_compression is None


def test_event_dispatch():
    event = util.parse_json_event({
        'method': 'Page.windowOpen',
        'params': {
        'url': 'https://foo.com',
        'windowName': 'Window 1',
        'windowFeatures': ['feature1', 'feature2'],
        'userGesture': False
        }
    })
    assert event.url == 'https://foo.com'
    assert event.window_name == 'Window 1'
    assert event.window_features == ['feature1', 'feature2']
    assert not event.user_gesture
