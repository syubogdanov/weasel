from pydantic import BaseModel

from weasel.domain.entities.workflow import WorkflowEntity


class ManifestEntity(BaseModel):
    """The manifest entity."""

    workflows: list[WorkflowEntity]
