from dataclasses import dataclass
from typing import TYPE_CHECKING

from weasel.domain.services.interfaces.cache import CacheInterface


if TYPE_CHECKING:
    from weasel.infrastructure.adapters.cashews.cache import CacheCashewsAdapter


@dataclass
class CacheAdapter(CacheInterface):
    """The cache adapter."""

    _cashews: "CacheCashewsAdapter"

    async def get(self, bucket: str, key: str) -> str | None:
        """Get the value for `key`."""
        primary_key = self._build_key(bucket, key)
        return await self._cashews.get(primary_key)

    async def put(self, bucket: str, key: str, value: str) -> None:
        """Put the value for `key`."""
        primary_key = self._build_key(bucket, key)
        await self._cashews.put(primary_key, value)

    @classmethod
    def _build_key(cls, bucket: str, key: str) -> str:
        """Build the *Cashews* key."""
        return f"{bucket}:{key}"
