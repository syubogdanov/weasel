from typing import Annotated

from pydantic import BaseModel, Field, NonNegativeInt


class MutationTreeSettings(BaseModel):
    """The mutation tree settings."""

    # The number of branches to explore.
    degree_of_freedom: NonNegativeInt = 3
    # The maximum tree depth.
    depth: NonNegativeInt = 3
    # The tolerance.
    tolerance: Annotated[float, Field(ge=0.0, le=1.0)] = 0.05
