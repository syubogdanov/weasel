from typing import Annotated

from pydantic import Field


Probability = Annotated[float, Field(ge=0.0, le=1.0)]
