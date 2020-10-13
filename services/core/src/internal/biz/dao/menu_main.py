from typing import Tuple, Optional

import asyncpg

from src.internal.adapters.entities.error import Error
from src.internal.adapters.enums.errors import ErrorEnum
from src.internal.biz.dao.base_dao import BaseDao
from src.internal.biz.entities.menu_main import MenuMain


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
                menu_id = await self.conn.fetchval(sql, menu_main.place_main.id, menu_main.name, menu_main.photo.short_url)
            else:
                async with self.pool.acquire() as conn:
                    menu_id = await conn.fetchval(sql, menu_main.place_main.id, menu_main.name, menu_main.photo.short_url)
        except asyncpg.exceptions.ForeignKeyViolationError as exc:
            if exc.constraint_name == MENU_PLACE_MAIN_FKEY:
                return None, ErrorEnum.PLACE_DOESNT_EXISTS
            else:
                raise TypeError
        except Exception as exc:
            raise TypeError

        menu_main.id = menu_id
        return menu_main, None

        menu_common = MenuCommon(
            menu_main=MenuMain(

            )
        )

    async def get(self, menu_id: int) -> Tuple[Optional[MenuMain], Optional[Error]]:
        sql = """
            SELECT 
                place_main.main_language,
                menu_main.id,
                menu_main.name,
                menu_main.photo_link,
                menu_category.id,
                menu_category.name,
                measure_unit.name,
                dish_main.name,
                dish_main.photo_link,
                dish_main.description,
                dish_measure.price_value,
                dish_measure.measure_value,
            FROM
                menu_main
            INNER JOIN
                    place_main ON place_main.id = menu_main.place_main_id
            INNER JOIN
                    dish_main ON menu_main.id = dish_main.menu_main_id
            INNER JOIN
                    dish_measure ON dish_main.id = dish_measure.dish_main_id
            INNER JOIN 
                    measure_unit ON dish_main.measure_unit_id = measure_unit.id
            INNER JOIN 
                    menu_category ON menu_category.menu_main_id = menu_main.id
            WHERE 
                menu_main.id = $1
        """

        if self.conn:
            menu = await self.conn.fetchrow(sql, menu_id)
        else:
            async with self.pool.acquire() as conn:
                menu = await conn.fetchrow(sql, menu_id)
        if not menu:
            return None, ErrorEnum.MENU_DOESNT_EXISTS
        else:
            print(menu)
            return menu, None

