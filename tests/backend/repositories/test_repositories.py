"""Tests for the repositories and the unit of work."""

import pytest

from src.backend.models import Answer, Question, Section, Topic
from src.backend.models.errors import ConflictError, NotFoundError
from src.backend.repositories.unit_of_work import UnitOfWork


def build_question(section: Section, text: str, flagged: bool = False) -> Question:
    """Build a valid question inside the section."""
    return Question(
        section=section,
        text=text,
        option_a="a",
        option_b="b",
        option_c="c",
        option_d="d",
        correct_option="a",
        flagged=flagged,
    )


@pytest.mark.parametrize("repository_name", ["topics", "sections", "questions"])
def test_get_unknown_row_raises_not_found(uow: UnitOfWork, repository_name: str) -> None:
    """Test that every repository raises NotFoundError, naming the missing id, when the row does not exist."""
    with pytest.raises(NotFoundError, match="999"):
        getattr(uow, repository_name).get(999)


def test_sections_are_listed_newest_first(uow: UnitOfWork, topic: Topic, section: Section) -> None:
    """Test that a section created later is listed before an older one."""
    newer = uow.sections.add(Section(topic=topic, name="Rivers"))
    uow.commit("The section could not be saved.")

    assert [item.id for item in uow.sections.get_all()] == [newer.id, section.id]


def test_questions_are_listed_flagged_first_then_newest_first(uow: UnitOfWork, section: Section, question: Question) -> None:
    """Test that a flagged question goes first even if it is older than others that are not flagged."""
    flagged = uow.questions.add(build_question(section, "Flagged question", flagged=True))
    uow.commit("The question could not be saved.")
    newest = uow.questions.add(build_question(section, "Newest question"))
    uow.commit("The question could not be saved.")

    assert [item.id for item in uow.questions.get_all()] == [flagged.id, newest.id, question.id]


def test_counts_only_include_the_rows_of_the_given_parent(
    uow: UnitOfWork,
    topic: Topic,
    section: Section,
    question: Question,
    answer: Answer,
    other_topic: Topic,
    other_section: Section,
) -> None:
    """Test that the counts include the children of one parent and ignore those of another."""
    uow.sections.add(Section(topic=topic, name="Rivers"))
    unanswered = uow.questions.add(build_question(section, "Unanswered question"))
    uow.commit("The data could not be saved.")

    assert uow.sections.count_by_topic(topic.id) == 2
    assert uow.sections.count_by_topic(other_topic.id) == 1

    assert uow.questions.count_by_section(section.id) == 2
    assert uow.questions.count_by_section(other_section.id) == 0

    assert uow.questions.count_answers(question.id) == 1
    assert uow.questions.count_answers(unanswered.id) == 0


def test_commit_raises_conflict_and_leaves_the_session_usable(uow: UnitOfWork, topic: Topic) -> None:
    """Test that a database constraint violation becomes ConflictError and the session can keep being used."""
    uow.topics.add(Topic(name="Geography"))

    with pytest.raises(ConflictError, match="already exists"):
        uow.commit("A topic with that name already exists.")

    assert [item.name for item in uow.topics.get_all()] == ["Geography"]
