from typing import Optional, List

from src.internal.biz.entities.menu_category import MenuCategory
from src.internal.biz.entities.dish_measure import DishMeasure
from src.internal.biz.entities.dish_main import DishMain
from src.internal.biz.entities.language import Language
from src.internal.biz.entities.menu_main import MenuMain
from src.internal.biz.entities.currency import Currency
from src.internal.biz.entities.measure_unit import MeasureUnit


class MenuCommon:

    def __init__(self, main_menu: Optional[MenuMain] = None,
                 language: Optional[Language] = None,
                 menu_category: Optional[List[MenuCategory]] = None,
                 measure_unit: Optional[List[MeasureUnit]] = None,
                 dish_main: Optional[List[DishMain]] = None,
                 dish_measures: Optional[List[DishMeasure]] = None,
                 currency: Optional[Currency] = None,
                 ) -> None:
        self.__main_menu = main_menu
        self.__dish_main = dish_main
        self.__dish_measures = dish_measures
        self.__menu_category = menu_category
        self.__language = language
        self.__currency = currency
        self.__measure_unit = measure_unit

    @property
    def menu(self) -> Optional[MenuMain]:
        return self.__main_menu

    @property
    def dish_main(self) -> Optional[List[DishMain]]:
        return self.__dish_main

    @property
    def dish_measures(self) -> Optional[List[DishMeasure]]:
        return self.__dish_measures

    @property
    def menu_category(self) -> Optional[List[MenuCategory]]:
        return self.__menu_category

    @property
    def language(self) -> Optional[Language]:
        return self.__language

    @property
    def currency(self) -> Optional[Currency]:
        return self.__currency

    @property
    def measure_unit(self) -> Optional[List[MeasureUnit]]:
        return self.__measure_unit
