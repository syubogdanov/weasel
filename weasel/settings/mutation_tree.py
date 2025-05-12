from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt


class MutationTreeSettings(BaseModel):
    """The mutation tree settings.

    Notes
    -----
    * The settings are not meant to be overridden by environment variables;
    * `pydantic_settings` must not be used.
    """

    # The number of branches to explore.
    degree_of_freedom: NonNegativeInt = 3
    # The maximum tree depth.
    depth: NonNegativeInt = 3
    # The tolerance.
    tolerance: NonNegativeFloat = 0.05
