from enum import StrEnum, auto

from pydantic import BaseModel


class EstimatorType(StrEnum):
    """The estimator type."""

    DAMERAU_LEVENSHTEIN = auto()
    JARO_WINKLER = auto()
    LEVENSHTEIN = auto()


class CoreSettings(BaseModel):
    """The core settings."""

    # The algorithm used to estimate the similarity between two strings.
    estimator_type: EstimatorType = EstimatorType.DAMERAU_LEVENSHTEIN
