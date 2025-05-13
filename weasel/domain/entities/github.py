from pydantic import BaseModel


class GitHubEntity(BaseModel):
    """The *GitHub* entity."""

    user: str
    repo: str

    branch: str | None = None
    commit: str | None = None
    tag: str | None = None
