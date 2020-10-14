from typing import Tuple, Optional

import asyncpg

from src.internal.adapters.entities.error import Error
from src.internal.adapters.enums.errors import ErrorEnum
from src.internal.biz.dao.base_dao import BaseDao
from src.internal.biz.entities.menu_main import MenuMain
from src.internal.biz.entities.menu_common import MenuCommon
from src.internal.biz.entities.dish_main import DishMain
from src.internal.biz.entities.dish_measure import DishMeasure
from src.internal.biz.entities.language import Language
from src.internal.biz.entities.currency import Currency
from src.internal.biz.entities.menu_category import MenuCategory
from src.internal.biz.entities.measure_unit import MeasureUnit

MENU_PLACE_MAIN_FKEY = 'menu-place-main-fkey'


class MenuMainDao(BaseDao):

    async def add(self, menu_main: MenuMain) -> Tuple[Optional[MenuMain], Optional[Error]]:
        sql = """
            INSERT INTO menu_main(place_main_id, name, photo_link) VALUES
            ($1, $2, $3)
            RETURNING id;
        """

        try:
            if self.conn:
                menu_id = await self.conn.fetchval(sql, menu_main.place_main.id, menu_main.name,
                                                   menu_main.photo.short_url)
            else:
                async with self.pool.acquire() as conn:
                    menu_id = await conn.fetchval(sql, menu_main.place_main.id, menu_main.name,
                                                  menu_main.photo.short_url)
        except asyncpg.exceptions.ForeignKeyViolationError as exc:
            if exc.constraint_name == MENU_PLACE_MAIN_FKEY:
                return None, ErrorEnum.PLACE_DOESNT_EXISTS
            else:
                raise TypeError
        except Exception as exc:
            raise TypeError

        menu_main.id = menu_id
        return menu_main, None

        # menu_common = MenuCommon(
        #     menu_main=MenuMain(
        #
        #     )
        # )

    async def get(self, menu_id: int) -> Tuple[Optional[MenuCommon], Optional[Error]]:
        sql = """
                SELECT
                    menu_main.id                        AS menu_main_id,
                    menu_main.name                      AS menu_main_name,
                    menu_main.photo_link                AS menu_main_photo_link,
                    language.id                         AS language_id,
                    language.name                       AS language_name,
                    menu_category.id                    AS menu_category_id,
                    menu_category.name                  AS menu_category_name,
                    measure_unit.id                     AS measure_unit_id,
                    measure_unit.short_name             AS measure_unit_short_name,
                    dish_main.id                        AS dish_main_id,
                    dish_main.name                      AS dish_main_name,
                    dish_main.photo_link                AS dish_main_photo_link,
                    dish_main.description               AS dish_main_description,
                    dish_measure.id                     AS dish_measure_id,
                    dish_measure.price_value            AS dish_measure_price_value,
                    dish_measure.measure_value          AS dish_measure_measure_value,
                    currency.id                         AS currency_id,
                    currency.sign                       AS currency_sign
                FROM
                        place_main
                INNER JOIN 
                        menu_main ON place_main.id = menu_main.place_main_id
                INNER JOIN
                        account_main ON place_main.account_main_id = account_main.id
                INNER JOIN
                        language ON language.id = place_main.main_language
                INNER JOIN
                        menu_category ON menu_category.menu_main_id = menu_main.id
                INNER JOIN
                        dish_main ON dish_main.menu_category_id = menu_category.id AND dish_main.menu_main_id = menu_main.id
                INNER JOIN
                        measure_unit ON dish_main.measure_unit_id = measure_unit.id
                INNER JOIN 
                        dish_measure ON dish_measure.dish_main_id = dish_main.id
                INNER JOIN
                        currency ON place_main.main_currency = currency.id
                WHERE 
                        menu_main.id = $1
                ORDER BY 
                        dish_main_id
            """
        if self.conn:
            menu = await self.conn.fetch(sql, menu_id)
        else:
            async with self.pool.acquire() as conn:
                menu = await conn.fetch(sql, menu_id)
        if not menu:
            return None, ErrorEnum.MENU_DOESNT_EXISTS
        menu_common = MenuCommon(
            main_menu=MenuMain(
                id=menu[0]['menu_main_id'],
                name=menu[0]['menu_main_name'],
                photo=menu[0]['menu_main_photo_link']
            ),
            language=Language(
                id=menu[0]['language_id'],
                name=menu[0]['language_name']
            ),
            menu_category=[
                MenuCategory(
                            id=menu[i]['menu_category_id'],
                            name=menu[i]['menu_category_name']
                            ) for i in range(len(menu))],
            measure_unit=[
                MeasureUnit(
                            id=menu[i]['measure_unit_id'],
                            name=menu[i]['measure_unit_short_name']
                           ) for i in range(len(menu))],
            dish_main=[
                DishMain(
                        id=menu[i]['dish_main_id'],
                        name=menu[i]['dish_main_name'],
                        photo=menu[i]['dish_main_photo_link'],
                        description=menu[i]['dish_main_description']
                        )for i in range(len(menu))],
            dish_measures=[
                DishMeasure(
                            id=menu[i]['dish_measure_id'],
                            price_value=menu[i]['dish_measure_price_value'],
                            measure_value=menu[i]['dish_measure_measure_value']
                            ) for i in range(len(menu))],
            currency=Currency(
                id=menu[0]['currency_id'],
                sign=menu[0]['currency_sign']
            )
        )
        return menu_common, None
