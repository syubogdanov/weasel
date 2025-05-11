from pydantic import BaseModel

from weasel.domain.types.estimator import EstimatorType


class WeaselSettings(BaseModel):
    """The *Weasel* settings.

    Notes
    -----
    * `pydantic_settings` should not be used to avoid using the environment.
    """

    estimator_type: EstimatorType = EstimatorType.DAMERAU_LEVENSHTEIN
