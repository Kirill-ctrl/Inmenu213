import datetime
from typing import Dict, Any

from src.internal.biz.deserializers.base_deserializer import BaseDeserializer
from src.internal.biz.entities.place_work_hours import PlaceWorkHours

DES_WORK_HOURS_ADD = 'work-hours-add'
DES_WORK_HOURS_UPDATE = 'work-hours-week-update'


class PlaceWorkHoursDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_WORK_HOURS_ADD:
            return cls._deserialize_add
        elif format_des == DES_WORK_HOURS_UPDATE:
            return cls._deserialize_update
        else:
            raise TypeError

    @staticmethod
    def _deserialize_add(work_hours: Dict[str, Any]) -> PlaceWorkHours:
        return PlaceWorkHours(
            is_holiday=work_hours['is_holiday'],
            time_start=datetime.time(hour=work_hours['time_start'] // 3600, minute=work_hours['time_start'] % 3600 // 60) if work_hours.get('time_start') else None,
            time_finish=datetime.time(hour=work_hours['time_finish'] // 3600, minute=work_hours['time_finish'] % 3600 // 60) if work_hours.get('time_finish') else None,
        )

    @staticmethod
    def _deserialize_update(work_hours: Dict[str, Any]) -> PlaceWorkHours:
        return PlaceWorkHours(
            is_holiday=work_hours['is_holiday'],
            time_start=datetime.time(hour=work_hours['time_start'] // 3600, minute=work_hours['time_start'] % 3600 // 60) if work_hours.get('time_start') else None,
            time_finish=datetime.time(hour=work_hours['time_finish'] // 3600, minute=work_hours['time_finish'] % 3600 // 60) if work_hours.get('time_finish') else None
        )
