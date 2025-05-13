import tomllib

from functools import cached_property
from pathlib import Path
from typing import Self

from platformdirs import site_cache_dir, site_config_dir, site_data_dir
from pydantic import BaseModel, PositiveInt


class Poetry(BaseModel):
    """The `tool.poetry` section."""

    name: str
    version: str

    license: str
    authors: list[str]

    documentation: str
    homepage: str
    repository: str


class Tool(BaseModel):
    """The `tool` section."""

    poetry: Poetry


class PyProject(BaseModel):
    """The `pyproject.toml` file."""

    tool: Tool

    @classmethod
    def load(cls, path: Path) -> Self:
        """Load the `pyproject.toml` file."""
        with Path(path).open(mode="rb") as file:
            return cls(**tomllib.load(file))


class ServiceSettings(BaseModel):
    """The service settings."""

    precision: PositiveInt = 3

    @cached_property
    def pyproject(self) -> PyProject:
        """Get the `pyproject.toml` file."""
        base_dir = Path(__file__).parent.parent.parent
        path = base_dir / "pyproject.toml"
        return PyProject.load(path)

    @property
    def name(self) -> str:
        """Get the service name."""
        return self.pyproject.tool.poetry.name

    @property
    def version(self) -> str:
        """Get the service version."""
        return self.pyproject.tool.poetry.version

    @property
    def authors(self) -> list[str]:
        """Get the service authors."""
        return self.pyproject.tool.poetry.authors

    @property
    def license(self) -> str:
        """Get the service license."""
        return self.pyproject.tool.poetry.license

    @property
    def documentation(self) -> str:
        """Get the service documentation URL."""
        return self.pyproject.tool.poetry.documentation

    @property
    def homepage(self) -> str:
        """Get the service homepage URL."""
        return self.pyproject.tool.poetry.homepage

    @property
    def repository(self) -> str:
        """Get the service repository URL."""
        return self.pyproject.tool.poetry.repository

    @cached_property
    def cache_directory(self) -> Path:
        """Get the cache directory."""
        return Path(site_cache_dir(appname=self.name, version=self.version))

    @cached_property
    def config_directory(self) -> Path:
        """Get the config directory."""
        return Path(site_config_dir(appname=self.name, version=self.version))

    @cached_property
    def data_directory(self) -> Path:
        """Get the data directory."""
        return Path(site_data_dir(appname=self.name, version=self.version))
