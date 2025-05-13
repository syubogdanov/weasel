from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

from weasel.domain.entities.bitbucket import BitbucketEntity
from weasel.domain.entities.github import GitHubEntity


class SubmissionEntity(BaseModel):
    """The submission entity."""

    name: str
    bitbucket: BitbucketEntity | None = None
    github: GitHubEntity | None = None
    path: Path | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def ensure_source(self) -> Self:
        """Ensure exactly one source is specified."""
        sources = [self.bitbucket, self.github, self.path]
        count = sum(map(bool, sources))

        if not count:
            detail = f"No sources are specified ({self.name!r})"
            raise ValueError(detail)

        if count > 1:
            detail = f"Exactly one source must be specified ({self.name!r})"
            raise ValueError(detail)

        return self
