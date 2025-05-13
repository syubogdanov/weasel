from pydantic import BaseModel


class BitbucketEntity(BaseModel):
    """The *Bitbucket* entity."""

    user: str
    repo: str

    branch: str | None = None
    commit: str | None = None
    tag: str | None = None
