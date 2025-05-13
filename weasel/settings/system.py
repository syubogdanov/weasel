from os import cpu_count

from pydantic import BaseModel


class SystemSettings(BaseModel):
    """The system settings."""

    @property
    def max_threads(self) -> int:
        """Get the maximum number of threads."""
        return cpu_count() or 1

    @property
    def max_workers(self) -> int:
        """Get the maximum number of workers."""
        return min(self.max_threads + 4, 32)
