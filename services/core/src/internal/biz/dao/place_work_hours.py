from datetime import time
from typing import List, Tuple, Optional

import asyncpg

from src.internal.adapters.entities.error import Error
from src.internal.adapters.enums.errors import ErrorEnum
from src.internal.biz.dao.base_dao import BaseDao
from src.internal.biz.entities.place_work_hours import PlaceWorkHours


class PlaceWorkHoursDao(BaseDao):

    async def add_many(self, place_work_hours_list: List[PlaceWorkHours]) -> Tuple[None, Optional[Error]]:
        sql = """
            INSERT INTO place_work_hours(place_main_id, week_day, time_start, time_finish, is_holiday) VALUES
        """

        inserted_values = []
        for place_work_hours, i in list(zip(place_work_hours_list, range(1, len(place_work_hours_list) * 5, 5))):
            sql += ', ' if len(inserted_values) != 0 else ''
            sql += f'(${i}, ${i + 1}, ${i + 2}, ${i + 3}, ${i + 4})'
            inserted_values.append(place_work_hours.place_main.id)
            inserted_values.append(place_work_hours.week_day)
            inserted_values.append(place_work_hours.time_start)
            inserted_values.append(place_work_hours.time_finish)
            inserted_values.append(place_work_hours.is_holiday)

        if inserted_values:
            await self.conn.execute(sql, *inserted_values)

        return None, None

    async def get_by_place_main_id(self, place_main_id):
        sql = """
            SELECT 
                place_main_id, week_day, time_start, time_finish, is_holiday
            FROM
                place_work_hours
            WHERE place_main_id = $1 
        """
        data = await self.conn.fetch(sql, place_main_id)
        return data

    async def update_work_hours(self, place_main_id, place_work_hours_list: List[PlaceWorkHours], arr: List[Tuple]):
        sql = """"""
        update_values = []
        for place_work_hours, i in list(zip(place_work_hours_list, range(1, len(place_work_hours_list) * 5, 5))):
            sql += '; ' if len(update_values) != 0 else ''
            sql += f" UPDATE place_work_hours SET time_start = CASE WHEN ${i} IS NOT NULL THEN ${i} ELSE NULL END, " \
                   f"time_finish = CASE WHEN ${i+1} IS NOT NULL THEN ${i+1} ELSE NULL END, " \
                   f"is_holiday = CASE WHEN ${i + 2} IS NOT NULL THEN ${i + 3} ELSE NULL END " \
                   f"WHERE place_main_id = ${i + 3} AND week_day = ${i + 4} "
            update_values.append(place_work_hours.time_start)
            update_values.append(place_work_hours.time_finish)
            update_values.append(place_work_hours.is_holiday)
            update_values.append(place_work_hours.place_main.id)
            update_values.append(place_work_hours.week_day)
        if update_values:
            await self.conn.fetchval(sql, *update_values)
        return None, None
