"""Errors raised by the data access and business layers."""


class NotFoundError(Exception):
    """The requested row does not exist."""


class ConflictError(Exception):
    """The operation breaks a rule."""
