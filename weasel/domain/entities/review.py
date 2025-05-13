from pydantic import BaseModel, ConfigDict

from weasel.domain.entities.comparison import ComparisonEntity


class ReviewEntity(BaseModel):
    """The review entity."""

    name: str
    comparisons: list[ComparisonEntity]

    model_config = ConfigDict(from_attributes=True)
