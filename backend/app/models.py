from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


DeviceType = Literal["air_handler", "vav_box", "boiler", "thermostat"]
DeviceStatus = Literal["online", "offline", "fault"]


class Device(BaseModel):
    id: str = Field(..., min_length=1)
    type: DeviceType
    status: DeviceStatus = "online"
    temperature: float = Field(..., ge=-50, le=120)
    humidity: float = Field(..., ge=0, le=100)


class Telemetry(BaseModel):
    device_id: str = Field(..., min_length=1)
    temperature: float = Field(..., ge=-50, le=120)
    humidity: float = Field(..., ge=0, le=100)
    status: DeviceStatus = "online"
    timestamp: datetime