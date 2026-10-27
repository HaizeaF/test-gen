"""Tests for the scoring service."""

import pytest
from pytest import approx

from src.backend.services.scoring_service import smoothed_accuracy


@pytest.mark.parametrize(
    "correct, attempts, expected_score",
    [(0, 0, 0.5), (0, 1, 1 / 3), (0, 2, 0.25), (1, 2, 0.5), (3, 4, 4 / 6)],
)
def test_smoothed_accuracy(correct, attempts, expected_score):
    """Test that the smoothed score matches the (correct + 1) / (attempts + 2) formula."""
    assert smoothed_accuracy(correct, attempts) == approx(expected_score)


@pytest.mark.parametrize("correct, attempts", [(-1, 3), (0, -1), (4, 3)])
def test_impossible_counts_are_rejected(correct, attempts):
    """Test that more correct answers than attempts or negative counts are rejected."""
    with pytest.raises(ValueError):
        smoothed_accuracy(correct, attempts)


def test_more_evidence_beats_a_single_success():
    """Test that a single success is beaten by more evidence of success, even if the success rate is the same."""
    assert smoothed_accuracy(1, 1) < smoothed_accuracy(10, 10)
