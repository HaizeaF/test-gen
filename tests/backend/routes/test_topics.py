"""Tests for the topic routes."""

from fastapi.testclient import TestClient

from src.backend.models import Section, Topic


def test_create_topic(client: TestClient) -> None:
    """Test that creating a topic returns 201 and the stored topic."""
    response = client.post("/topics", json={"name": "  Geography  "})

    assert response.status_code == 201
    assert response.json()["name"] == "Geography"
    assert len(client.get("/topics").json()) == 1


def test_create_topic_with_existing_name_conflicts(client: TestClient, topic: Topic) -> None:
    """Test that a second topic with the same name is rejected with 409 and a message naming it."""
    response = client.post("/topics", json={"name": "Geography"})

    assert response.status_code == 409
    assert "Geography" in response.json()["detail"]


def test_create_topic_with_blank_name_is_rejected(client: TestClient) -> None:
    """Test that a name with only whitespace fails validation."""
    response = client.post("/topics", json={"name": "   "})

    assert response.status_code == 422


def test_list_topics_returns_them_in_creation_order(client: TestClient) -> None:
    """Test that every topic is listed, ordered by id."""
    client.post("/topics", json={"name": "Maths"})
    client.post("/topics", json={"name": "Sociology"})

    response = client.get("/topics")

    assert response.status_code == 200
    assert [topic["name"] for topic in response.json()] == ["Sociology", "Maths"]


def test_update_topic_persists_the_new_name(client: TestClient, topic: Topic) -> None:
    """Test that the change is saved, not only returned in the response."""
    response = client.patch(f"/topics/{topic.id}", json={"name": "Maps"})

    assert response.status_code == 200
    assert response.json()["name"] == "Maps"
    assert [item["name"] for item in client.get("/topics").json()] == ["Maps"]


def test_update_topic_to_existing_name_conflicts(client: TestClient, topic: Topic) -> None:
    """Test that renaming onto an existing name returns 409 and leaves the topic unchanged."""
    client.post("/topics", json={"name": "History"})

    response = client.patch(f"/topics/{topic.id}", json={"name": "History"})

    assert response.status_code == 409
    assert [item["name"] for item in client.get("/topics").json()] == ["History", "Geography"]


def test_update_unknown_topic_returns_404(client: TestClient) -> None:
    """Test that updating a topic that does not exist returns 404."""
    response = client.patch("/topics/999", json={"name": "Maps"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Topic 999 not found"


def test_update_topic_ignores_null_fields(client: TestClient, topic: Topic) -> None:
    """Test that sending null for the name does not erase it."""
    response = client.patch(f"/topics/{topic.id}", json={"name": None})

    assert response.status_code == 200
    assert response.json()["name"] == "Geography"
    assert [item["name"] for item in client.get("/topics").json()] == ["Geography"]


def test_delete_topic(client: TestClient, topic: Topic) -> None:
    """Test that deleting a topic without sections returns 204 and removes it."""
    topic_id = topic.id

    response = client.delete(f"/topics/{topic_id}")

    assert response.status_code == 204
    assert client.get("/topics").json() == []


def test_delete_topic_with_sections_conflicts(client: TestClient, section: Section) -> None:
    """Test that a topic that still has sections cannot be deleted."""
    topic_id = section.topic_id

    response = client.delete(f"/topics/{topic_id}")

    assert response.status_code == 409
    assert "1 section(s)" in response.json()["detail"]
    assert len(client.get("/topics").json()) == 1


def test_delete_unknown_topic_returns_404(client: TestClient) -> None:
    """Test that deleting a topic that does not exist returns 404."""
    response = client.delete("/topics/999")

    assert response.status_code == 404
