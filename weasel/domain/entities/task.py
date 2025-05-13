from pydantic import BaseModel, ConfigDict

from weasel.domain.entities.submission import SubmissionEntity


class TaskEntity(BaseModel):
    """The task entity."""

    name: str
    submissions: list[SubmissionEntity]

    model_config = ConfigDict(from_attributes=True)
