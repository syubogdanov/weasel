import string

from pydantic import BaseModel, ConfigDict, field_validator

from weasel.domain.dtypes.gitref import GitRef
from weasel.domain.dtypes.sha1 import SHA1


class GitHubEntity(BaseModel):
    """The *GitHub* entity."""

    user: str
    repo: str

    branch: GitRef | None = None
    commit: SHA1 | None = None
    tag: GitRef | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("user")
    @classmethod
    def ensure_user(cls, user: str) -> str:
        """Ensure the user name is valid."""
        if not user:
            detail = "The GitHub username cannot be empty"
            raise ValueError(detail)

        if len(user) > 39:
            detail = "The GitHub username cannot be longer than 39 characters"
            raise ValueError(detail)

        chars = set(string.ascii_letters + string.digits + "-_")

        if not all(char in chars for char in user):
            detail = "The GitHub username can only contain alphanumeric characters"
            raise ValueError(detail)

        if user.startswith(("-", "_")) or user.endswith(("-", "_")):
            detail = "The GitHub username cannot start or end with a hyphen or underscore"
            raise ValueError(detail)

        if "--" in user or "__" in user:
            detail = "The GitHub username cannot contain two consecutive hyphens or underscores"
            raise ValueError(detail)

        return user

    @field_validator("repo")
    @classmethod
    def ensure_repo(cls, repo: str) -> str:
        """Ensure the repo name is valid."""
        if not repo:
            detail = "The GitHub repository name cannot be empty"
            raise ValueError(detail)

        if len(repo) > 100:
            detail = "The GitHub repository name cannot be longer than 100 characters"
            raise ValueError(detail)

        chars = set(string.ascii_letters + string.digits + "-_")

        if not all(char in chars for char in repo):
            detail = "The GitHub repository name can only contain alphanumeric characters"
            raise ValueError(detail)

        if repo.startswith(("-", "_")) or repo.endswith(("-", "_")):
            detail = "The GitHub repository name cannot start or end with a hyphen or underscore"
            raise ValueError(detail)

        if "--" in repo or "__" in repo:
            detail = "The GitHub repository name cannot contain two consecutive hyphens"
            raise ValueError(detail)

        return repo
