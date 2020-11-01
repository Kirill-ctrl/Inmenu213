from typing import Tuple, Optional, List

import asyncpg

from src.internal.adapters.entities.error import Error
from src.internal.adapters.enums.errors import ErrorEnum
from src.internal.biz.dao.base_dao import BaseDao
from src.internal.biz.entities.cuisine_type import CuisineType
from src.internal.biz.entities.place_cuisine_type import PlaceCuisineType
from src.internal.biz.entities.place_main import PlaceMain

CUISINE_TYPE_FOREIGN_TYPE = 'place_cuisine_type_cuisine_type_id_fkey'


class PlaceCuisineTypeDao(BaseDao):

    async def add_many(self, place_cuisine_types: List[PlaceCuisineType]) -> Tuple[None, Optional[Error]]:
        sql = """
            INSERT INTO place_cuisine_type(place_main_id, cuisine_type_id) VALUES
        """

        inserted_values = []
        for place_cuisine_type, i in list(zip(place_cuisine_types, range(1, len(place_cuisine_types) * 2, 2))):
            sql += ', ' if len(inserted_values) != 0 else ''
            sql += f'(${i}, ${i + 1})'
            inserted_values.append(place_cuisine_type.place_main.id)
            inserted_values.append(place_cuisine_type.cuisine_type.id)

        if inserted_values:
            try:
                await self.conn.execute(sql, *inserted_values)
            except asyncpg.exceptions.ForeignKeyViolationError as exc:
                if exc.constraint_name == CUISINE_TYPE_FOREIGN_TYPE:
                    return None, ErrorEnum.WRONG_CUISINE_TYPE
                else:
                    raise TypeError

        return None, None

    async def get_by_main_ids(self, place_main_ids: List[int], lang_id: int) -> Tuple[Optional[List[PlaceCuisineType]], Optional[Error]]:
        async with self.pool.acquire() as conn:
            sql = """
                SELECT
                    place_cuisine_type.place_main_id,
                    place_cuisine_type.cuisine_type_id,
                    cuisine_type_translate.name
                FROM
                    place_cuisine_type
                    INNER JOIN cuisine_type_translate ON (place_cuisine_type.cuisine_type_id = cuisine_type_translate.cuisine_type_id AND cuisine_type_translate.language_id = $2)
                WHERE
                    place_cuisine_type.place_main_id = ANY($1)
            """

            rows = await conn.fetch(sql, place_main_ids, lang_id)
            return [PlaceCuisineType(place_main=PlaceMain(id=row['place_main_id']), cuisine_type=CuisineType(id=row['cuisine_type_id'], name=row['name'])) for row in rows], None

    async def get_place_main_id_place_cuisine_type_id(self, place_main_id: int):
        sql = """
            SELECT place_main_id, cuisine_type_id
            FROM place_cuisine_type
            WHERE place_main_id = $1
        """
        data = await self.conn.fetch(sql, place_main_id)
        return data

    async def update_cuisine_type(self, place_main_id: int, place_cuisine_types: List[PlaceCuisineType], arr: List[Tuple]):
        sql = """"""
        temp_sql = 'UPDATE place_cuisine_type SET cuisine_type_id = CASE WHEN '
        for i in range(len(place_cuisine_types)):
            sql += temp_sql + f'{place_cuisine_types[i].cuisine_type.id if place_cuisine_types[i].cuisine_type.id else None}::int IS NOT NULL THEN ' + \
                   f'{place_cuisine_types[i].cuisine_type.id if place_cuisine_types[i].cuisine_type.id else None}::int ELSE cuisine_type_id END ' + \
                   'WHERE (place_main_id, cuisine_type_id) = ' + f'({arr[i][0]}, {arr[i][1]}); '
        print(sql)
        try:
            await self.conn.execute(sql)
        except asyncpg.exceptions.ForeignKeyViolationError as exc:
            if exc.constraint_name == CUISINE_TYPE_FOREIGN_TYPE:
                return None, ErrorEnum.WRONG_CUISINE_TYPE
            else:
                raise TypeError

        return None, None
