from typing import Tuple, Optional

from src.internal.adapters.entities.error import Error
from src.internal.adapters.enums.errors import ErrorEnum
from src.internal.biz.dao.dish_common_dao import DishCommonDao
from src.internal.biz.dao.menu_category import MenuCategoryDao
from src.internal.biz.dao.menu_main import MenuMainDao
from src.internal.biz.dao.place_account_role import PlaceAccountRoleDao
from src.internal.biz.dao.place_main_dao import PlaceMainDao
from src.internal.biz.entities.dish_common import DishCommon
from src.internal.biz.entities.menu_category import MenuCategory
from src.internal.biz.entities.menu_main import MenuMain
from src.internal.biz.services.base_service import BaseService
from src.internal.biz.entities.menu_common import MenuCommon
from src.internal.biz.entities.dish_main import DishMain
from src.internal.biz.entities.dish_measure import DishMeasure
from src.internal.biz.entities.language import Language
from src.internal.biz.serializers.menu_serializers import MenuSerializer



class MenuService(BaseService):

    @staticmethod
    async def add_menu(menu: MenuMain, auth_account_main_id: int) -> Tuple[Optional[MenuMain], Optional[Error]]:

        account_main, err = await PlaceMainDao().get_place_owner(menu.place_main.id)
        if err:
            return None, err

        if not account_main:
            return None, ErrorEnum.PLACE_DOESNT_EXISTS

        if account_main.id != auth_account_main_id:
            return None, ErrorEnum.PLACE_FORBIDDEN

        menu_main, err = await MenuMainDao().add(menu)
        if err:
            return None, err

        return menu, None

    @staticmethod
    async def add_menu_category(menu_category: MenuCategory, auth_account_main_id: int):
        place_account_role, err = await PlaceAccountRoleDao().get_by_menu_main_id(menu_category.menu_main.id, auth_account_main_id)
        if err:
            return None, err

        if not place_account_role or place_account_role.account_status.id not in (1, 2):
            return None, ErrorEnum.PLACE_FORBIDDEN

        menu_category, err = await MenuCategoryDao().add(menu_category)
        if err:
            return None, err

        return menu_category, None

    @staticmethod
    async def add_dish(dish_common: DishCommon, auth_account_main_id: int):
        place_account_role, err = await PlaceAccountRoleDao().get_by_menu_main_id(dish_common.dish_main.menu_main.id, auth_account_main_id)
        if err:
            return None, err

        if not place_account_role or place_account_role.account_status.id not in (1, 2):
            return None, ErrorEnum.PLACE_FORBIDDEN

        dish_common, err = await DishCommonDao().add(dish_common)
        if err:
            return None, err

        return dish_common, err


    @staticmethod
    async def get_menu(menu_id: int):
        menu, err = MenuMainDao().get(menu_id)
        if err:
            return None, err

        menu_common = MenuCommon(
            menu_main=MenuMain(
                id=menu['menu_main.id'],
                name=menu['menu_main.name'],
                photo=menu['menu_main.photo_link']
            ),
            dish_main=DishMain(
                name=menu['dish_main.name'],
                photo=menu['dish_main.photo_link'],
                description=menu['dish_main.description']
            ),
            dish_measures=list(DishMeasure(
                price_value=menu['dish_measure.price_value'],
                measure_value=menu['dish_measure.measure_value']
            )),
            menu_category=list(MenuCategory(
                name=menu['menu_category.name']
            )),
            language=Language(
                name=menu['place_main.main_language']
            )
        )
