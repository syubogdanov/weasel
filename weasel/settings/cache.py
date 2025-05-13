from pathlib import Path

from pydantic import BaseModel, NonNegativeInt


class CacheSettings(BaseModel):
    """The cache settings."""

    # The DiskCache directory.
    directory: Path
    # The number of shards.
    shards: NonNegativeInt = 8
    # The cache size limit (bytes).
    size_limit: NonNegativeInt = 4 * 1024 * 1024 * 1024  # 4 GiB

    @property
    def uri(self) -> str:
        """Get the URI."""
        return "disk://"
