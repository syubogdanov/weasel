from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from weasel.domain.services.interfaces.git import GitInterface


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.cache import CacheInterface


@dataclass
class BitbucketAdapter(GitInterface):
    """The *Bitbucket* adapter."""

    _cache: "CacheInterface"

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
        raise NotImplementedError
