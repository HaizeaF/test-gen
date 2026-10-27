"""Scoring logic used to rank questions."""


def smoothed_accuracy(correct: int, attempts: int) -> float:
    """Return a Laplace smoothed success rate: (correct + 1) / (attempts + 2)."""
    if not 0 <= correct <= attempts:
        raise ValueError(f"Invalid counts: correct={correct}, attempts={attempts}")

    return (correct + 1) / (attempts + 2)
