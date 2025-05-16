import string

from typing import Self

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from weasel.domain.dtypes.gitref import GitRef
from weasel.domain.dtypes.sha1 import SHA1


class BitbucketEntity(BaseModel):
    """The *Bitbucket* entity."""

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
            detail = "The Bitbucket username cannot be empty"
            raise ValueError(detail)

        if len(user) < 3:
            detail = "The Bitbucket username must be at least 3 characters long"
            raise ValueError(detail)

        if len(user) > 30:
            detail = "The Bitbucket username cannot be longer than 30 characters"
            raise ValueError(detail)

        chars = set(string.ascii_letters + string.digits + "-_")

        if not all(char in chars for char in user):
            detail = "The Bitbucket username can only contain alphanumeric characters"
            raise ValueError(detail)

        if user.startswith(("-", "_")) or user.endswith(("-", "_")):
            detail = "The Bitbucket username cannot start or end with a hyphen or underscore"
            raise ValueError(detail)

        if "--" in user or "__" in user:
            detail = "The Bitbucket username cannot contain two consecutive hyphens or underscores"
            raise ValueError(detail)

        return user

    @field_validator("repo")
    @classmethod
    def ensure_repo(cls, repo: str) -> str:
        """Ensure the repo name is valid."""
        if not repo:
            detail = "The Bitbucket repository name cannot be empty"
            raise ValueError(detail)

        if len(repo) > 62:
            detail = "The Bitbucket repository name cannot be longer than 100 characters"
            raise ValueError(detail)

        chars = set(string.ascii_letters + string.digits + "-_")

        if not all(char in chars for char in repo):
            detail = "The Bitbucket repository name can only contain alphanumeric characters"
            raise ValueError(detail)

        if repo.startswith(("-", "_")) or repo.endswith(("-", "_")):
            detail = "The Bitbucket repository name cannot start or end with a hyphen or underscore"
            raise ValueError(detail)

        if "--" in repo or "__" in repo:
            detail = "The Bitbucket repository name cannot contain two consecutive hyphens"
            raise ValueError(detail)

        return repo

    @model_validator(mode="after")
    def ensure__no_more_than_one_ref(self) -> Self:
        """Ensure that only one of branch, commit or tag is provided."""
        if self.branch and self.commit and self.tag:
            detail = "All three branch, commit and tag provided"
            raise ValueError(detail)

        if self.branch and self.commit:
            detail = "Both branch and commit provided"
            raise ValueError(detail)

        if self.branch and self.tag:
            detail = "Both branch and tag provided"
            raise ValueError(detail)

        if self.commit and self.tag:
            detail = "Both commit and tag provided"
            raise ValueError(detail)

        return self
