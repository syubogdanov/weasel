class WeaselError(Exception):
    """Base class for all exceptions."""


class UnknownLanguageError(WeaselError):
    """Exception when the language is unknown."""
