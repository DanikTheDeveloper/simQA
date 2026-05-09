from typing import List

import strawberry

from app.storage import devices


@strawberry.type
class DeviceGraphQL:
    id: str
    type: str
    status: str
    temperature: float
    humidity: float


@strawberry.type
class Query:
    @strawberry.field
    def devices(self) -> List[DeviceGraphQL]:
        return [
            DeviceGraphQL(
                id=device.id,
                type=device.type,
                status=device.status,
                temperature=device.temperature,
                humidity=device.humidity,
            )
            for device in devices.values()
        ]


schema = strawberry.Schema(query=Query)