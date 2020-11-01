from typing import Union

from asyncpg import Record

from src.internal.biz.deserializers.base_constants import ID, CREATED_AT, EDITED_AT
from src.internal.biz.deserializers.base_deserializer import BaseDeserializer
from src.internal.biz.deserializers.place_main import PLACE_MAIN, PlaceMainDeserializer, DES_PLACE_MAIN_FROM_DB_FULL
from src.internal.biz.deserializers.utils import filter_keys_by_substr
from src.internal.biz.entities.place_location import PlaceLocation


DES_PLACE_LOCATION_FROM_DB_FULL = 'place-location-from-db-full'
DES_PLACE_LOCATIONS_UPDATE = 'place-locations-update'

PLACE_LOCATION = 'plloc_'
PLACE_LOCATION_ID = PLACE_LOCATION + ID
PLACE_LOCATION_CREATED_AT = PLACE_LOCATION + CREATED_AT
PLACE_LOCATION_EDITED_AT = PLACE_LOCATION + EDITED_AT
PLACE_LOCATION_FULL_ADDRESS = PLACE_LOCATION + 'fa'
PLACE_LOCATION_COORD_LAT = PLACE_LOCATION + 'clt'
PLACE_LOCATION_COORD_LONG = PLACE_LOCATION + 'clg'
PLACE_LOCATION_CITY = PLACE_LOCATION + 'ct'
PLACE_LOCATION_COUNTRY = PLACE_LOCATION + 'co'
PLACE_LOCATION_COUNT_PLACES = PLACE_LOCATION + 'cp'


class PlaceLocationDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_PLACE_LOCATION_FROM_DB_FULL:
            return cls._deserialize_from_db_full
        elif format_des == DES_PLACE_LOCATIONS_UPDATE:
            return cls._deserialize_update
        else:
            raise TypeError

    @staticmethod
    def _deserialize_from_db_full(place_location: Union[dict, Record]) -> PlaceLocation:
        place_main = filter_keys_by_substr(place_location, PLACE_MAIN)
        return PlaceLocation(
            id=place_location.get(PLACE_LOCATION_ID),
            created_at=place_location.get(PLACE_LOCATION_CREATED_AT),
            edited_at=place_location.get(PLACE_LOCATION_EDITED_AT),
            place_main=PlaceMainDeserializer.deserialize(place_main, DES_PLACE_MAIN_FROM_DB_FULL),
            full_address=place_location.get(PLACE_LOCATION_FULL_ADDRESS),
            coords=tuple([place_location[PLACE_LOCATION_COORD_LAT], place_location[PLACE_LOCATION_COORD_LONG]]) if place_location.get(PLACE_LOCATION_COORD_LAT) and place_location.get(PLACE_LOCATION_COORD_LONG) else None,
            city=place_location.get(PLACE_LOCATION_CITY),
            country=place_location.get(PLACE_LOCATION_COUNTRY),
            count_places=place_location.get(PLACE_LOCATION_COUNT_PLACES)
        )

    @staticmethod
    def _deserialize_update(place_location: dict) -> PlaceLocation:
        return PlaceLocation(
            full_address=place_location['full_address'],
            city=place_location['city'],
            country=place_location['country'],
            coords=(place_location['coords']['lat'], place_location['coords']['long'])
        )
