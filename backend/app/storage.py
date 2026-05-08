from app.models import Device, Telemetry


devices: dict[str, Device] = {}
telemetry_store: dict[str, list[Telemetry]] = {}


def seed_devices() -> None:
    if devices:
        return

    default_devices = [
        Device(
            id="ahu-001",
            type="air_handler",
            status="online",
            temperature=22.5,
            humidity=41.0,
        ),
        Device(
            id="vav-001",
            type="vav_box",
            status="online",
            temperature=21.0,
            humidity=38.0,
        ),
        Device(
            id="boiler-001",
            type="boiler",
            status="online",
            temperature=65.0,
            humidity=30.0,
        ),
    ]

    for device in default_devices:
        devices[device.id] = device
        telemetry_store[device.id] = []