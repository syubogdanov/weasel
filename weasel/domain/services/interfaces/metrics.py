from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    from weasel.domain.entities.metrics import MetricsEntity


class MetricsInterface(Protocol):
    """The metrics interface."""

    @abstractmethod
    def calculate(self, probabilities: list[float]) -> "MetricsEntity":
        """Calculate metrics based on probabilities."""
