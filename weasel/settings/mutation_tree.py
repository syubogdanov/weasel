from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt


class MutationTreeSettings(BaseModel):
    """The mutation tree settings."""

    # The number of branches to explore.
    degree_of_freedom: NonNegativeInt = 3
    # The maximum tree depth.
    depth: NonNegativeInt = 3
    # The tolerance.
    tolerance: NonNegativeFloat = 0.05
