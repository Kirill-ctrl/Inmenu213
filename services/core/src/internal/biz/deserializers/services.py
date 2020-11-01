from typing import List

from src.internal.biz.deserializers.base_deserializer import BaseDeserializer
from src.internal.biz.entities.place_service import PlaceService
from src.internal.biz.entities.service import Service

DES_SERVICES_ADD = 'services-add'
DES_SERVICES_UPDATE = 'services-update'


class ServicesDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_SERVICES_ADD:
            return cls._deserialize_add
        elif format_des == DES_SERVICES_UPDATE:
            return cls._deserialize_update
        else:
            raise TypeError

    @staticmethod
    def _deserialize_add(services: List[int]) -> List[PlaceService]:
        return [PlaceService(service=Service(id=service_type_id)) for service_type_id in services]

    @staticmethod
    def _deserialize_update(services: List[int]) -> List[PlaceService]:
        return [PlaceService(service=Service(id=service_type_id if service_type_id else 0)) for service_type_id in services]
