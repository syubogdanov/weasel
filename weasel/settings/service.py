import tomllib

from functools import cached_property
from pathlib import Path
from typing import Self

from platformdirs import site_cache_dir
from pydantic import BaseModel


class Poetry(BaseModel):
    """The `tool.poetry` section."""

    name: str
    version: str


class Tool(BaseModel):
    """The `tool` section."""

    poetry: Poetry


class PyProject(BaseModel):
    """The `pyproject.toml` file."""

    tool: Tool

    @classmethod
    def from_path(cls, path: Path) -> Self:
        """Load the `pyproject.toml` file."""
        with Path(path).open(mode="rb") as file:
            return cls(**tomllib.load(file))


class ServiceSettings(BaseModel):
    """The service settings."""

    @cached_property
    def pyproject(self) -> PyProject:
        """Get the `pyproject.toml` file."""
        base_dir = Path(__file__).parent.parent.parent
        path = base_dir / "pyproject.toml"
        return PyProject.from_path(path)

    @property
    def name(self) -> str:
        """Get the service name."""
        return self.pyproject.tool.poetry.name

    @property
    def version(self) -> str:
        """Get the service version."""
        return self.pyproject.tool.poetry.version

    @property
    def cache_directory(self) -> Path:
        """Get the cache directory."""
        return Path(site_cache_dir(appname=self.name, version=self.version))
