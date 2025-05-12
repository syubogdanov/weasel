from enum import StrEnum, auto


class LanguageType(StrEnum):
    """The language type."""

    JAVA = auto()
    PYTHON = auto()
    SQL = auto()
    STARLARK = auto()
