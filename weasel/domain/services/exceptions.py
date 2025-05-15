class WeaselError(Exception):
    """Base class for all exceptions."""


class WeaselConnectionError(WeaselError, ConnectionError):
    """Raised when there is a connection error."""


class WeaselCacheError(WeaselError):
    """Raised when there is a cache error."""
