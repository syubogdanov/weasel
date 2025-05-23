import asyncio

from dataclasses import dataclass
from typing import TYPE_CHECKING

from rapidfuzz.distance.Levenshtein import normalized_similarity

from weasel.domain.services.interfaces.estimator import EstimatorInterface


if TYPE_CHECKING:
    from weasel.domain.dtypes.probability import Probability


@dataclass
class EstimatorAdapter(EstimatorInterface):
    """The estimator adapter."""

    _precision: int

    async def estimate(self, source: str, target: str) -> "Probability":
        """Estimate whether `source` is derived from `target`.

        Notes
        -----
        * `rapidfuzz` is written in *C++*.
        """
        probability = await asyncio.to_thread(normalized_similarity, source, target)
        return round(probability, self._precision)
