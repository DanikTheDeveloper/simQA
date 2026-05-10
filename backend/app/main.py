from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.models import Device, Telemetry
from app.storage import devices, telemetry_store, seed_devices

from strawberry.fastapi import GraphQLRouter
from app.graphql_schema import schema


app = FastAPI(
    title="Building Device Simulation Platform API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


@app.on_event("startup")
def startup_event() -> None:
    seed_devices()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/devices", response_model=list[Device])
def get_devices() -> list[Device]:
    return list(devices.values())


@app.post("/devices", response_model=Device, status_code=status.HTTP_201_CREATED)
def create_device(device: Device) -> Device:
    if device.id in devices:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Device '{device.id}' already exists",
        )

    devices[device.id] = device
    telemetry_store[device.id] = []
    return device


@app.post("/telemetry", status_code=status.HTTP_201_CREATED)
def submit_telemetry(telemetry: Telemetry) -> dict[str, str]:
    if telemetry.device_id not in devices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device '{telemetry.device_id}' not found",
        )

    existing_device = devices[telemetry.device_id]

    updated_device = Device(
        id=existing_device.id,
        type=existing_device.type,
        status=telemetry.status,
        temperature=telemetry.temperature,
        humidity=telemetry.humidity,
    )

    devices[telemetry.device_id] = updated_device
    telemetry_store[telemetry.device_id].append(telemetry)

    return {"message": "telemetry accepted"}


@app.get("/telemetry/{device_id}", response_model=list[Telemetry])
def get_device_telemetry(device_id: str) -> list[Telemetry]:
    if device_id not in devices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device '{device_id}' not found",
        )

    return telemetry_store[device_id]
