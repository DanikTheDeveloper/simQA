def test_get_devices_returns_list(client):
    response = client.get("/devices")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_device_successfully(client):
    payload = {
        "id": "ahu-test-001",
        "type": "air_handler",
        "status": "online",
        "temperature": 22.5,
        "humidity": 41.0
    }

    response = client.post("/devices", json=payload)

    assert response.status_code in [200, 201]

    devices_response = client.get("/devices")
    devices = devices_response.json()

    assert any(device["id"] == "ahu-test-001" for device in devices)


def test_create_device_rejects_missing_id(client):
    payload = {
        "type": "air_handler",
        "status": "online",
        "temperature": 22.5,
        "humidity": 41.0
    }

    response = client.post("/devices", json=payload)

    assert response.status_code == 422