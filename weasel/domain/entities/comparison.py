from pydantic import BaseModel, ConfigDict

from weasel.domain.entities.match import MatchEntity
from weasel.domain.entities.metrics import MetricsEntity


class ComparisonEntity(BaseModel):
    """The comparison entity."""

    source: str
    target: str
    metrics: MetricsEntity
    matches: list[MatchEntity]

    model_config = ConfigDict(from_attributes=True)
