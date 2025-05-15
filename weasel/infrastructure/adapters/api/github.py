import asyncio

from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin
from uuid import UUID

import aiofiles
import aioshutil

from aiohttp import ClientResponseError, ServerConnectionError
from aiohttp.client import ClientSession
from aiostdlib import os

from weasel.domain.services.exceptions import WeaselConnectionError, WeaselError
from weasel.infrastructure.adapters.api.retries import retry_api


@dataclass
class GitHubAPIAdapter:
    """The *GitHub* API adapter."""

    _api_url: str
    _connect_timeout: float
    _data_dir: Path
    _id_factory: Callable[[], UUID]

    _chunk_size: int = 1024 * 1024  # 1 MB

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._github_dir = self._data_dir / "github"
        self._archive_dir = self._github_dir / "archive"
        self._extract_dir = self._github_dir / "extract"

    @retry_api
    async def download(self, user: str, repo: str, ref: str) -> Path:
        """Clone the repository."""
        path = f"/repos/{user}/{repo}/zipball/{ref}"
        url = urljoin(self._api_url, path)

        identifier = self._id_factory()
        archive_path = self._archive_dir / identifier.hex
        extract_path = self._extract_dir / identifier.hex

        await asyncio.gather(
            os.makedirs(self._archive_dir, exist_ok=True),
            os.makedirs(self._extract_dir, exist_ok=True),
        )

        try:
            async with (
                ClientSession(headers=self._headers, conn_timeout=self._connect_timeout) as session,
                session.get(url, allow_redirects=True, raise_for_status=True) as response,
                aiofiles.open(archive_path, mode="wb") as file,
            ):
                async for chunk in response.content.iter_chunked(self._chunk_size):
                    await file.write(chunk)

        except ServerConnectionError as exception:
            detail = f"GitHub: connection failed while downloading '{user}/{repo}@{ref}'"
            raise WeaselConnectionError(detail) from exception

        except ClientResponseError as exception:
            detail = f"GitHub: '{user}/{repo}@{ref}' is private or does not exist"
            raise FileNotFoundError(detail) from exception

        except Exception as exception:
            detail = f"GitHub: an error occurred while downloading '{user}/{repo}@{ref}'"
            raise WeaselError(detail) from exception

        await aioshutil.unpack_archive(archive_path, extract_path, format="zip")

        paths, _ = await asyncio.gather(os.listdir(extract_path), self._safe_unlink(archive_path))
        return extract_path / paths[0]

    @property
    def _headers(self) -> dict[str, str]:
        """Get the headers for the request."""
        return {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}

    @classmethod
    async def _safe_unlink(cls, path: Path) -> None:
        """Safely unlink a file."""
        with suppress(OSError):
            await os.unlink(path)
