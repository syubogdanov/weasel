from enum import StrEnum, auto


class LanguageType(StrEnum):
    """The language type."""

    PYTHON = auto()
    SQL = auto()
    STARLARK = auto()
