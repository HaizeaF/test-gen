"""Errors that services raise."""

class NotFoundError(Exception):
    """The requested row does not exist."""

class ConflictError(Exception):
    """The operation breaks a rule."""