from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from src.internal.adapters.entities.utils import get_response_with_validation_errors
from src.internal.servers.http.answers.accounts import get_response_menu_detail
from src.internal.biz.deserializers.menu import DES_MENU_ADD, MenuDeserializer
from src.internal.biz.services.menu import MenuService
from src.internal.biz.validators.menu_add import MenuAddSchema
from src.internal.servers.http.middlewares.auth import required_auth_with_confirmed_email

menu = Blueprint('menu', url_prefix='/menu')


@menu.route('', methods=['POST'])
@required_auth_with_confirmed_email
async def add_menu(request: Request, auth_account_main_id: int):
    errors = MenuAddSchema().validate(request.json)
    if errors:
        return get_response_with_validation_errors(errors)

    menu_main = MenuDeserializer.deserialize(request.json, DES_MENU_ADD)
    menu_main, err = await MenuService.add_menu(menu_main, auth_account_main_id)
    if err:
        return err.get_response_with_error()

    return json({'id': menu_main.id})


@menu.route('/<menu_id:int>')
async def get_menu(request: Request, menu_id: int):
    menu_common, err = await MenuService.get_menu(menu_id)
    if err:
        return None
    return get_response_menu_detail(menu_common)
