from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    from weasel.domain.dtypes.probability import Probability


class EstimatorInterface(Protocol):
    """The estimator interface."""

    @abstractmethod
    async def estimate(self, source: str, target: str) -> "Probability":
        """Estimate whether `source` is derived from `target`."""
