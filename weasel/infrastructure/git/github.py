from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from aiostdlib import os

from weasel.domain.services.exceptions import WeaselCacheError
from weasel.domain.services.interfaces.git import GitInterface


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.cache import CacheInterface
    from weasel.infrastructure.adapters.api.github import GitHubAPIAdapter


@dataclass
class GitHubAdapter(GitInterface):
    """The *GitHub* adapter."""

    _cache: "CacheInterface"
    _github: "GitHubAPIAdapter"

    _bucket: ClassVar[str] = "github"
    _headref: ClassVar[str] = "HEAD"

    async def clone(
        self,
        user: str,
        repo: str,
        *,
        branch: str | None,
        commit: str | None = None,
        tag: str | None = None,
    ) -> Path:
        """Clone the repository."""
        ref = commit or branch or tag or self._headref
        key = self._build_key(user, repo, ref)

        if ref != self._headref and (cached := await self._maybe_from_cache(key)):
            return cached

        path = await self._github.download(user, repo, ref)

        with suppress(WeaselCacheError):
            await self._cache.put(self._bucket, key, path.as_posix())

        return path

    async def _maybe_from_cache(self, key: str) -> Path | None:
        """Get the repository from the cache if exists."""
        try:
            cached = await self._cache.get(self._bucket, key)
        except WeaselCacheError:
            return None

        if not cached:
            return None

        return Path(cached) if await os.path.exists(cached) else None

    @classmethod
    def _build_key(cls, user: str, repo: str, ref: str) -> str:
        """Build the cache key."""
        return f"{user}:{repo}:{ref}"
