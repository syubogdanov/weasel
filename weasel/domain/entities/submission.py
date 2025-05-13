from pathlib import Path

from pydantic import BaseModel, ConfigDict

from weasel.domain.entities.bitbucket import BitbucketEntity
from weasel.domain.entities.github import GitHubEntity


class SubmissionEntity(BaseModel):
    """The submission entity."""

    name: str
    bitbucket: BitbucketEntity | None = None
    github: GitHubEntity | None = None
    path: Path | None = None

    model_config = ConfigDict(from_attributes=True)
