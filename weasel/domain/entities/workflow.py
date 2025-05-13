from pydantic import BaseModel

from weasel.domain.entities.task import TaskEntity


class WorkflowEntity(BaseModel):
    """The workflow entity."""

    name: str
    tasks: list[TaskEntity]
