from dataclasses import dataclass

from weasel.infrastructure.adapters.cashews.retries import retry_cashews


@dataclass
class CacheCashewsAdapter:
    """The *Cashews* adapter."""

    @retry_cashews
    async def get(self, key: str) -> str | None:
        """Get the value for `key`."""
        raise NotImplementedError

    @retry_cashews
    async def put(self, key: str, value: str) -> None:
        """Put the value for `key`."""
        raise NotImplementedError
