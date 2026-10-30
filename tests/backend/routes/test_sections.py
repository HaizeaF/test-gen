"""Tests for the section routes."""

from fastapi.testclient import TestClient

from src.backend.models import Question, Section, Topic


def test_create_section(client: TestClient, topic: Topic) -> None:
    """Test that creating a section returns 201 with the name of its topic."""
    response = client.post("/sections", json={"topic_id": topic.id, "name": "Rivers"})

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Rivers"
    assert body["topic_id"] == topic.id
    assert body["topic_name"] == "Geography"


def test_create_section_in_unknown_topic_returns_404(client: TestClient) -> None:
    """Test that a missing topic is reported as 404 and not as a name conflict."""
    response = client.post("/sections", json={"topic_id": 999, "name": "Rivers"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Topic 999 not found"


def test_create_section_with_name_used_in_the_same_topic_conflicts(client: TestClient, section: Section) -> None:
    """Test that a topic cannot have two sections with the same name."""
    response = client.post("/sections", json={"topic_id": section.topic_id, "name": "Capitals"})

    assert response.status_code == 409


def test_create_section_with_name_used_in_another_topic_is_allowed(
    client: TestClient, section: Section, other_topic: Topic
) -> None:
    """Test that the same section name can exist in different topics."""
    response = client.post("/sections", json={"topic_id": other_topic.id, "name": "Capitals"})

    assert response.status_code == 201


def test_list_sections_includes_the_topic_name(client: TestClient, section: Section) -> None:
    """Test that every section is listed together with the name of its topic."""
    response = client.get("/sections")

    assert response.status_code == 200
    assert [(item["name"], item["topic_name"]) for item in response.json()] == [("Capitals", "Geography")]


def test_update_section_persists_the_new_name(client: TestClient, section: Section) -> None:
    """Test that the rename is saved, not only returned in the response."""
    response = client.patch(f"/sections/{section.id}", json={"name": "Cities"})

    assert response.status_code == 200
    assert response.json()["name"] == "Cities"
    assert [item["name"] for item in client.get("/sections").json()] == ["Cities"]


def test_update_section_ignores_null_fields(client: TestClient, section: Section, other_topic: Topic) -> None:
    """Test that a null field is ignored while the other fields sent in the same request are applied."""
    response = client.patch(f"/sections/{section.id}", json={"name": None, "topic_id": other_topic.id})

    assert response.status_code == 200
    assert response.json()["name"] == "Capitals"
    assert response.json()["topic_name"] == "History"


def test_move_section_to_another_topic(client: TestClient, section: Section, other_topic: Topic) -> None:
    """Test that moving a section changes its topic, both in the response and in what is stored."""
    response = client.patch(f"/sections/{section.id}", json={"topic_id": other_topic.id})

    assert response.status_code == 200
    assert response.json()["topic_name"] == "History"
    stored = client.get("/sections").json()[0]
    assert stored["topic_id"] == other_topic.id
    assert stored["topic_name"] == "History"


def test_move_section_to_unknown_topic_returns_404(client: TestClient, section: Section) -> None:
    """Test that moving a section to a topic that does not exist returns 404."""
    response = client.patch(f"/sections/{section.id}", json={"topic_id": 999})

    assert response.status_code == 404
    assert response.json()["detail"] == "Topic 999 not found"


def test_move_section_to_topic_with_same_section_name_conflicts(client: TestClient, section: Section, other_topic: Topic) -> None:
    """Test that a section cannot be moved into a topic that already has a section with its name."""
    client.post("/sections", json={"topic_id": other_topic.id, "name": "Capitals"})

    response = client.patch(f"/sections/{section.id}", json={"topic_id": other_topic.id})

    assert response.status_code == 409
    assert {item["topic_name"] for item in client.get("/sections").json()} == {"Geography", "History"}


def test_update_unknown_section_returns_404(client: TestClient) -> None:
    """Test that updating a section that does not exist returns 404."""
    response = client.patch("/sections/999", json={"name": "Cities"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Section 999 not found"


def test_delete_section(client: TestClient, section: Section) -> None:
    """Test that deleting a section without questions returns 204 and removes it."""
    section_id = section.id

    response = client.delete(f"/sections/{section_id}")

    assert response.status_code == 204
    assert client.get("/sections").json() == []


def test_delete_section_with_questions_conflicts(client: TestClient, section: Section, question: Question) -> None:
    """Test that a section that still has questions cannot be deleted."""
    section_id = section.id

    response = client.delete(f"/sections/{section_id}")

    assert response.status_code == 409
    assert "1 question(s)" in response.json()["detail"]
    assert len(client.get("/sections").json()) == 1


def test_delete_unknown_section_returns_404(client: TestClient) -> None:
    """Test that deleting a section that does not exist returns 404."""
    response = client.delete("/sections/999")

    assert response.status_code == 404
