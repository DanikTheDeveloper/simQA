import strawberry
from typing import List, Optional

from app.storage import devices


@strawberry.type
class DeviceType:
    id: str
    type: str
    status: str
    temperature: Optional[float]
    humidity: Optional[float]


@strawberry.type
class Query:
    @strawberry.field
    def devices(self) -> List[DeviceType]:
        return [
            DeviceType(
                id=device["id"],
                type=device["type"],
                status=device["status"],
                temperature=device.get("temperature"),
                humidity=device.get("humidity"),
            )
            for device in devices.values()
        ]


schema = strawberry.Schema(query=Query)