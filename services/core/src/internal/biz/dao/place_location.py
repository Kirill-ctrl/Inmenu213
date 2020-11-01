from typing import List, Tuple, Optional

from src.internal.adapters.entities.error import Error
from src.internal.biz.dao.base_dao import BaseDao
from src.internal.biz.deserializers.place_location import PLACE_LOCATION_CITY, PLACE_LOCATION_COUNTRY, \
    PLACE_LOCATION_COUNT_PLACES, PlaceLocationDeserializer, DES_PLACE_LOCATION_FROM_DB_FULL, PLACE_LOCATION, \
    PLACE_LOCATION_COORD_LAT, PLACE_LOCATION_COORD_LONG, PLACE_LOCATION_ID
from src.internal.biz.deserializers.place_main import PLACE_MAIN, PLACE_MAIN_ID
from src.internal.biz.entities.place_location import PlaceLocation


class PlaceLocationDao(BaseDao):

    async def add_many(self, place_locations: List[PlaceLocation]) -> Tuple[None, Optional[Error]]:
        sql = """
            INSERT INTO place_location(place_main_id, full_location, coords, city, country) VALUES
        """

        inserted_values = []
        for place_location, i in list(zip(place_locations, range(1, len(place_locations) * 3, 3))):
            sql += ', ' if len(inserted_values) != 0 else ''
            sql += f'(${i}, ${i + 1}, ${i + 2}, ${i + 3}, ${i + 4})'
            inserted_values.append(place_location.place_main.id)
            inserted_values.append(place_location.full_address)
            inserted_values.append(place_location.coords)
            inserted_values.append(place_location.city)
            inserted_values.append(place_location.country)

        if inserted_values:
            await self.conn.execute(sql, *inserted_values)

        return None, None

    async def get_all_distinct(self) -> Tuple[Optional[List[PlaceLocation]], Optional[Error]]:
        async with self.pool.acquire() as conn:
            sql = f"""
                SELECT
                    city        AS {PLACE_LOCATION_CITY},
                    country     AS {PLACE_LOCATION_COUNTRY},
                    COUNT(*)    AS {PLACE_LOCATION_COUNT_PLACES}
                FROM
                    place_location
                    INNER JOIN place_main ON place_location.place_main_id = place_main.id
                WHERE
                    place_main.is_published = TRUE
                GROUP BY
                    city, country
            """

            rows = await conn.fetch(sql)

            if not rows:
                return [], None

            return [PlaceLocationDeserializer.deserialize(row, DES_PLACE_LOCATION_FROM_DB_FULL) for row in rows], None

    async def get_place_locations_on_map(self, center_point_list: List[float], radius: float) -> Tuple[Optional[List[PlaceLocation]], Optional[Error]]:
        async with self.pool.acquire() as conn:
            sql = f"""
                SELECT
                    place_main.id               AS {PLACE_LOCATION + PLACE_MAIN_ID},
                    place_location.id           AS {PLACE_LOCATION_ID},
                    place_location.coords[0]    AS {PLACE_LOCATION_COORD_LAT},
                    place_location.coords[1]    AS {PLACE_LOCATION_COORD_LONG}
                FROM
                    place_location
                    INNER JOIN place_main ON place_location.place_main_id = place_main.id
                WHERE
                    place_main.is_published = TRUE AND
                    SQRT( POWER( $1 - place_location.coords[0], 2 ) + POWER( $2 - place_location.coords[1], 2 ) ) < $3
            """

            rows = await conn.fetch(sql, center_point_list[0], center_point_list[1], radius)
            return [PlaceLocationDeserializer.deserialize(row, DES_PLACE_LOCATION_FROM_DB_FULL) for row in rows], None

    async def update(self, place_main_id, place_location: PlaceLocation):
        sql = """
            UPDATE
                place_location
            SET
                full_location = $1,
                city = $2,
                country = $3,
                coords = $4
            WHERE place_main_id = $5
        """
        print(place_location.coords)
        await self.conn.execute(sql, place_location.full_address,
                                place_location.city,
                                place_location.country,
                                place_location.coords,
                                place_main_id)

        return None, None
