from typing import Union

from asyncpg import Record

from src.internal.biz.deserializers.base_deserializer import BaseDeserializer, DES_FROM_DICT
from src.internal.biz.deserializers.cuisine_types import CuisineTypesDeserializer, DES_CUISINE_TYPES_ADD, \
    DES_CUISINE_TYPES_UPDATE
from src.internal.biz.deserializers.place_contacts import PlaceContactsDeserializer, PLACE_CONTACTS, \
    DES_PLACE_CONTACTS_FROM_DB_FULL
from src.internal.biz.deserializers.place_location import PlaceLocationDeserializer, PLACE_LOCATION, \
    DES_PLACE_LOCATION_FROM_DB_FULL, DES_PLACE_LOCATIONS_UPDATE
from src.internal.biz.deserializers.place_locations import PlaceLocationsDeserializer, DES_PLACE_LOCATIONS_ADD
from src.internal.biz.deserializers.place_main import PlaceMainDeserializer, DES_PLACE_MAIN_ADD, PLACE_MAIN, \
    DES_PLACE_MAIN_FROM_DB_FULL, DES_PLACE_MAIN_UPDATE
from src.internal.biz.deserializers.place_types import PlaceTypesDeserializer, DES_PLACE_TYPES_ADD, \
    DES_PLACE_TYPES_UPDATE
from src.internal.biz.deserializers.place_work_hours_week import PlaceWorkHoursWeekDeserializer, \
    DES_WORK_HOURS_WEEK_ADD, DES_WORK_HOURS_WEEK_UPDATE
from src.internal.biz.deserializers.services import ServicesDeserializer, DES_SERVICES_ADD, DES_SERVICES_UPDATE
from src.internal.biz.deserializers.utils import filter_keys_by_substr
from src.internal.biz.entities.place_common import PlaceCommon

DES_PLACE_COMMON_ADD = 'place-common-add'
DES_PLACE_COMMON_UPDATE = 'place_common-update'
DES_PLACE_COMMON_FROM_DB_FULL = 'place-common-from-db-full'

PLACE_COMMON = 'plc_'


class PlaceCommonDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_ser: str):
        if format_ser == DES_PLACE_COMMON_ADD:
            return cls._deserializer_add
        elif format_ser == DES_PLACE_COMMON_FROM_DB_FULL:
            return cls._deserialize_from_db_full
        elif format_ser == DES_PLACE_COMMON_UPDATE:
            return cls._deserializer_update
        else:
            raise TypeError

    @staticmethod
    def _deserializer_add(place_common: dict) -> PlaceCommon:
        return PlaceCommon(
            place_main=PlaceMainDeserializer.deserialize(place_common, DES_PLACE_MAIN_ADD),
            place_contacts=PlaceContactsDeserializer.deserialize(place_common['contacts'] if place_common.get('contacts') else {}, DES_FROM_DICT),
            place_cuisine_types=CuisineTypesDeserializer.deserialize(place_common['cuisine_types_ids'] if place_common.get('cuisine_types_ids') else [], DES_CUISINE_TYPES_ADD),
            place_places_types=PlaceTypesDeserializer.deserialize(place_common['place_types_ids'] if place_common.get('place_types_ids') else [], DES_PLACE_TYPES_ADD),
            place_services=ServicesDeserializer.deserialize(place_common['services_ids'] if place_common.get('services_ids') else [], DES_SERVICES_ADD),
            place_locations=PlaceLocationsDeserializer.deserialize(place_common['locations'] if place_common.get('locations') else [], DES_PLACE_LOCATIONS_ADD),
            place_work_hours=PlaceWorkHoursWeekDeserializer.deserialize(place_common['work_hours'] if place_common.get('work_hours') else {}, DES_WORK_HOURS_WEEK_ADD)
        )

    @staticmethod
    def _deserialize_from_db_full(place_common: Union[dict, Record]) -> PlaceCommon:
        place_main = filter_keys_by_substr(place_common, PLACE_MAIN)
        place_location = filter_keys_by_substr(place_common, PLACE_LOCATION)
        place_contacts = filter_keys_by_substr(place_common, PLACE_CONTACTS)
        return PlaceCommon(
            place_main=PlaceMainDeserializer.deserialize(place_main, DES_PLACE_MAIN_FROM_DB_FULL),
            place_contacts=PlaceContactsDeserializer.deserialize(place_contacts, DES_PLACE_CONTACTS_FROM_DB_FULL),
            place_location=PlaceLocationDeserializer.deserialize(place_location, DES_PLACE_LOCATION_FROM_DB_FULL)
        )

    @staticmethod
    def _deserializer_update(place_common: dict) -> PlaceCommon:
        return PlaceCommon(
            place_main=PlaceMainDeserializer.deserialize(place_common, DES_PLACE_MAIN_UPDATE),
            place_contacts=PlaceContactsDeserializer.deserialize(place_common['contacts'] if place_common.get('contacts') else {}, DES_FROM_DICT),
            place_cuisine_types=CuisineTypesDeserializer.deserialize(place_common['cuisine_types_ids'] if place_common.get('cuisine_types_ids') else [], DES_CUISINE_TYPES_UPDATE),
            place_places_types=PlaceTypesDeserializer.deserialize(place_common['place_types_ids'] if 'place_types_ids' in place_common.keys() else [], DES_PLACE_TYPES_UPDATE),
            place_services=ServicesDeserializer.deserialize(place_common['services_ids'] if'services_ids' in place_common.keys() else [], DES_SERVICES_UPDATE),
            place_location=PlaceLocationDeserializer.deserialize(place_common['location'] if place_common.get('location') else {}, DES_PLACE_LOCATIONS_UPDATE),
            place_work_hours=PlaceWorkHoursWeekDeserializer.deserialize(place_common['work_hours'] if place_common.get('work_hours') else {}, DES_WORK_HOURS_WEEK_UPDATE)
        )
