from typing import List, Tuple, Optional

import asyncpg

from src.internal.adapters.entities.error import Error
from src.internal.adapters.enums.errors import ErrorEnum
from src.internal.biz.dao.base_dao import BaseDao
from src.internal.biz.deserializers.place_service import PlaceServiceDeserializer, DES_PLACE_SERVICE_FROM_DB_FULL, \
    PLACE_SERVICE
from src.internal.biz.deserializers.service import SERVICE_ID, SERVICE_NAME
from src.internal.biz.entities.place_service import PlaceService


SERVICE_FOREIGN_KEY = 'place_service_service_id_fkey'
UNIQUE_PLACE_SERVICE = 'unique_place_service'


class PlaceServiceDao(BaseDao):

    async def add_many(self, place_services: List[PlaceService]) -> Tuple[None, Optional[Error]]:
        sql = """
            INSERT INTO place_service(place_main_id, service_id) VALUES
        """

        inserted_values = []
        for place_service, i in list(zip(place_services, range(1, len(place_services) * 2, 2))):
            sql += ', ' if len(inserted_values) != 0 else ''
            sql += f'(${i}, ${i + 1})'
            inserted_values.append(place_service.place_main.id)
            inserted_values.append(place_service.service.id)

        if inserted_values:
            try:
                await self.conn.execute(sql, *inserted_values)
            except asyncpg.exceptions.ForeignKeyViolationError as exc:
                if exc.constraint_name == SERVICE_FOREIGN_KEY:
                    return None, ErrorEnum.WRONG_SERVICE
                else:
                    raise TypeError

        return None, None

    async def get_by_place_main_id(self, place_main_id: int, lang_id: int) -> Tuple[Optional[List[PlaceService]], Optional[Error]]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(f"""
                SELECT
                    service.id              AS {SERVICE_ID},
                    service_translate.name  AS {SERVICE_NAME}
                FROM
                    place_service
                    INNER JOIN service ON place_service.service_id = service.id
                    INNER JOIN service_translate ON service.id = service_translate.service_id AND service_translate.language_id = $2
                WHERE
                    place_service.place_main_id = $1
            """, place_main_id, lang_id)

            return [PlaceServiceDeserializer.deserialize(row, DES_PLACE_SERVICE_FROM_DB_FULL) for row in rows], None

    async def get_place_main_id_place_place_service_id(self, place_main_id: int):
        sql = f"""
            SELECT place_main_id, service_id
            FROM place_service
            WHERE place_main_id = $1
        """
        data = await self.conn.fetch(sql, place_main_id)
        return data

    async def update_place_service(self, place_main_id: int, place_services: List[PlaceService], arr: List[Tuple]):
        sql = """"""
        temp_sql = 'UPDATE place_service SET service_id = CASE WHEN '
        for i in range(len(place_services)):
            sql += temp_sql + f'{place_services[i].service.id if place_services[i].service.id != 0 else None}::int IS NOT NULL THEN ' + \
                   f'{place_services[i].service.id if place_services[i].service.id != 0 else None}::int ELSE service_id END ' \
                   f'WHERE (place_main_id, service_id) = ({arr[i][0]}, {arr[i][1]}); '
        try:
            await self.conn.execute(sql)
        except asyncpg.exceptions.ForeignKeyViolationError as exc:
            if exc.constraint_name == SERVICE_FOREIGN_KEY:
                return None, ErrorEnum.WRONG_SERVICE
            else:
                raise TypeError
        except asyncpg.exceptions.UniqueViolationError as exc:
            if exc.constraint_name == UNIQUE_PLACE_SERVICE:
                return None, ErrorEnum.UNIQUE_PLACE_SERVICE

        return None, None
