from typing import Annotated

from pydantic import Field


SHA1 = Annotated[str, Field(pattern=r"^[a-f0-9]{40}$")]
