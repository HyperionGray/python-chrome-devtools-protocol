# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: CacheStorage (experimental)

from __future__ import annotations
from cdp.util import event_class, T_JSON_DICT
from dataclasses import dataclass
import enum
import typing


class CacheId(str):
    '''
    Unique identifier of the Cache object.
    '''
    def to_json(self) -> str:
        return self

    @classmethod
    def from_json(cls, json: str) -> CacheId:
        return cls(json)

    def __repr__(self):
        return 'CacheId({})'.format(super().__repr__())


class CachedResponseType(enum.Enum):
    '''
    type of HTTP response cached
    '''
    BASIC = "basic"
    CORS = "cors"
    DEFAULT = "default"
    ERROR = "error"
    OPAQUE_RESPONSE = "opaqueResponse"
    OPAQUE_REDIRECT = "opaqueRedirect"

    def to_json(self) -> str:
        return self.value

    @classmethod
    def from_json(cls, json: str) -> CachedResponseType:
        return cls(json)


@dataclass
class DataEntry:
    '''
    Data entry.
    '''
    #: Request URL.
    request_url: str

    #: Request method.
    request_method: str

    #: Request headers
    request_headers: typing.List[Header]

    #: Number of seconds since epoch.
    response_time: float

    #: HTTP response status code.
    response_status: int

    #: HTTP response status text.
    response_status_text: str

    #: HTTP response type
    response_type: CachedResponseType

    #: Response headers
    response_headers: typing.List[Header]

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['requestURL'] = self.request_url
        json['requestMethod'] = self.request_method
        json['requestHeaders'] = [i.to_json() for i in self.request_headers]
        json['responseTime'] = self.response_time
        json['responseStatus'] = self.response_status
        json['responseStatusText'] = self.response_status_text
        json['responseType'] = self.response_type.to_json()
        json['responseHeaders'] = [i.to_json() for i in self.response_headers]
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DataEntry:
        return cls(
            request_url=str(json['requestURL']),
            request_method=str(json['requestMethod']),
            request_headers=[Header.from_json(i) for i in json['requestHeaders']],
            response_time=float(json['responseTime']),
            response_status=int(json['responseStatus']),
            response_status_text=str(json['responseStatusText']),
            response_type=CachedResponseType.from_json(json['responseType']),
            response_headers=[Header.from_json(i) for i in json['responseHeaders']],
        )


@dataclass
class Cache:
    '''
    Cache identifier.
    '''
    #: An opaque unique id of the cache.
    cache_id: CacheId

    #: Security origin of the cache.
    security_origin: str

    #: The name of the cache.
    cache_name: str

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['cacheId'] = self.cache_id.to_json()
        json['securityOrigin'] = self.security_origin
        json['cacheName'] = self.cache_name
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Cache:
        return cls(
            cache_id=CacheId.from_json(json['cacheId']),
            security_origin=str(json['securityOrigin']),
            cache_name=str(json['cacheName']),
        )


@dataclass
class Header:
    name: str

    value: str

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['name'] = self.name
        json['value'] = self.value
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Header:
        return cls(
            name=str(json['name']),
            value=str(json['value']),
        )


@dataclass
class CachedResponse:
    '''
    Cached response
    '''
    #: Entry content, base64-encoded. (Encoded as a base64 string when passed over JSON)
    body: str

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['body'] = self.body
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CachedResponse:
        return cls(
            body=str(json['body']),
        )


def delete_cache(
        cache_id: CacheId
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Deletes a cache.

    :param cache_id: Id of cache for deletion.
    '''
    params: T_JSON_DICT = dict()
    params['cacheId'] = cache_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'CacheStorage.deleteCache',
        'params': params,
    }
    json = yield cmd_dict


def delete_entry(
        cache_id: CacheId,
        request: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Deletes a cache entry.

    :param cache_id: Id of cache where the entry will be deleted.
    :param request: URL spec of the request.
    '''
    params: T_JSON_DICT = dict()
    params['cacheId'] = cache_id.to_json()
    params['request'] = request
    cmd_dict: T_JSON_DICT = {
        'method': 'CacheStorage.deleteEntry',
        'params': params,
    }
    json = yield cmd_dict


def request_cache_names(
        security_origin: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List[Cache]]:
    '''
    Requests cache names.

    :param security_origin: Security origin.
    :returns: Caches for the security origin.
    '''
    params: T_JSON_DICT = dict()
    params['securityOrigin'] = security_origin
    cmd_dict: T_JSON_DICT = {
        'method': 'CacheStorage.requestCacheNames',
        'params': params,
    }
    json = yield cmd_dict
    return [Cache.from_json(i) for i in json['caches']]


def request_cached_response(
        cache_id: CacheId,
        request_url: str,
        request_headers: typing.List[Header]
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,CachedResponse]:
    '''
    Fetches cache entry.

    :param cache_id: Id of cache that contains the entry.
    :param request_url: URL spec of the request.
    :param request_headers: headers of the request.
    :returns: Response read from the cache.
    '''
    params: T_JSON_DICT = dict()
    params['cacheId'] = cache_id.to_json()
    params['requestURL'] = request_url
    params['requestHeaders'] = [i.to_json() for i in request_headers]
    cmd_dict: T_JSON_DICT = {
        'method': 'CacheStorage.requestCachedResponse',
        'params': params,
    }
    json = yield cmd_dict
    return CachedResponse.from_json(json['response'])


def request_entries(
        cache_id: CacheId,
        skip_count: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        path_filter: typing.Optional[str] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.Tuple[typing.List[DataEntry], float]]:
    '''
    Requests data from cache.

    :param cache_id: ID of cache to get entries from.
    :param skip_count: *(Optional)* Number of records to skip.
    :param page_size: *(Optional)* Number of records to fetch.
    :param path_filter: *(Optional)* If present, only return the entries containing this substring in the path
    :returns: A tuple with the following items:

        0. **cacheDataEntries** - Array of object store data entries.
        1. **returnCount** - Count of returned entries from this storage. If pathFilter is empty, it is the count of all entries from this storage.
    '''
    params: T_JSON_DICT = dict()
    params['cacheId'] = cache_id.to_json()
    if skip_count is not None:
        params['skipCount'] = skip_count
    if page_size is not None:
        params['pageSize'] = page_size
    if path_filter is not None:
        params['pathFilter'] = path_filter
    cmd_dict: T_JSON_DICT = {
        'method': 'CacheStorage.requestEntries',
        'params': params,
    }
    json = yield cmd_dict
    return (
        [DataEntry.from_json(i) for i in json['cacheDataEntries']],
        float(json['returnCount'])
    )
