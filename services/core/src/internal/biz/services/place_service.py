from typing import Optional, Tuple, List

from src.internal.adapters.entities.error import Error
from src.internal.adapters.enums.errors import ErrorEnum
from src.internal.biz.dao.place_account_role import PlaceAccountRoleDao
from src.internal.biz.dao.place_common import PlaceCommonDao
from src.internal.biz.dao.place_cuisine_type_dao import PlaceCuisineTypeDao
from src.internal.biz.dao.place_location import PlaceLocationDao
from src.internal.biz.dao.place_main_dao import PlaceMainDao
from src.internal.biz.dao.place_place_type import PlacePlaceTypeDao
from src.internal.biz.dao.place_service_dao import PlaceServiceDao
from src.internal.biz.entities.place_common import PlaceCommon
from src.internal.biz.entities.place_location import PlaceLocation
from src.internal.biz.entities.place_main import PlaceMain
from src.internal.biz.services.base_service import BaseService
from src.internal.biz.services.utils import get_radius


class PlaceService(BaseService):

    @staticmethod
    async def add_place(place_common: PlaceCommon) -> Tuple[Optional[PlaceCommon], Optional[Error]]:
        place_common, err = await PlaceCommonDao().add(place_common)
        if err:
            return None, err

        return place_common, None

    @classmethod
    async def get_all_places(cls, city_name: Optional[str], pagination_size: int, pagination_after: int, lang_id: int) -> Tuple[Optional[List[PlaceCommon]], Optional[Error]]:
        place_mains, err = await PlaceMainDao().get_all_places(city_name, pagination_size, pagination_after)
        if err:
            return None, err

        place_commons, err = await cls._get_place_commons_with_place_cuisine_types_by_place_mains(place_mains, lang_id)
        if err:
            return None, err

        return place_commons, None

    @classmethod
    async def get_places_by_name(cls, city_name: Optional[str], place_name: str, pagination_size: int, pagination_after: int, lang_id: int) -> Tuple[Optional[List[PlaceCommon]], Optional[Error]]:
        place_mains, err = await PlaceMainDao().get_places_by_name(city_name, place_name, pagination_size, pagination_after)
        if err:
            return None, err

        place_commons, err = await cls._get_place_commons_with_place_cuisine_types_by_place_mains(place_mains, lang_id)
        if err:
            return None, err

        return place_commons, None

    @staticmethod
    def _get_place_commons_by_place_main_and_place_cuisine_types(place_mains: List[PlaceMain], place_cuisine_types) -> List[PlaceCommon]:
        return [PlaceCommon(
            place_main=place_main,
            place_cuisine_types=[place_cuisine_type
                                 for place_cuisine_type in place_cuisine_types if
                                 place_cuisine_type.place_main.id == place_main.id])
                for place_main in place_mains]

    @classmethod
    async def _get_place_commons_with_place_cuisine_types_by_place_mains(cls, place_mains: List[PlaceMain], lang_id: int) -> Tuple[Optional[List[PlaceCommon]], Optional[Error]]:
        place_main_ids = [place_main.id for place_main in place_mains]

        place_cuisine_types, err = await PlaceCuisineTypeDao().get_by_main_ids(place_main_ids, lang_id)
        if err:
            return None, err

        place_commons = cls._get_place_commons_by_place_main_and_place_cuisine_types(place_mains, place_cuisine_types)

        return place_commons, None

    @staticmethod
    async def get_locations_with_places() -> Tuple[Optional[List[PlaceLocation]], Optional[Error]]:
        place_locations, err = await PlaceLocationDao().get_all_distinct()
        if err:
            return None, err

        return place_locations, None

    @staticmethod
    async def get_place_location_on_map(center_point_list: List[float], radius_point_list: List[float]) -> Tuple[Optional[List[PlaceLocation]], Optional[Error]]:
        radius = get_radius(center_point_list, radius_point_list)
        place_locations, err = await PlaceLocationDao().get_place_locations_on_map(center_point_list, radius)
        if err:
            return None, err

        return place_locations, None

    @staticmethod
    async def get_place_by_location_id(place_location_id: int, lang_id: int) -> Tuple[Optional[PlaceCommon], Optional[Error]]:
        place_common, err = await PlaceCommonDao().get_by_location_id(place_location_id)
        if err:
            return None, err

        if not place_common:
            return None, ErrorEnum.NOT_FOUND

        place_place_types, err = await PlacePlaceTypeDao().get_by_place_main_id(place_common.place_main.id, lang_id)
        if err:
            return None, err

        place_services, err = await PlaceServiceDao().get_by_place_main_id(place_common.place_main.id, lang_id)
        if err:
            return None, err

        place_common.place_places_types = place_place_types
        place_common.place_services = place_services

        return place_common, err

    @staticmethod
    async def get_places_by_account_main_id(account_main_id: int, pagination_size: int, pagination_after: int) -> Tuple[Optional[List[PlaceMain]], Optional[Error]]:
        place_mains, err = await PlaceMainDao().get_places_by_account_main_id(account_main_id, pagination_size, pagination_after)
        if err:
            return None, err

        return place_mains, err

    @staticmethod
    async def del_place(place_main_id: int) -> Tuple[Optional[bool], Optional[Error]]:
        response_place_main, err = await PlaceMainDao().del_by_place_main_id(place_main_id)
        if err:
            return False, err

        return True, None

    @staticmethod
    async def update_place(place_main_id: int, place_common: PlaceCommon) -> Tuple[Optional[PlaceCommon], Optional[Error]]:
        place_common, err = await PlaceCommonDao().update(place_main_id, place_common)
        if err:
            return None, err

        return place_common, None
