from typing import List, T, Union

from asyncpg import Record

from src.internal.biz.deserializers.base_constants import ID, CREATED_AT, EDITED_AT
from src.internal.biz.deserializers.base_deserializer import BaseDeserializer, DES_FROM_DICT
from src.internal.biz.deserializers.place_main import PLACE_MAIN, PlaceMainDeserializer, DES_PLACE_MAIN_FROM_DB_FULL
from src.internal.biz.deserializers.utils import filter_keys_by_substr
from src.internal.biz.entities.place_contacts import PlaceContacts

DES_PLACE_CONTACTS_ADD = 'place-contacts-add'
DES_PLACE_CONTACTS_FROM_DB_FULL = 'place-contacts-from-db-full'
DES_PLACE_CONTACTS_UPDATE = 'place-contacts-update'

PLACE_CONTACTS = 'plcts_'
PLACE_CONTACTS_ID = PLACE_CONTACTS + ID
PLACE_CONTACTS_CREATED_AT = PLACE_CONTACTS + CREATED_AT
PLACE_CONTACTS_EDITED_AT = PLACE_CONTACTS + EDITED_AT
PLACE_CONTACTS_PHONE_NUMBER = PLACE_CONTACTS + 'phn'
PLACE_CONTACTS_EMAIL = PLACE_CONTACTS + 'em'
PLACE_CONTACTS_SITE_LINK = PLACE_CONTACTS + 'st'
PLACE_CONTACTS_VK_LINK = PLACE_CONTACTS + 'vk'
PLACE_CONTACTS_INSTAGRAM_LINK = PLACE_CONTACTS + 'in'
PLACE_CONTACTS_FACEBOOK_LINK = PLACE_CONTACTS + 'fa'


class PlaceContactsDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DICT:
            return cls._deserializer_from_dict(PlaceContacts)
        if format_des == DES_PLACE_CONTACTS_ADD:
            return cls._deserialize_add
        elif format_des == DES_PLACE_CONTACTS_FROM_DB_FULL:
            return cls._deserialize_from_db_full
        elif format_des == DES_PLACE_CONTACTS_UPDATE:
            return cls._deserialize_update
        else:
            raise TypeError

    @staticmethod
    def _deserialize_add(place_contacts: dict) -> PlaceContacts:
        return PlaceContacts(
            phone_number=place_contacts['phone_number'] if place_contacts.get('phone_number') else None,
            email=place_contacts['email'] if place_contacts.get('email') else None,
            site_link=place_contacts['site_link'] if place_contacts.get('site_link') else None,
            facebook_link=place_contacts['facebook_link'] if place_contacts.get('facebook_link') else None,
            instagram_link=place_contacts['instagram_link'] if place_contacts.get('instagram_link') else None,
            vk_link=place_contacts['vk_link'] if place_contacts.get('vk_link') else None
        )

    @staticmethod
    def _deserialize_from_db_full(place_contacts: Union[dict, Record]) -> PlaceContacts:
        place_main = filter_keys_by_substr(place_contacts, PLACE_MAIN)
        return PlaceContacts(
            id=place_contacts.get(PLACE_CONTACTS_ID),
            created_at=place_contacts.get(CREATED_AT),
            edited_at=place_contacts.get(EDITED_AT),
            place_main=PlaceMainDeserializer.deserialize(place_main, DES_PLACE_MAIN_FROM_DB_FULL),
            phone_number=place_contacts.get(PLACE_CONTACTS_PHONE_NUMBER),
            email=place_contacts.get(PLACE_CONTACTS_EMAIL),
            site_link=place_contacts.get(PLACE_CONTACTS_SITE_LINK),
            vk_link=place_contacts.get(PLACE_CONTACTS_VK_LINK),
            instagram_link=place_contacts.get(PLACE_CONTACTS_INSTAGRAM_LINK),
            facebook_link=place_contacts.get(PLACE_CONTACTS_FACEBOOK_LINK)
        )

    @staticmethod
    def _deserialize_update(place_contacts: dict) -> PlaceContacts:
        return PlaceContacts(
            phone_number=place_contacts['phone_number'] if place_contacts.get('phone_number') else None,
            email=place_contacts['email'] if place_contacts.get('email') else None,
            site_link=place_contacts['site_link'] if place_contacts.get('site_link') else None,
            facebook_link=place_contacts['facebook_link'] if place_contacts.get('facebook_link') else None,
            instagram_link=place_contacts['instagram_link'] if place_contacts.get('instagram_link') else None,
            vk_link=place_contacts['vk_link'] if place_contacts.get('vk_link') else None
        )