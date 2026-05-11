def test_post_telemetry_successfully(client):
    device_id = "test-vav-telemetry-999"

    device_payload = {
        "id": device_id,
        "type": "vav_box",
        "status": "online",
        "temperature": 21.0,
        "humidity": 39.5
    }

    create_response = client.post("/devices", json=device_payload)

    assert create_response.status_code == 201, create_response.json()

    telemetry_payload = {
        "device_id": device_id,
        "temperature": 23.2,
        "humidity": 44.1,
        "status": "online",
        "timestamp": "2026-01-01T12:00:00Z"
    }

    response = client.post("/telemetry", json=telemetry_payload)

    assert response.status_code == 201, response.json()
    assert response.json()["message"] == "telemetry accepted"


def test_get_telemetry_for_existing_device(client):
    device_payload = {
        "id": "boiler-test-001",
        "type": "boiler",
        "status": "online",
        "temperature": 61.0,
        "humidity": 30.0
    }

    client.post("/devices", json=device_payload)

    telemetry_payload = {
        "device_id": "boiler-test-001",
        "temperature": 65.0,
        "humidity": 32.0,
        "status": "online",
        "timestamp": "2026-01-01T12:00:00Z"
    }

    client.post("/telemetry", json=telemetry_payload)

    response = client.get("/telemetry/boiler-test-001")

    assert response.status_code == 200

    telemetry_data = response.json()

    assert isinstance(telemetry_data, list)
    assert len(telemetry_data) == 1
    assert telemetry_data[0]["device_id"] == "boiler-test-001"
    assert telemetry_data[0]["temperature"] == 65.0


def test_get_telemetry_for_unknown_device_returns_404(client):
    response = client.get("/telemetry/unknown-device")

    assert response.status_code == 404


def test_post_telemetry_rejects_missing_device_id(client):
    payload = {
        "temperature": 23.2,
        "humidity": 44.1,
        "status": "online",
        "timestamp": "2026-01-01T12:00:00Z"
    }

    response = client.post("/telemetry", json=payload)

    assert response.status_code == 422