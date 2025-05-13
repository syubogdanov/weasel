from pathlib import Path
from typing import Self

import toml
import yaml

from pydantic import BaseModel, ConfigDict

from weasel.domain.entities.task import TaskEntity


class ContestEntity(BaseModel):
    """The contest entity."""

    workflows: list[TaskEntity]

    model_config = ConfigDict(from_attributes=True)

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
