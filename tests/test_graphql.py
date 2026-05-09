from datetime import datetime, timezone, timedelta

from fastapi.testclient import TestClient

from app.main import app


def test_graphql_devices_query_returns_seeded_devices():
    with TestClient(app) as test_client:
        response = test_client.post(
            "/graphql",
            json={
                "query": """
                query {
                  devices {
                    id
                    type
                    status
                    temperature
                    humidity
                  }
                }
                """
            },
        )

    assert response.status_code == 200

    body = response.json()
    assert "data" in body
    assert "devices" in body["data"]

    returned_devices = body["data"]["devices"]

    assert any(device["id"] == "ahu-001" for device in returned_devices)
    assert any(device["id"] == "vav-001" for device in returned_devices)
    assert any(device["id"] == "boiler-001" for device in returned_devices)


def test_graphql_invalid_field_returns_error():
    with TestClient(app) as test_client:
        response = test_client.post(
            "/graphql",
            json={
                "query": """
                query {
                  devices {
                    id
                    nonexistentField
                  }
                }
                """
            },
        )

    assert response.status_code == 200

    body = response.json()
    assert "errors" in body


def test_graphql_telemetry_query_returns_device_telemetry():
    with TestClient(app) as test_client:
        test_client.post(
            "/telemetry",
            json={
                "device_id": "ahu-001",
                "temperature": 23.5,
                "humidity": 42.0,
                "status": "online",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

        response = test_client.post(
            "/graphql",
            json={
                "query": """
                query {
                  telemetry(deviceId: "ahu-001") {
                    deviceId
                    temperature
                    humidity
                    status
                    timestamp
                  }
                }
                """
            },
        )

    assert response.status_code == 200

    body = response.json()
    assert "data" in body
    assert "telemetry" in body["data"]

    telemetry_data = body["data"]["telemetry"]

    assert len(telemetry_data) >= 1
    assert any(item["temperature"] == 23.5 for item in telemetry_data)
    assert any(item["deviceId"] == "ahu-001" for item in telemetry_data)


def test_graphql_recent_minutes_filters_old_telemetry():
    old_timestamp = datetime.now(timezone.utc) - timedelta(minutes=10)
    current_timestamp = datetime.now(timezone.utc)

    with TestClient(app) as test_client:
        test_client.post(
            "/telemetry",
            json={
                "device_id": "vav-001",
                "temperature": 20.0,
                "humidity": 39.0,
                "status": "online",
                "timestamp": old_timestamp.isoformat(),
            },
        )

        test_client.post(
            "/telemetry",
            json={
                "device_id": "vav-001",
                "temperature": 22.0,
                "humidity": 41.0,
                "status": "online",
                "timestamp": current_timestamp.isoformat(),
            },
        )

        response = test_client.post(
            "/graphql",
            json={
                "query": """
                query {
                  telemetry(deviceId: "vav-001", recentMinutes: 1) {
                    deviceId
                    temperature
                    humidity
                    status
                    timestamp
                  }
                }
                """
            },
        )

    assert response.status_code == 200

    body = response.json()
    telemetry_data = body["data"]["telemetry"]

    temperatures = [item["temperature"] for item in telemetry_data]

    assert 22.0 in temperatures
    assert 20.0 not in temperatures