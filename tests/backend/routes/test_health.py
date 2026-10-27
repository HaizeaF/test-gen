"""Tests for the health route."""

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    """Test that the health endpoint returns a 200 status code and a JSON response."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
