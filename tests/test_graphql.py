from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


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