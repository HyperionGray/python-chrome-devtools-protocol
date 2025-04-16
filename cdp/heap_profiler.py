# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: HeapProfiler (experimental)

from __future__ import annotations
from cdp.util import event_class, T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from . import runtime


class HeapSnapshotObjectId(str):
    r'''
    Heap snapshot object id.
    '''
    def to_json(self) -> str:
        return self

    @classmethod
    def from_json(cls, json: str) -> HeapSnapshotObjectId:
        return cls(json)

    def __repr__(self):
        return 'HeapSnapshotObjectId({})'.format(super().__repr__())


@dataclass
class SamplingHeapProfileNode:
    r'''
    Sampling Heap Profile node. Holds callsite information, allocation statistics and child nodes.
    '''
    #: Function location.
    call_frame: runtime.CallFrame

    #: Allocations size in bytes for the node excluding children.
    self_size: float

    #: Node id. Ids are unique across all profiles collected between startSampling and stopSampling.
    id_: int

    #: Child nodes.
    children: typing.List[SamplingHeapProfileNode]

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['callFrame'] = self.call_frame.to_json()
        json['selfSize'] = self.self_size
        json['id'] = self.id_
        json['children'] = [i.to_json() for i in self.children]
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SamplingHeapProfileNode:
        return cls(
            call_frame=runtime.CallFrame.from_json(json['callFrame']),
            self_size=float(json['selfSize']),
            id_=int(json['id']),
            children=[SamplingHeapProfileNode.from_json(i) for i in json['children']],
        )


@dataclass
class SamplingHeapProfileSample:
    r'''
    A single sample from a sampling profile.
    '''
    #: Allocation size in bytes attributed to the sample.
    size: float

    #: Id of the corresponding profile tree node.
    node_id: int

    #: Time-ordered sample ordinal number. It is unique across all profiles retrieved
    #: between startSampling and stopSampling.
    ordinal: float

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['size'] = self.size
        json['nodeId'] = self.node_id
        json['ordinal'] = self.ordinal
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SamplingHeapProfileSample:
        return cls(
            size=float(json['size']),
            node_id=int(json['nodeId']),
            ordinal=float(json['ordinal']),
        )


@dataclass
class SamplingHeapProfile:
    r'''
    Sampling profile.
    '''
    head: SamplingHeapProfileNode

    samples: typing.List[SamplingHeapProfileSample]

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['head'] = self.head.to_json()
        json['samples'] = [i.to_json() for i in self.samples]
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SamplingHeapProfile:
        return cls(
            head=SamplingHeapProfileNode.from_json(json['head']),
            samples=[SamplingHeapProfileSample.from_json(i) for i in json['samples']],
        )


def add_inspected_heap_object(
        heap_object_id: HeapSnapshotObjectId
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    Enables console to refer to the node with given id via $x (see Command Line API for more details
    $x functions).

    :param heap_object_id: Heap snapshot object id to be accessible by means of $x command line API.
    '''
    params: T_JSON_DICT = dict()
    params['heapObjectId'] = heap_object_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.addInspectedHeapObject',
        'params': params,
    }
    json = yield cmd_dict


def collect_garbage() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:

    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.collectGarbage',
    }
    json = yield cmd_dict


def disable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:

    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.disable',
    }
    json = yield cmd_dict


def enable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:

    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.enable',
    }
    json = yield cmd_dict


def get_heap_object_id(
        object_id: runtime.RemoteObjectId
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,HeapSnapshotObjectId]:
    r'''
    :param object_id: Identifier of the object to get heap object id for.
    :returns: Id of the heap snapshot object corresponding to the passed remote object id.
    '''
    params: T_JSON_DICT = dict()
    params['objectId'] = object_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.getHeapObjectId',
        'params': params,
    }
    json = yield cmd_dict
    return HeapSnapshotObjectId.from_json(json['heapSnapshotObjectId'])


def get_object_by_heap_object_id(
        object_id: HeapSnapshotObjectId,
        object_group: typing.Optional[str] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,runtime.RemoteObject]:
    r'''
    :param object_id:
    :param object_group: *(Optional)* Symbolic group name that can be used to release multiple objects.
    :returns: Evaluation result.
    '''
    params: T_JSON_DICT = dict()
    params['objectId'] = object_id.to_json()
    if object_group is not None:
        params['objectGroup'] = object_group
    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.getObjectByHeapObjectId',
        'params': params,
    }
    json = yield cmd_dict
    return runtime.RemoteObject.from_json(json['result'])


def get_sampling_profile() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,SamplingHeapProfile]:
    r'''


    :returns: Return the sampling profile being collected.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.getSamplingProfile',
    }
    json = yield cmd_dict
    return SamplingHeapProfile.from_json(json['profile'])


