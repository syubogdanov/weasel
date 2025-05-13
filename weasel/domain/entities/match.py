from pathlib import Path

from pydantic import BaseModel, ConfigDict

from weasel.domain.dtypes.probability import Probability
from weasel.domain.types.language import LanguageType


class MatchEntity(BaseModel):
    """The match entity."""

    source: Path
    target: Path
    language: LanguageType
    probability: Probability
    labels: list[str]

    model_config = ConfigDict(from_attributes=True)
