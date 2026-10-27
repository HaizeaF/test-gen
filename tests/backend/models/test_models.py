"""Contract tests for the schema"""

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.backend.models import Answer, Question, QuizSession, Section, Topic


def _question(section: Section, **overrides) -> Question:
    fields = {
        "section": section,
        "text": "What is the capital of France?",
        "option_a": "Paris",
        "option_b": "London",
        "option_c": "Berlin",
        "option_d": "Madrid",
        "correct_option": "a",
    }
    return Question(**{**fields, **overrides})


def _answer(quiz: QuizSession, question: Question, **overrides) -> Answer:
    fields = {"session": quiz, "question": question, "selected_option": "a", "is_correct": True, "time_spent_seconds": 3.0}
    return Answer(**{**fields, **overrides})


def _count(session: Session, model: type) -> int:
    return session.execute(select(func.count()).select_from(model)).scalar_one()


@pytest.fixture
def section(session: Session) -> Section:
    sec = Section(topic=Topic(name="Geography"), name="Capitals")
    session.add(sec)
    session.commit()
    return sec


@pytest.fixture
def answered(session: Session, section: Section) -> tuple[Question, QuizSession, Answer]:
    question, quiz = _question(section), QuizSession(mode="random")
    answer = _answer(quiz, question)
    session.add(answer)
    session.commit()
    return question, quiz, answer


# // ------------ QUESTIONS ------------ //


def test_questions_with_the_same_text_are_allowed(session: Session, section: Section) -> None:
    session.add_all([_question(section), _question(section, option_a="other")])

    session.commit()

    assert _count(session, Question) == 2


def test_new_question_is_active_and_not_flagged(session: Session, section: Section) -> None:
    question = _question(section)
    session.add(question)
    session.commit()

    assert question.active is True
    assert question.flagged is False


def test_invalid_correct_option_is_rejected(session: Session, section: Section) -> None:
    session.add(_question(section, correct_option="z"))

    with pytest.raises(IntegrityError):
        session.commit()


# // ------------ ANSWERS ------------ //


def test_invalid_selected_option_is_rejected(session: Session, section: Section) -> None:
    session.add(_answer(QuizSession(mode="random"), _question(section), selected_option="z"))

    with pytest.raises(IntegrityError):
        session.commit()


def test_blank_answer_is_allowed(session: Session, section: Section) -> None:
    session.add(_answer(QuizSession(mode="random"), _question(section), selected_option=None, is_correct=False))

    session.commit()


# // ------------ NAMES ------------ //


def test_topic_names_are_unique(session: Session) -> None:
    session.add_all([Topic(name="Geography"), Topic(name="Geography")])

    with pytest.raises(IntegrityError):
        session.commit()


def test_section_names_are_unique_within_a_topic(session: Session, section: Section) -> None:
    session.add(Section(topic=section.topic, name=section.name))

    with pytest.raises(IntegrityError):
        session.commit()


def test_two_topics_can_share_a_section_name(session: Session, section: Section) -> None:
    session.add(Section(topic=Topic(name="History"), name=section.name))

    session.commit()


# // ------------ DELETIONS ------------ //


def test_deleting_a_session_deletes_its_answers(session: Session, answered) -> None:
    _, quiz, _ = answered

    session.delete(quiz)
    session.commit()

    assert _count(session, Answer) == 0


def test_deleting_an_answer_keeps_its_session(session: Session, answered) -> None:
    _, _, answer = answered

    session.delete(answer)
    session.commit()

    assert _count(session, QuizSession) == 1


def test_question_with_answers_cannot_be_deleted(session: Session, answered) -> None:
    question, _, _ = answered

    session.delete(question)

    with pytest.raises(IntegrityError):
        session.commit()


def test_section_with_questions_cannot_be_deleted(session: Session, section: Section) -> None:
    session.add(_question(section))
    session.commit()

    session.delete(section)

    with pytest.raises(IntegrityError):
        session.commit()


def test_topic_with_sections_cannot_be_deleted(session: Session, section: Section) -> None:
    session.delete(section.topic)

    with pytest.raises(IntegrityError):
        session.commit()
