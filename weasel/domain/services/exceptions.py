class WeaselError(Exception):
    """Base class for all exceptions."""


class WeaselCacheError(WeaselError):
    """Raised when there is a cache error."""
