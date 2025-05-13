from pydantic import BaseModel, ConfigDict

from weasel.domain.entities.task import TaskEntity


class WorkflowEntity(BaseModel):
    """The workflow entity."""

    name: str
    tasks: list[TaskEntity]

    model_config = ConfigDict(from_attributes=True)
