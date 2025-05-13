from dataclasses import dataclass
from typing import TYPE_CHECKING

from cashews import cache

from weasel.domain.services.exceptions import WeaselCacheError
from weasel.infrastructure.adapters.cashews.retries import retry_cashews


if TYPE_CHECKING:
    from weasel.settings.cache import CacheSettings


@dataclass
class CacheCashewsAdapter:
    """The *Cashews* adapter."""

    _settings: "CacheSettings"

    def __post_init__(self) -> None:
        """Initialize the object."""
        cache.setup(
            self._settings.uri,
            directory=self._settings.directory,
            shards=self._settings.shards,
            size_limit=self._settings.size_limit,
        )

    @retry_cashews
    async def get(self, key: str) -> str | None:
        """Get the value for `key`."""
        try:
            value = await cache.get(key)

        except Exception as exception:
            detail = "Failed to get the key-value from the cache"
            raise WeaselCacheError(detail) from exception

        return value

    @retry_cashews
    async def put(self, key: str, value: str) -> None:
        """Put the value for `key`."""
        try:
            await cache.set(key, value)

        except Exception as exception:
            detail = "Failed to set the key-value in the cache"
            raise WeaselCacheError(detail) from exception

    @retry_cashews
    async def clean(self) -> None:
        """Clean the cache."""
        try:
            await cache.clear()

        except Exception as exception:
            detail = "Failed to clean up the cache"
            raise WeaselCacheError(detail) from exception
