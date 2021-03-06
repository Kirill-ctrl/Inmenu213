from typing import Dict, List

from src.internal.biz.deserializers.base_deserializer import BaseDeserializer
from src.internal.biz.deserializers.place_work_hours import PlaceWorkHoursDeserializer, DES_WORK_HOURS_ADD
from src.internal.biz.entities.place_work_hours import PlaceWorkHours

DES_WORK_HOURS_WEEK_ADD = 'work-hours-week-add'


class PlaceWorkHoursWeekDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str) -> List[PlaceWorkHours]:
        if format_des == DES_WORK_HOURS_WEEK_ADD:
            return cls._deserialize_add
        else:
            raise TypeError

    @staticmethod
    def _deserialize_add(work_hours: dict) -> List[PlaceWorkHours]:

        place_work_hours_week = []
        for week_day, work_hours_day in work_hours.items():
            place_work_hours = PlaceWorkHoursDeserializer.deserialize(work_hours_day, DES_WORK_HOURS_ADD)
            place_work_hours.week_day = week_day
            place_work_hours_week.append(place_work_hours)
        return place_work_hours_week
