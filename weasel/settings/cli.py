from enum import StrEnum, auto

from pydantic import BaseModel


class EstimatorType(StrEnum):
    """The estimator type."""

    DAMERAU_LEVENSHTEIN = auto()
    JARO_WINKLER = auto()
    LEVENSHTEIN = auto()


class CommandLineSettings(BaseModel):
    """The command line settings.

    Notes
    -----
    * The settings are not meant to be overridden by environment variables;
    * `pydantic_settings` must not be used.
    """

    # The algorithm used to estimate the similarity between two strings.
    estimator_type: EstimatorType = EstimatorType.DAMERAU_LEVENSHTEIN
