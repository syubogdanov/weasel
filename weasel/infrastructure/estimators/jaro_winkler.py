from dataclasses import dataclass

from rapidfuzz.distance.JaroWinkler import normalized_similarity

from weasel.domain.services.interfaces.estimator import EstimatorInterface


@dataclass(slots=True)
class JaroWinklerEstimator(EstimatorInterface):
    """The Jaro-Winkler estimator."""

    @classmethod
    def estimate(cls, source: str, target: str) -> float:
        """Estimate whether `source` is derived from `target`."""
        return normalized_similarity(source, target)
