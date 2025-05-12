from os import cpu_count

from pydantic import BaseModel


class SystemSettings(BaseModel):
    """The system settings."""

    @property
    def threads(self) -> int:
        """Get the number of threads."""
        return cpu_count() or 1

    @property
    def workers(self) -> int:
        """Get the number of workers."""
        return min(self.threads + 4, 32)
