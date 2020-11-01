from typing import Tuple, Optional

from src.internal.adapters.entities.error import Error
from src.internal.biz.dao.base_dao import BaseDao
from src.internal.biz.entities.place_contacts import PlaceContacts


class PlaceContactsDao(BaseDao):

    async def add(self, place_contacts: PlaceContacts) -> Tuple[Optional[PlaceContacts], Optional[Error]]:
        await self.conn.execute(
            """
                INSERT INTO place_contacts(place_main_id, phone_number, email, site_link, vk_link, instagram_link, facebook_link)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, place_contacts.place_main.id, place_contacts.phone_number, place_contacts.email, place_contacts.site_link,
            place_contacts.vk_link, place_contacts.instagram_link, place_contacts.facebook_link
        )
        return place_contacts, None

    async def update(self, place_main_id, place_contacts: PlaceContacts) -> Tuple[Optional[PlaceContacts], Optional[Error]]:
        sql = """
            UPDATE place_contacts
            SET
                phone_number = $1,
                email = $2,
                site_link = $3,
                facebook_link = $4,
                instagram_link = $5,
                vk_link = $6
            WHERE place_main_id = $7
        """
        await self.conn.execute(sql, place_contacts.phone_number, place_contacts.email,
                                place_contacts.site_link, place_contacts.facebook_link,
                                place_contacts.instagram_link, place_contacts.vk_link,
                                place_main_id)
        return place_contacts, None
