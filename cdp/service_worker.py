# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: ServiceWorker (experimental)

from __future__ import annotations
from cdp.util import event_class, T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from . import target


class RegistrationID(str):
    def to_json(self) -> str:
        return self

    @classmethod
    def from_json(cls, json: str) -> RegistrationID:
        return cls(json)

    def __repr__(self):
        return 'RegistrationID({})'.format(super().__repr__())


@dataclass
class ServiceWorkerRegistration:
    r'''
    ServiceWorker registration.
    '''
    registration_id: RegistrationID

    scope_url: str

    is_deleted: bool

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['registrationId'] = self.registration_id.to_json()
        json['scopeURL'] = self.scope_url
        json['isDeleted'] = self.is_deleted
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ServiceWorkerRegistration:
        return cls(
            registration_id=RegistrationID.from_json(json['registrationId']),
            scope_url=str(json['scopeURL']),
            is_deleted=bool(json['isDeleted']),
        )


class ServiceWorkerVersionRunningStatus(enum.Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"

    def to_json(self) -> str:
        return self.value

    @classmethod
    def from_json(cls, json: str) -> ServiceWorkerVersionRunningStatus:
        return cls(json)


class ServiceWorkerVersionStatus(enum.Enum):
    NEW = "new"
    INSTALLING = "installing"
    INSTALLED = "installed"
    ACTIVATING = "activating"
    ACTIVATED = "activated"
    REDUNDANT = "redundant"

    def to_json(self) -> str:
        return self.value

    @classmethod
    def from_json(cls, json: str) -> ServiceWorkerVersionStatus:
        return cls(json)


@dataclass
class ServiceWorkerVersion:
    r'''
    ServiceWorker version.
    '''
    version_id: str

    registration_id: RegistrationID

    script_url: str

    running_status: ServiceWorkerVersionRunningStatus

    status: ServiceWorkerVersionStatus

    #: The Last-Modified header value of the main script.
    script_last_modified: typing.Optional[float] = None

    #: The time at which the response headers of the main script were received from the server.
    #: For cached script it is the last time the cache entry was validated.
    script_response_time: typing.Optional[float] = None

    controlled_clients: typing.Optional[typing.List[target.TargetID]] = None

    target_id: typing.Optional[target.TargetID] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['versionId'] = self.version_id
        json['registrationId'] = self.registration_id.to_json()
        json['scriptURL'] = self.script_url
        json['runningStatus'] = self.running_status.to_json()
        json['status'] = self.status.to_json()
        if self.script_last_modified is not None:
            json['scriptLastModified'] = self.script_last_modified
        if self.script_response_time is not None:
            json['scriptResponseTime'] = self.script_response_time
        if self.controlled_clients is not None:
            json['controlledClients'] = [i.to_json() for i in self.controlled_clients]
        if self.target_id is not None:
            json['targetId'] = self.target_id.to_json()
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ServiceWorkerVersion:
        return cls(
            version_id=str(json['versionId']),
            registration_id=RegistrationID.from_json(json['registrationId']),
            script_url=str(json['scriptURL']),
            running_status=ServiceWorkerVersionRunningStatus.from_json(json['runningStatus']),
            status=ServiceWorkerVersionStatus.from_json(json['status']),
            script_last_modified=float(json['scriptLastModified']) if 'scriptLastModified' in json else None,
            script_response_time=float(json['scriptResponseTime']) if 'scriptResponseTime' in json else None,
            controlled_clients=[target.TargetID.from_json(i) for i in json['controlledClients']] if 'controlledClients' in json else None,
            target_id=target.TargetID.from_json(json['targetId']) if 'targetId' in json else None,
        )


@dataclass
class ServiceWorkerErrorMessage:
    r'''
    ServiceWorker error message.
    '''
    error_message: str

    registration_id: RegistrationID

    version_id: str

    source_url: str

    line_number: int

    column_number: int

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['errorMessage'] = self.error_message
        json['registrationId'] = self.registration_id.to_json()
        json['versionId'] = self.version_id
        json['sourceURL'] = self.source_url
        json['lineNumber'] = self.line_number
        json['columnNumber'] = self.column_number
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ServiceWorkerErrorMessage:
        return cls(
            error_message=str(json['errorMessage']),
            registration_id=RegistrationID.from_json(json['registrationId']),
            version_id=str(json['versionId']),
            source_url=str(json['sourceURL']),
            line_number=int(json['lineNumber']),
            column_number=int(json['columnNumber']),
        )


def deliver_push_message(
        origin: str,
        registration_id: RegistrationID,
        data: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param origin:
    :param registration_id:
    :param data:
    '''
    params: T_JSON_DICT = dict()
    params['origin'] = origin
    params['registrationId'] = registration_id.to_json()
    params['data'] = data
    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.deliverPushMessage',
        'params': params,
    }
    json = yield cmd_dict


def disable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:

    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.disable',
    }
    json = yield cmd_dict


def dispatch_sync_event(
        origin: str,
        registration_id: RegistrationID,
        tag: str,
        last_chance: bool
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param origin:
    :param registration_id:
    :param tag:
    :param last_chance:
    '''
    params: T_JSON_DICT = dict()
    params['origin'] = origin
    params['registrationId'] = registration_id.to_json()
    params['tag'] = tag
    params['lastChance'] = last_chance
    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.dispatchSyncEvent',
        'params': params,
    }
    json = yield cmd_dict


def dispatch_periodic_sync_event(
        origin: str,
        registration_id: RegistrationID,
        tag: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param origin:
    :param registration_id:
    :param tag:
    '''
    params: T_JSON_DICT = dict()
    params['origin'] = origin
    params['registrationId'] = registration_id.to_json()
    params['tag'] = tag
    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.dispatchPeriodicSyncEvent',
        'params': params,
    }
    json = yield cmd_dict


def enable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:

    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.enable',
    }
    json = yield cmd_dict


def inspect_worker(
        version_id: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param version_id:
    '''
    params: T_JSON_DICT = dict()
    params['versionId'] = version_id
    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.inspectWorker',
        'params': params,
    }
    json = yield cmd_dict


def set_force_update_on_page_load(
        force_update_on_page_load: bool
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param force_update_on_page_load:
    '''
    params: T_JSON_DICT = dict()
    params['forceUpdateOnPageLoad'] = force_update_on_page_load
    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.setForceUpdateOnPageLoad',
        'params': params,
    }
    json = yield cmd_dict


def skip_waiting(
        scope_url: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param scope_url:
    '''
    params: T_JSON_DICT = dict()
    params['scopeURL'] = scope_url
    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.skipWaiting',
        'params': params,
    }
    json = yield cmd_dict


def start_worker(
        scope_url: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param scope_url:
    '''
    params: T_JSON_DICT = dict()
    params['scopeURL'] = scope_url
    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.startWorker',
        'params': params,
    }
    json = yield cmd_dict


def stop_all_workers() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:

    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.stopAllWorkers',
    }
    json = yield cmd_dict


def stop_worker(
        version_id: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param version_id:
    '''
    params: T_JSON_DICT = dict()
    params['versionId'] = version_id
    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.stopWorker',
        'params': params,
    }
    json = yield cmd_dict


def unregister(
        scope_url: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param scope_url:
    '''
    params: T_JSON_DICT = dict()
    params['scopeURL'] = scope_url
    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.unregister',
        'params': params,
    }
    json = yield cmd_dict


def update_registration(
        scope_url: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    :param scope_url:
    '''
    params: T_JSON_DICT = dict()
    params['scopeURL'] = scope_url
    cmd_dict: T_JSON_DICT = {
        'method': 'ServiceWorker.updateRegistration',
        'params': params,
    }
    json = yield cmd_dict


@event_class('ServiceWorker.workerErrorReported')
@dataclass
class WorkerErrorReported:
    error_message: ServiceWorkerErrorMessage

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WorkerErrorReported:
        return cls(
            error_message=ServiceWorkerErrorMessage.from_json(json['errorMessage'])
        )


@event_class('ServiceWorker.workerRegistrationUpdated')
@dataclass
class WorkerRegistrationUpdated:
    registrations: typing.List[ServiceWorkerRegistration]

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WorkerRegistrationUpdated:
        return cls(
            registrations=[ServiceWorkerRegistration.from_json(i) for i in json['registrations']]
        )


@event_class('ServiceWorker.workerVersionUpdated')
@dataclass
class WorkerVersionUpdated:
    versions: typing.List[ServiceWorkerVersion]

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WorkerVersionUpdated:
        return cls(
            versions=[ServiceWorkerVersion.from_json(i) for i in json['versions']]
        )
