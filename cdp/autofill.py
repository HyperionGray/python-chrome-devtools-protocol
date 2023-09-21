# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: Autofill (experimental)

from __future__ import annotations
from cdp.util import event_class, T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from . import dom
from . import page


@dataclass
class CreditCard:
    #: 16-digit credit card number.
    number: str

    #: Name of the credit card owner.
    name: str

    #: 2-digit expiry month.
    expiry_month: str

    #: 4-digit expiry year.
    expiry_year: str

    #: 3-digit card verification code.
    cvc: str

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['number'] = self.number
        json['name'] = self.name
        json['expiryMonth'] = self.expiry_month
        json['expiryYear'] = self.expiry_year
        json['cvc'] = self.cvc
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CreditCard:
        return cls(
            number=str(json['number']),
            name=str(json['name']),
            expiry_month=str(json['expiryMonth']),
            expiry_year=str(json['expiryYear']),
            cvc=str(json['cvc']),
        )


@dataclass
class AddressField:
    #: address field name, for example GIVEN_NAME.
    name: str

    #: address field name, for example Jon Doe.
    value: str

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['name'] = self.name
        json['value'] = self.value
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AddressField:
        return cls(
            name=str(json['name']),
            value=str(json['value']),
        )


@dataclass
class Address:
    #: fields and values defining a test address.
    fields: typing.List[AddressField]

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['fields'] = [i.to_json() for i in self.fields]
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Address:
        return cls(
            fields=[AddressField.from_json(i) for i in json['fields']],
        )


def trigger(
        field_id: dom.BackendNodeId,
        frame_id: typing.Optional[page.FrameId] = None,
        card: CreditCard = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Trigger autofill on a form identified by the fieldId.
    If the field and related form cannot be autofilled, returns an error.

    :param field_id: Identifies a field that serves as an anchor for autofill.
    :param frame_id: *(Optional)* Identifies the frame that field belongs to.
    :param card: Credit card information to fill out the form. Credit card data is not saved.
    '''
    params: T_JSON_DICT = dict()
    params['fieldId'] = field_id.to_json()
    if frame_id is not None:
        params['frameId'] = frame_id.to_json()
    params['card'] = card.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Autofill.trigger',
        'params': params,
    }
    json = yield cmd_dict


def set_addresses(
        addresses: typing.List[Address]
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Set addresses so that developers can verify their forms implementation.

    :param addresses:
    '''
    params: T_JSON_DICT = dict()
    params['addresses'] = [i.to_json() for i in addresses]
    cmd_dict: T_JSON_DICT = {
        'method': 'Autofill.setAddresses',
        'params': params,
    }
    json = yield cmd_dict
