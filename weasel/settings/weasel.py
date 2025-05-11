from enum import StrEnum, auto

from pydantic import BaseModel


class EstimatorType(StrEnum):
    """The estimator type."""

    DAMERAU_LEVENSHTEIN = auto()
    JARO_WINKLER = auto()
    LEVENSHTEIN = auto()


class WeaselSettings(BaseModel):
    """The *Weasel* settings.

    Notes
    -----
    * `pydantic_settings` should not be used to avoid using the environment.
    """

    estimator_type: EstimatorType = EstimatorType.DAMERAU_LEVENSHTEIN
