from dataclasses import dataclass

from rapidfuzz.distance.Levenshtein import normalized_similarity

from weasel.domain.services.interfaces.estimator import EstimatorInterface


@dataclass(slots=True)
class LevenshteinEstimator(EstimatorInterface):
    """The Levenshtein estimator."""

    @classmethod
    def estimate(cls, source: str, target: str) -> float:
        """Estimate whether `source` is derived from `target`."""
        return normalized_similarity(source, target)
