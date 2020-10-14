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
        return {'menu_main_id': menu_common.menu.id,
                'menu_main_name': menu_common.menu.name,
                'menu_main_photo_link': menu_common.menu.photo,
                'language_id': menu_common.language.id,
                'language_name': menu_common.language.name,
                'currency_id': menu_common.currency.id,
                'currency_sign': menu_common.currency.sign,
                'data': {f'{i + 1}': {
                            'menu_category': {'menu_category_id' : menu_common.menu_category[i].id,
                                              'menu_category_name' : menu_common.menu_category[i].name},
                            'measure_unit': {'measure_unit_id' : menu_common.measure_unit[i].id,
                                             'measure_unit_name': menu_common.measure_unit[i].name},
                            'dish_main': {'dish_main_id' :menu_common.dish_main[i].id,
                                          'dish_main_name': menu_common.dish_main[i].name,
                                          'dish_main_photo': menu_common.dish_main[i].photo,
                                          'dish_main_description': menu_common.dish_main[i].description},
                            'dish_measures': {'dish_measures_id' : menu_common.dish_measures[i].id,
                                              'dish_measures_price_value': menu_common.dish_measures[i].price_value,
                                              'dish_measures_measure_value': menu_common.dish_measures[i].measure_value}
                            } for i in range(len(menu_common.dish_main))}
                }
