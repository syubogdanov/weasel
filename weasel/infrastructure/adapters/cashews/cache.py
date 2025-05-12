from dataclasses import dataclass


@dataclass
class CacheCashewsAdapter:
    """The *Cashews* adapter."""

    async def get(self, key: str) -> str | None:
        """Get the value for `key`."""
        raise NotImplementedError

    async def put(self, key: str, value: str) -> None:
        """Put the value for `key`."""
        raise NotImplementedError
