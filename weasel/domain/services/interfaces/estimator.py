from abc import abstractmethod
from typing import Protocol


class EstimatorInterface(Protocol):
    """The estimator interface."""

    @abstractmethod
    def estimate(self, source: str, target: str) -> float:
        """Estimate whether `source` is derived from `target`."""
