from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from src.internal.adapters.entities.utils import get_response_with_validation_errors
from src.internal.biz.deserializers.place_common import PlaceCommonDeserializer, DES_PLACE_COMMON_ADD
from src.internal.biz.entities.account_main import AccountMain
from src.internal.biz.services.place_service import PlaceService
from src.internal.biz.validators.place_add import PlaceAddSchema
from src.internal.servers.http.answers.places import get_response_get_places
from src.internal.servers.http.middlewares.auth import required_auth_with_confirmed_email
from src.internal.servers.http.middlewares.request import get_pagination_params, get_city_name, get_lang_id

places = Blueprint('places', url_prefix='/places')


@places.route('', methods=['POST', 'GET'])
async def add_get_place(request: Request):

    if request.method == 'POST':
        return await add_place(request)
    elif request.method == 'GET':
        return await get_places(request)


@required_auth_with_confirmed_email
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


@get_pagination_params
@get_city_name
@get_lang_id
async def get_places(request: Request, pagination_size: int = None, pagination_after: int = None, city_name: str = None, lang_id: int = None):
    place_commons, err = await PlaceService.get_all_places(city_name, pagination_size, pagination_after, lang_id)
    if err:
        return err.get_response_with_error()

    return get_response_get_places(place_commons)


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
