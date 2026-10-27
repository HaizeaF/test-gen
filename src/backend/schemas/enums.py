"""Enumerations shared across the backend."""

from enum import StrEnum


class QuizMode(StrEnum):
    """Ways of building a quiz."""

    RANDOM = "random"
    WEAK = "weak"
    UNSEEN = "unseen"
    RECOMMENDED = "recommended"


class Option(StrEnum):
    """Possible answers to a question."""

    A = "a"
    B = "b"
    C = "c"
    D = "d"