def start_sampling(
        sampling_interval: typing.Optional[float] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param sampling_interval: *(Optional)* Average sample interval in bytes. Poisson distribution is used for the intervals. The default value is 32768 bytes.
    '''
    params: T_JSON_DICT = dict()
    if sampling_interval is not None:
        params['samplingInterval'] = sampling_interval
    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.startSampling',
        'params': params,
    }
    json = yield cmd_dict


def start_tracking_heap_objects(
        track_allocations: typing.Optional[bool] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param track_allocations: *(Optional)*
    '''
    params: T_JSON_DICT = dict()
    if track_allocations is not None:
        params['trackAllocations'] = track_allocations
    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.startTrackingHeapObjects',
        'params': params,
    }
    json = yield cmd_dict


def stop_sampling() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,SamplingHeapProfile]:
    r'''


    :returns: Recorded sampling heap profile.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.stopSampling',
    }
    json = yield cmd_dict
    return SamplingHeapProfile.from_json(json['profile'])


def stop_tracking_heap_objects(
        report_progress: typing.Optional[bool] = None,
        treat_global_objects_as_roots: typing.Optional[bool] = None,
        capture_numeric_value: typing.Optional[bool] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param report_progress: *(Optional)* If true 'reportHeapSnapshotProgress' events will be generated while snapshot is being taken when the tracking is stopped.
    :param treat_global_objects_as_roots: *(Optional)*
    :param capture_numeric_value: *(Optional)* If true, numerical values are included in the snapshot
    '''
    params: T_JSON_DICT = dict()
    if report_progress is not None:
        params['reportProgress'] = report_progress
    if treat_global_objects_as_roots is not None:
        params['treatGlobalObjectsAsRoots'] = treat_global_objects_as_roots
    if capture_numeric_value is not None:
        params['captureNumericValue'] = capture_numeric_value
    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.stopTrackingHeapObjects',
        'params': params,
    }
    json = yield cmd_dict


def take_heap_snapshot(
        report_progress: typing.Optional[bool] = None,
        treat_global_objects_as_roots: typing.Optional[bool] = None,
        capture_numeric_value: typing.Optional[bool] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param report_progress: *(Optional)* If true 'reportHeapSnapshotProgress' events will be generated while snapshot is being taken.
    :param treat_global_objects_as_roots: *(Optional)* If true, a raw snapshot without artificial roots will be generated
    :param capture_numeric_value: *(Optional)* If true, numerical values are included in the snapshot
    '''
    params: T_JSON_DICT = dict()
    if report_progress is not None:
        params['reportProgress'] = report_progress
    if treat_global_objects_as_roots is not None:
        params['treatGlobalObjectsAsRoots'] = treat_global_objects_as_roots
    if capture_numeric_value is not None:
        params['captureNumericValue'] = capture_numeric_value
    cmd_dict: T_JSON_DICT = {
        'method': 'HeapProfiler.takeHeapSnapshot',
        'params': params,
    }
    json = yield cmd_dict


@event_class('HeapProfiler.addHeapSnapshotChunk')
@dataclass
class AddHeapSnapshotChunk:
    chunk: str

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AddHeapSnapshotChunk:
        return cls(
            chunk=str(json['chunk'])
        )


@event_class('HeapProfiler.heapStatsUpdate')
@dataclass
class HeapStatsUpdate:
    r'''
    If heap objects tracking has been started then backend may send update for one or more fragments
    '''
    #: An array of triplets. Each triplet describes a fragment. The first integer is the fragment
    #: index, the second integer is a total count of objects for the fragment, the third integer is
    #: a total size of the objects for the fragment.
    stats_update: typing.List[int]

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> HeapStatsUpdate:
        return cls(
            stats_update=[int(i) for i in json['statsUpdate']]
        )


@event_class('HeapProfiler.lastSeenObjectId')
@dataclass
class LastSeenObjectId:
    r'''
    If heap objects tracking has been started then backend regularly sends a current value for last
    seen object id and corresponding timestamp. If the were changes in the heap since last event
    then one or more heapStatsUpdate events will be sent before a new lastSeenObjectId event.
    '''
    last_seen_object_id: int
    timestamp: float

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LastSeenObjectId:
        return cls(
            last_seen_object_id=int(json['lastSeenObjectId']),
            timestamp=float(json['timestamp'])
        )


@event_class('HeapProfiler.reportHeapSnapshotProgress')
@dataclass
class ReportHeapSnapshotProgress:
    done: int
    total: int
    finished: typing.Optional[bool]

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ReportHeapSnapshotProgress:
        return cls(
            done=int(json['done']),
            total=int(json['total']),
            finished=bool(json['finished']) if 'finished' in json else None
        )


@event_class('HeapProfiler.resetProfiles')
@dataclass
class ResetProfiles:


    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ResetProfiles:
        return cls(

        )
