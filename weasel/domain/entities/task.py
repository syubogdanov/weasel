from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

from weasel.domain.entities.submission import SubmissionEntity


class TaskEntity(BaseModel):
    """The task entity."""

    name: str
    submissions: list[SubmissionEntity]

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def ensure_unique_names(self) -> Self:
        """Ensure that submission names are unique."""
        submission_names = {submission.name for submission in self.submissions}

        if len(submission_names) != len(self.submissions):
            detail = f"The submission names must be unique ({self.name!r})"
            raise ValueError(detail)

        return self
