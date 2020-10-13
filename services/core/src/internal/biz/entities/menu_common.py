from typing import Optional, List

from src.internal.biz.entities.abstract_model import AbstractModel
from src.internal.biz.entities.menu_category import MenuCategory
from src.internal.biz.entities.dish_measure import DishMeasure
from src.internal.biz.entities.dish_main import DishMain
from src.internal.biz.entities.language import Language
from src.internal.biz.entities.menu_main import MenuMain


class MenuCommon:

    def __init__(self, menu_main: Optional[MenuMain] = None,
                 dish_main: Optional[DishMain] = None,
                 dish_measures: Optional[List[DishMeasure]] = None,
                 menu_category: Optional[List[MenuCategory]] = None,
                 language: Optional[Language] = None,
                 ) -> None:
        self.__menu_main = menu_main
        self.__dish_main = dish_main
        self.__dish_measures = dish_measures
        self.__menu_category = menu_category
        self.__language = language


    @property
    def menu(self) -> Optional[MenuMain]:
        return self.__menu

    @property
    def dish_main(self) -> Optional[DishMain]:
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
