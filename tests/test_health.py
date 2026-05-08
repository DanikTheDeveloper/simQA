from tests.conftest import get_client


def test_health_returns_ok():
    client = get_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] in ["ok", "healthy"]