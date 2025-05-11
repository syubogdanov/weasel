from enum import StrEnum, auto


class EstimatorType(StrEnum):
    """The estimator type."""

    DAMERAU_LEVENSHTEIN = auto()
    JARO_WINKLER = auto()
    LEVENSHTEIN = auto()
