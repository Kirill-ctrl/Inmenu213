from src.internal.biz.serializers.base_serializer import BaseSerializer
from src.internal.biz.entities.menu_common import MenuCommon

SER_FOR_GET_MENU = 'ser-for-get-menu'


class MenuSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_GET_MENU:
            return cls._ser_for_get_menu

    @staticmethod
    def _ser_for_get_menu(menu_common: MenuCommon):

        return {
            'language': menu_common.language,
            'menu_main_id': menu_common.menu.id,
            'menu_main_name': menu_common.menu.name,
            'menu_main_photo_link': menu_common.menu.photo,
            'menu_category_name' : menu_common.menu_category.name,
            'price_measures': menu_common.dish_measures.price_value,
            'measure_value': menu_common.dish_measures.measure_value
        }