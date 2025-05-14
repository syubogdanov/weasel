import json

from pathlib import Path

import toml
import yaml

from pydantic import BaseModel, ConfigDict

from weasel.domain.entities.review import ReviewEntity


class ReportEntity(BaseModel):
    """The report entity."""

    reviews: list[ReviewEntity]

    model_config = ConfigDict(from_attributes=True)

    def to_json(
        self,
        path: Path,
        *,
        indent: int | None = None,
        encoding: str = "utf-8",
        sort_keys: bool = False,
    ) -> None:
        """Dump the entity as *JSON*."""
        data = self.model_dump(mode="json")
        with path.open(mode="w", encoding=encoding) as file:
            json.dump(data, file, indent=indent, sort_keys=sort_keys)

    def to_toml(self, path: Path, encoding: str = "utf-8") -> None:
        """Dump the entity as *TOML*."""
        data = self.model_dump(mode="json")
        with path.open(mode="w", encoding=encoding) as file:
            toml.dump(data, file)

    def to_yaml(
        self,
        path: Path,
        *,
        indent: int | None = None,
        encoding: str = "utf-8",
        sort_keys: bool = False,
    ) -> None:
        """Dump the entity as *YAML*."""
        data = self.model_dump(mode="json")
        with path.open(mode="w", encoding=encoding) as file:
            yaml.safe_dump(data, file, default_flow_style=False, indent=indent, sort_keys=sort_keys)
