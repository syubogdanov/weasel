from enum import StrEnum, auto

from pydantic import BaseModel


class EstimatorType(StrEnum):
    """The estimator type."""

    DAMERAU_LEVENSHTEIN = auto()
    JARO_WINKLER = auto()
    LEVENSHTEIN = auto()


class EstimatorSettings(BaseModel):
    """The estimator settings."""

    # The estimator used to measure string similarity.
    type: EstimatorType = EstimatorType.DAMERAU_LEVENSHTEIN
