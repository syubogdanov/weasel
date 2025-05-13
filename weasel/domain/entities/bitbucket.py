from pydantic import BaseModel, ConfigDict


class BitbucketEntity(BaseModel):
    """The *Bitbucket* entity."""

    user: str
    repo: str

    branch: str | None = None
    commit: str | None = None
    tag: str | None = None

    model_config = ConfigDict(from_attributes=True)
