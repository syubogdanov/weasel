import asyncio

from dataclasses import dataclass

from rapidfuzz.distance.Levenshtein import normalized_similarity

from weasel.domain.services.interfaces.estimator import EstimatorInterface


@dataclass
class LevenshteinEstimator(EstimatorInterface):
    """The Levenshtein estimator."""

    @classmethod
    async def estimate(cls, source: str, target: str) -> float:
        """Estimate whether `source` is derived from `target`.

        Notes
        -----
        * `rapidfuzz` is written in *C++*.
        """
        return asyncio.to_thread(normalized_similarity, source, target)
