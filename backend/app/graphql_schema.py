from typing import List

import strawberry

from app.storage import devices, telemetry_store


@strawberry.type
class DeviceGraphQL:
    id: str
    type: str
    status: str
    temperature: float
    humidity: float


@strawberry.type
class TelemetryGraphQL:
    device_id: str
    temperature: float
    humidity: float
    status: str


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

    @strawberry.field
    def telemetry(self, device_id: str) -> List[TelemetryGraphQL]:
        telemetry_data = telemetry_store.get(device_id, [])

        return [
            TelemetryGraphQL(
                device_id=item.device_id,
                temperature=item.temperature,
                humidity=item.humidity,
                status=item.status,
            )
            for item in telemetry_data
        ]


schema = strawberry.Schema(query=Query)