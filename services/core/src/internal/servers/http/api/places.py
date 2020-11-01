from typing import List, Optional

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from src.internal.adapters.entities.utils import get_response_with_validation_errors
from src.internal.biz.deserializers.place_common import PlaceCommonDeserializer, DES_PLACE_COMMON_ADD, \
    DES_PLACE_COMMON_UPDATE
from src.internal.biz.entities.account_main import AccountMain
from src.internal.biz.services.place_service import PlaceService
from src.internal.biz.validators.patch_place import PlacePatchSchema
from src.internal.biz.validators.place_add import PlaceAddSchema
from src.internal.servers.http.answers.places import get_response_get_places, get_response_get_places_by_name, \
    get_response_get_locations_with_places, get_response_get_place_locations_on_map, \
    get_response_get_place_location_partial_detail, get_response_get_my_places, get_response_del_place
from src.internal.servers.http.middlewares.auth import required_auth
from src.internal.servers.http.middlewares.log import log_request
from src.internal.servers.http.middlewares.request import get_pagination_params, get_city_name, get_lang_id, \
    get_place_name, get_on_map_params
from src.internal.servers.http.middlewares.status import get_status

places = Blueprint('places', url_prefix='/places')


@places.route('', methods=['POST', 'GET'])
async def add_get_place(request: Request):

    if request.method == 'POST':
        return await add_place(request)
    elif request.method == 'GET':
        return await get_places(request)


@log_request
@required_auth
async def add_place(request: Request, auth_account_main_id: int):
    errors = PlaceAddSchema().validate(request.json)
    if errors:
        return get_response_with_validation_errors(errors)

    place_common = PlaceCommonDeserializer.deserialize(request.json, DES_PLACE_COMMON_ADD)
    place_common.place_main.account_main = AccountMain(id=auth_account_main_id)
    place_common, err = await PlaceService.add_place(place_common)
    if err:
        return err.get_response_with_error()

    return json({'id': place_common.place_main.id})


@log_request
@get_pagination_params
@get_city_name
@get_lang_id
async def get_places(request: Request, pagination_size: int = None, pagination_after: int = None, city_name: str = None, lang_id: int = None):
    place_commons, err = await PlaceService.get_all_places(city_name, pagination_size, pagination_after, lang_id)
    if err:
        return err.get_response_with_error()

    return get_response_get_places(place_commons)



@places.route('/byName', methods=['GET'])
@log_request
@get_place_name
@get_city_name
@get_pagination_params
@get_lang_id
async def get_places_by_name(request: Request, place_name: str, city_name: str, pagination_size: int, pagination_after: int, lang_id: int):
    place_commons, err = await PlaceService.get_places_by_name(city_name, place_name, pagination_size, pagination_after, lang_id)
    if err:
        return err.get_response_with_error()

    return get_response_get_places_by_name(place_commons)


@places.route('/cities', methods=['GET'])
async def get_locations_with_places(request: Request):
    place_locations, err = await PlaceService.get_locations_with_places()
    if err:
        return err.get_response_with_error()

    return get_response_get_locations_with_places(place_locations)


@places.route('/onMap', methods=['GET'])
@log_request
@get_on_map_params
async def get_place_locations_on_map(request: Request, center_point_list: Optional[List[float]], radius_point_list: Optional[List[float]]):
    place_locations, err = await PlaceService.get_place_location_on_map(center_point_list, radius_point_list)
    if err:
        return err.get_response_with_error()

    return get_response_get_place_locations_on_map(place_locations)


@places.route('/locations/<place_location_id:int>/partialDetail', methods=['GET'])
@get_lang_id
async def get_place_location_partial_detail(request: Request, place_location_id: int, lang_id: int):
    place_common, err = await PlaceService.get_place_by_location_id(place_location_id, lang_id)
    if err:
        return err.get_response_with_error()

    return get_response_get_place_location_partial_detail(place_common)


@places.route('/my')
@required_auth
@get_pagination_params
async def get_my_places(request: Request, auth_account_main_id: int, pagination_size: int, pagination_after: int):
    place_mains, err = await PlaceService.get_places_by_account_main_id(auth_account_main_id, pagination_size, pagination_after)
    if err:
        return err.get_response_with_error()

    return get_response_get_my_places(place_mains)

# @places.route('/byName', methods=['GET'])
# @get_place_name
# @get_city_name
# @get_pagination_params
# @get_lang_id
# async def get_places_by_name(request: Request, place_name: str, city_name: str, pagination_size: int, pagination_after: int, lang_id: int):
#     place_commons, err = await PlaceService.get_place_by_name(city_name, place_name, pagination_size, pagination_after, lang_id)
#     if err:
#         return err.get_response_with_error()
#
#     return get_response_get_places_by_name(place_commons)


@places.route('/<place_main_id:int>', methods=['DELETE'])
@required_auth
@get_status
async def del_my_place(request: Request, place_main_id: int):

    if request.method == 'DELETE':
        response, err = await PlaceService.del_place(place_main_id)
        if err:
            return err.get_response_with_error()

        return get_response_del_place(response)


@places.route('/<place_main_id:int>', methods=['PATCH'])
# @required_auth
# @get_status
async def update_my_place(request: Request, place_main_id: int, auth_account_main_id: int = 2):
    errors = PlacePatchSchema().validate(request.json)
    if errors:
        return get_response_with_validation_errors(errors)
    place_common = PlaceCommonDeserializer.deserialize(request.json, DES_PLACE_COMMON_UPDATE)
    place_common.place_main.account_main = AccountMain(id=auth_account_main_id)
    place_common, err = await PlaceService.update_place(place_main_id, place_common)
    if err:
        return err.get_response_with_error()

    return json({'id': place_common.place_main.id})
