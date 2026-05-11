import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.main import app  # noqa: E402
from app.storage import devices, telemetry_store, seed_devices  # noqa: E402


@pytest.fixture(autouse=True)
def reset_storage():
    devices.clear()
    telemetry_store.clear()
    seed_devices()


@pytest.fixture
def client():
    return TestClient(app)