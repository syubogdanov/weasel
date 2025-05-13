from pathlib import Path

import toml
import yaml

from pydantic import BaseModel, ConfigDict

from weasel.domain.entities.workflow import WorkflowEntity


class ManifestEntity(BaseModel):
    """The manifest entity."""

    workflows: list[WorkflowEntity]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_json(cls, path: Path, encoding: str = "utf-8") -> "ManifestEntity":
        """Load the entity from *JSON*."""
        text = path.read_text(encoding)
        return ManifestEntity.model_validate_json(text)

    @classmethod
    def from_toml(cls, path: Path, encoding: str = "utf-8") -> "ManifestEntity":
        """Load the entity from *TOML*."""
        with path.open(encoding=encoding) as file:
            data = toml.load(file)
        return ManifestEntity.model_validate(data)

    @classmethod
    def from_yaml(cls, path: Path, encoding: str = "utf-8") -> "ManifestEntity":
        """Load the entity from *YAML*."""
        with path.open(encoding=encoding) as file:
            data = yaml.safe_load(file)
        return ManifestEntity.model_validate(data)
