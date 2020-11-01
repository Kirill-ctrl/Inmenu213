from typing import Union

from asyncpg import Record

from src.internal.biz.deserializers.account_main import ACCOUNT_MAIN, AccountMainDeserializer, \
    DES_ACCOUNT_MAIN_FROM_DB_FULL
from src.internal.biz.deserializers.base_constants import ID, CREATED_AT, EDITED_AT
from src.internal.biz.deserializers.base_deserializer import BaseDeserializer
from src.internal.biz.deserializers.currency import CURRENCY, CurrencyDeserializer, DES_CURRENCY_FROM_DB_FULL
from src.internal.biz.deserializers.language import LanguageDeserializer, DES_LANGUAGE_FROM_DB_FULL, LANGUAGE
from src.internal.biz.deserializers.photo import PHOTO, PhotoDeserializer, DES_PHOTO_FROM_DB_FULL
from src.internal.biz.deserializers.utils import filter_keys_by_substr
from src.internal.biz.entities.currency import Currency
from src.internal.biz.entities.language import Language
from src.internal.biz.entities.photo import Photo
from src.internal.biz.entities.place_main import PlaceMain

DES_PLACE_MAIN_ADD = 'place-main-add'
DES_PLACE_MAIN_FROM_DB_FULL = 'place-main-from-db-full'
DES_PLACE_MAIN_UPDATE = 'place_main_update'

PLACE_MAIN = 'plm_'
PLACE_MAIN_ID = PLACE_MAIN + ID
PLACE_MAIN_CREATED_AT = PLACE_MAIN + CREATED_AT
PLACE_MAIN_EDITED_AT = PLACE_MAIN + EDITED_AT
PLACE_MAIN_NAME = PLACE_MAIN + 'nm'
PLACE_MAIN_LOGIN = PLACE_MAIN + 'lg'
PLACE_MAIN_DESCRIPTION = PLACE_MAIN + 'ds'
PLACE_MAIN_IS_DRAFT = PLACE_MAIN + 'dr'
PLACE_MAIN_IS_PUBLISHED = PLACE_MAIN + 'pb'


class PlaceMainDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_ser: str):
        if format_ser == DES_PLACE_MAIN_ADD:
            return cls._deserialize_add
        elif format_ser == DES_PLACE_MAIN_FROM_DB_FULL:
            return cls._deserialize_from_db_full
        elif format_ser == DES_PLACE_MAIN_UPDATE:
            return cls._deserializer_update
        else:
            raise TypeError

    @staticmethod
    def _deserialize_add(place_main: dict) -> PlaceMain:
        return PlaceMain(
            main_language=Language(id=place_main.get('main_lang_id')),
            name=place_main['name'] if place_main.get('name') else None,
            login=place_main['login'] if place_main.get('login') else None,
            photo=Photo(short_url=place_main['photo_link']) if place_main.get('photo_link') else None,
            description=place_main['description'] if place_main.get('description') else None,
            main_currency=Currency(id=place_main.get('main_currency_id')),
            is_draft=place_main['extra']['is_draft'],
            is_published=not place_main['extra']['is_draft']
        )

    @staticmethod
    def _deserialize_from_db_full(place_main: Union[dict, Record]) -> PlaceMain:
        account_main = filter_keys_by_substr(place_main, ACCOUNT_MAIN)
        main_language = filter_keys_by_substr(place_main, LANGUAGE)
        photo = filter_keys_by_substr(place_main, PHOTO)
        main_currency = filter_keys_by_substr(place_main, CURRENCY)

        return PlaceMain(
            id=place_main.get(PLACE_MAIN_ID),
            created_at=place_main.get(PLACE_MAIN_CREATED_AT),
            edited_at=place_main.get(PLACE_MAIN_EDITED_AT),
            main_language=LanguageDeserializer.deserialize(main_language, DES_LANGUAGE_FROM_DB_FULL),
            account_main=AccountMainDeserializer.deserialize(account_main, DES_ACCOUNT_MAIN_FROM_DB_FULL),
            name=place_main.get(PLACE_MAIN_NAME),
            login=place_main.get(PLACE_MAIN_LOGIN),
            photo=PhotoDeserializer.deserialize(photo, DES_PHOTO_FROM_DB_FULL),
            description=place_main.get(PLACE_MAIN_DESCRIPTION),
            main_currency=CurrencyDeserializer.deserialize(main_currency, DES_CURRENCY_FROM_DB_FULL),
            is_draft=place_main.get(PLACE_MAIN_IS_DRAFT),
            is_published=place_main.get(PLACE_MAIN_IS_PUBLISHED)
        )

    @staticmethod
    def _deserializer_update(place_main: dict) -> PlaceMain:
        place_main_1 =  PlaceMain(
            main_language=Language(id=place_main['main_lang_id'] if place_main.get('main_lang_id') is not None else 0) if 'main_lang_id' in place_main.keys() else None,
            name=(place_main['name'] if place_main.get('name') is not None else '0') if 'name' in place_main.keys() else None,
            login=(place_main['login'] if place_main.get('login') is not None else '0') if 'login' in place_main.keys() else None,
            photo=Photo(short_url=place_main['photo_link'] if place_main.get('photo_link') is not None else '0') if 'photo_link' in place_main.keys() else None,
            description=(place_main['description'] if place_main.get('description') is not None else '0') if 'description' in place_main.keys() else None,
            main_currency=Currency(id=place_main['main_currency_id'] if place_main.get('main_currency_id') is not None else 0) if 'main_currency_id' in place_main.keys() else None
        )
        print(place_main_1.name)
        return place_main_1
