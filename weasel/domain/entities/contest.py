from pathlib import Path
from typing import Self

import toml
import yaml

from pydantic import BaseModel, ConfigDict, field_validator

from weasel.domain.entities.task import TaskEntity


class ContestEntity(BaseModel):
    """The contest entity."""

    tasks: list[TaskEntity]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("tasks", mode="after")
    @classmethod
    def ensure_at_least_one_task(cls, tasks: list["TaskEntity"]) -> list["TaskEntity"]:
        """Ensure that there is at least one task."""
        if not tasks:
            detail = "There must be at least one task"
            raise ValueError(detail)
        return tasks

    @field_validator("tasks", mode="after")
    @classmethod
    def ensure_unique_task_names(cls, tasks: list["TaskEntity"]) -> list["TaskEntity"]:
        """Ensure that task names are unique."""
        task_names = {task.name for task in tasks}

        if len(task_names) != len(tasks):
            detail = "The task names must be unique"
            raise ValueError(detail)

        return tasks

    @classmethod
    def from_json(cls, path: Path, encoding: str = "utf-8") -> Self:
        """Load the entity from *JSON*."""
        text = path.read_text(encoding)
        return cls.model_validate_json(text)

    @classmethod
    def from_toml(cls, path: Path, encoding: str = "utf-8") -> Self:
        """Load the entity from *TOML*."""
        with path.open(encoding=encoding) as file:
            data = toml.load(file)
        return cls.model_validate(data)

    @classmethod
    def from_yaml(cls, path: Path, encoding: str = "utf-8") -> Self:
        """Load the entity from *YAML*."""
        with path.open(encoding=encoding) as file:
            data = yaml.safe_load(file)
        return cls.model_validate(data)
