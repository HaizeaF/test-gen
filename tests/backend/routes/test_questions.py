"""Tests for the question routes."""

from fastapi.testclient import TestClient

from src.backend.models import Answer, Question, Section


def question_payload(section_id: int, **overrides: object) -> dict[str, object]:
    """Build a valid question body for the API."""
    payload = {
        "section_id": section_id,
        "text": "What is the capital of France?",
        "option_a": "Paris",
        "option_b": "Rome",
        "option_c": "Madrid",
        "option_d": "Berlin",
        "correct_option": "a",
    }
    return payload | overrides


def test_create_question(client: TestClient, section: Section) -> None:
    """Test that creating a question returns 201 with its section and topic names, not flagged and active."""
    response = client.post("/questions", json=question_payload(section.id))

    assert response.status_code == 201
    body = response.json()
    assert body["text"] == "What is the capital of France?"
    assert body["correct_option"] == "a"
    assert body["section_id"] == section.id
    assert body["section_name"] == "Capitals"
    assert body["topic_id"] == section.topic_id
    assert body["topic_name"] == "Geography"
    assert body["flagged"] is False
    assert body["active"] is True


def test_create_question_in_unknown_section_returns_404(client: TestClient) -> None:
    """Test that creating a question in a section that does not exist returns 404."""
    response = client.post("/questions", json=question_payload(999))

    assert response.status_code == 404
    assert response.json()["detail"] == "Section 999 not found"


def test_create_question_with_invalid_correct_option_is_rejected(client: TestClient, section: Section) -> None:
    """Test that the correct option must be one of a, b, c or d."""
    response = client.post("/questions", json=question_payload(section.id, correct_option="e"))

    assert response.status_code == 422


def test_create_question_with_blank_text_is_rejected(client: TestClient, section: Section) -> None:
    """Test that the text of the question and of its options cannot be blank."""
    response = client.post("/questions", json=question_payload(section.id, option_b="   "))

    assert response.status_code == 422


def test_list_questions_puts_flagged_ones_first(client: TestClient, question: Question) -> None:
    """Test that a flagged question is listed before questions that are not flagged."""
    question_id = client.post("/questions", json=question_payload(question.section_id)).json()["id"]
    second_id = question.id
    client.patch(f"/questions/{question_id}", json={"flagged": True})

    response = client.get("/questions")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [question_id, second_id]


def test_update_question_persists_the_changes(client: TestClient, question: Question) -> None:
    """Test that the edited fields are saved, not only returned in the response."""
    response = client.patch(f"/questions/{question.id}", json={"text": "New text", "correct_option": "d"})

    assert response.status_code == 200
    stored = client.get("/questions").json()[0]
    assert stored["text"] == "New text"
    assert stored["correct_option"] == "d"
    assert stored["option_a"] == "Paris"


def test_move_question_to_another_section(client: TestClient, question: Question, other_section: Section) -> None:
    """Test that moving a question updates its section and topic, both in the response and in what is stored."""
    response = client.patch(f"/questions/{question.id}", json={"section_id": other_section.id})

    assert response.status_code == 200
    for body in (response.json(), client.get("/questions").json()[0]):
        assert body["section_name"] == "Wars"
        assert body["topic_id"] == other_section.topic_id
        assert body["topic_name"] == "History"


def test_update_question_ignores_null_fields(client: TestClient, question: Question) -> None:
    """Test that sending null for a field does not erase it."""
    response = client.patch(f"/questions/{question.id}", json={"text": None, "flagged": True})

    assert response.status_code == 200
    assert response.json()["text"] == "What is the capital of Italy?"
    assert response.json()["flagged"] is True


def test_move_question_to_unknown_section_returns_404(client: TestClient, question: Question) -> None:
    """Test that moving a question to a section that does not exist returns 404 and keeps it where it was."""
    response = client.patch(f"/questions/{question.id}", json={"section_id": 999})

    assert response.status_code == 404
    assert response.json()["detail"] == "Section 999 not found"
    assert client.get("/questions").json()[0]["section_name"] == "Capitals"


def test_update_unknown_question_returns_404(client: TestClient) -> None:
    """Test that updating a question that does not exist returns 404."""
    response = client.patch("/questions/999", json={"text": "New text"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Question 999 not found"


def test_delete_question(client: TestClient, question: Question) -> None:
    """Test that deleting a question without answers returns 204 and removes it."""
    question_id = question.id

    response = client.delete(f"/questions/{question_id}")

    assert response.status_code == 204
    assert client.get("/questions").json() == []


def test_delete_question_with_answers_conflicts(client: TestClient, question: Question, answer: Answer) -> None:
    """Test that a question that has been answered cannot be deleted, so the analytics keep their history."""
    question_id = question.id

    response = client.delete(f"/questions/{question_id}")

    assert response.status_code == 409
    assert "1 answer(s)" in response.json()["detail"]
    assert len(client.get("/questions").json()) == 1


def test_delete_unknown_question_returns_404(client: TestClient) -> None:
    """Test that deleting a question that does not exist returns 404."""
    response = client.delete("/questions/999")

    assert response.status_code == 404
