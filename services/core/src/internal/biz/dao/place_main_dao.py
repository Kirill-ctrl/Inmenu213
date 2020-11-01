from typing import Tuple, Optional, List

import asyncpg

from src.internal.adapters.entities.error import Error
from src.internal.adapters.enums.errors import ErrorEnum
from src.internal.biz.dao.base_dao import BaseDao
from src.internal.biz.deserializers.photo import PHOTO_SHORT_URL
from src.internal.biz.deserializers.place_main import PlaceMainDeserializer, DES_PLACE_MAIN_FROM_DB_FULL, PLACE_MAIN_ID, \
    PLACE_MAIN_NAME, PLACE_MAIN
from src.internal.biz.entities.account_main import AccountMain
from src.internal.biz.entities.place_main import PlaceMain


UNIQUE_PLACE_LOGIN = 'unique_place_login'
LANGUAGE_FOREIGN_KEY = 'place_main_main_language_fkey'
CURRENCY_FOREIGN_KEY = 'place_main_main_currency_fkey'


class PlaceMainDao(BaseDao):

    async def add(self, place_main: PlaceMain) -> Tuple[Optional[PlaceMain], Optional[Error]]:

        sql = """
            INSERT INTO place_main(account_main_id, main_language, name, login, photo_link, description, main_currency, is_draft, is_published)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id
        """

        try:
            place_main_id = await self.conn.fetchval(
                sql, place_main.account_main.id, place_main.main_language.id, place_main.name, place_main.login, place_main.photo.short_url,
                place_main.description, place_main.main_currency.id, place_main.is_draft, place_main.is_published
            )
        except asyncpg.exceptions.UniqueViolationError as exc:
            if exc.constraint_name == UNIQUE_PLACE_LOGIN:
                return None, ErrorEnum.NOT_UNIQUE_PLACE_LOGIN
            else:
                raise TypeError
        except asyncpg.exceptions.ForeignKeyViolationError as exc:
            if exc.constraint_name == LANGUAGE_FOREIGN_KEY:
                return None, ErrorEnum.WRONG_LANGUAGE
            if exc.constraint_name == CURRENCY_FOREIGN_KEY:
                return None, ErrorEnum.WRONG_CURRENCY
            else:
                raise TypeError

        place_main.id = place_main_id
        return place_main, None

    async def get_place_owner(self, place_main_id: int) -> Tuple[Optional[AccountMain], Optional[Error]]:
        async with self.pool.acquire() as conn:
            account_main_id = await conn.fetchval(
                """
                SELECT account_main_id
                FROM place_main
                WHERE id = $1
                """, place_main_id
            )
            if not account_main_id:
                return None, None

            return AccountMain(id=account_main_id), None

    async def get_all_places(self, city: Optional[str], pagination_size: int, pagination_after: int) -> Tuple[Optional[List[PlaceMain]], Optional[Error]]:
        async with self.pool.acquire() as conn:
            sql = f"""
                SELECT
                    place_main.id           AS {PLACE_MAIN_ID},
                    place_main.name         AS {PLACE_MAIN_NAME},
                    place_main.photo_link   AS {PLACE_MAIN + PHOTO_SHORT_URL}
                FROM
                    place_main
                    INNER JOIN place_location ON place_main.id = place_location.place_main_id
                WHERE
                    place_main.is_published = TRUE
            """
            inserted_values = []

            if city:
                sql += ' WHERE ' if not inserted_values else ' AND '
                sql += f'city = ${len(inserted_values) + 1}'
                inserted_values.append(city)

            sql += f"""
            LIMIT ${len(inserted_values) + 1} OFFSET ${len(inserted_values) + 2}
            """
            inserted_values.append(pagination_size)
            inserted_values.append(pagination_after)

            rows = await conn.fetch(sql, *inserted_values)
            if not rows:
                return [], None

            return [PlaceMainDeserializer.deserialize(row, DES_PLACE_MAIN_FROM_DB_FULL) for row in rows], None

    async def get_places_by_name(self, city_name: Optional[str], place_name: str, pagination_size: int, pagination_after: int) -> Tuple[Optional[List[PlaceMain]], Optional[Error]]:
        async with self.pool.acquire() as conn:
            sql = f"""
                SELECT
                    place_main.id           AS {PLACE_MAIN_ID},
                    place_main.name         AS {PLACE_MAIN_NAME},
                    place_main.photo_link   AS {PLACE_MAIN + PHOTO_SHORT_URL}
                FROM
                    place_main
                    INNER JOIN place_location ON place_main.id = place_location.place_main_id
                WHERE
                    place_main.is_published = TRUE AND
                    position($1 in lower(place_main.name)) <> 0
            """
            inserted_values = [place_name]

            if city_name:
                sql += f' AND city = ${len(inserted_values) + 1}'
                inserted_values.append(city_name)

            sql += f"""
                LIMIT ${len(inserted_values) + 1} OFFSET ${len(inserted_values) + 2}
            """
            inserted_values.append(pagination_size)
            inserted_values.append(pagination_after)

            rows = await conn.fetch(sql, *inserted_values)
            if not rows:
                return [], None

            return [PlaceMainDeserializer.deserialize(row, DES_PLACE_MAIN_FROM_DB_FULL) for row in rows], None

    async def get_places_by_account_main_id(self, account_main_id: int, pagination_size: int, pagination_after: int) -> Tuple[Optional[List[PlaceMain]], Optional[Error]]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(f"""
                SELECT
                    place_main.id           AS {PLACE_MAIN_ID},
                    place_main.name         AS {PLACE_MAIN_NAME},
                    place_main.photo_link   AS {PLACE_MAIN + PHOTO_SHORT_URL}
                FROM
                    place_main
                WHERE
                    place_main.account_main_id = $1
                LIMIT $2 OFFSET $3
            """, account_main_id, pagination_size, pagination_after)

            return [PlaceMainDeserializer.deserialize(row, DES_PLACE_MAIN_FROM_DB_FULL) for row in rows], None

    async def del_by_place_main_id(self, place_main_id: int) -> Tuple[Optional[bool], Optional[Error]]:
        sql = """
            DELETE FROM place_main
            WHERE place_main.id = $1
            RETURNING place_main.id
        """
        try:
            async with self.pool.acquire() as conn:
                value = await conn.fetchval(sql, place_main_id)
        except:
            raise TypeError

        if not value:
            return None, ErrorEnum.PLACE_DOESNT_EXISTS

        return True, None

    async def update(self, place_main_id: int, place_main: PlaceMain) -> Tuple[Optional[PlaceMain], Optional[Error]]:
        sql = """
            UPDATE
                place_main
            SET
                main_language = CASE WHEN $1::int != 0 THEN $1::int WHEN $1::int = 0 THEN NULL::int WHEN $1::int IS NULL THEN main_language END,
                name = CASE WHEN $2::varchar != '0' THEN $2::varchar WHEN $2::varchar = '0' THEN NULL WHEN $2::varchar IS NULL THEN name END,
                description = CASE WHEN $3::varchar != '0' THEN $3::varchar WHEN $3::varchar = '0' THEN NULL WHEN $3::varchar IS NULL THEN description END,
                login = CASE WHEN $4::varchar != '0' THEN $4::varchar WHEN $4::varchar = '0' THEN NULL WHEN $4::varchar IS NULL THEN login END,
                photo_link = CASE WHEN $5::varchar != '0' THEN $5::varchar WHEN $5::varchar = '0' THEN NULL WHEN $5::varchar IS NULL THEN photo_link END,
                main_currency_id = CASE WHEN $6::int != 0 THEN $6::int WHEN $6::int = 0 THEN NULL::int WHEN $6::int IS NULL THEN main_currency_id END
            WHERE place_main.id = $7
            RETURNING id
        """
        try:
            place_main__id = await self.conn.fetchval(sql, place_main.main_language.id if place_main.main_language else None,
                                                     place_main.name if place_main.name else None,
                                                     place_main.description if place_main.description else None,
                                                     place_main.login if place_main.login else None,
                                                     place_main.photo.short_url if place_main.photo else None,
                                                     place_main.main_currency.id if place_main.main_currency else None,
                                                     place_main_id)
        except asyncpg.exceptions.UniqueViolationError as exc:
            if exc.constraint_name == UNIQUE_PLACE_LOGIN:
                return None, ErrorEnum.NOT_UNIQUE_PLACE_LOGIN
            else:
                raise TypeError
        except asyncpg.exceptions.ForeignKeyViolationError as exc:
            if exc.constraint_name == LANGUAGE_FOREIGN_KEY:
                return None, ErrorEnum.WRONG_LANGUAGE
            else:
                raise TypeError

        place_main.id = place_main_id
        return place_main, None
