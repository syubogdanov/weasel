from rapidfuzz.distance.DamerauLevenshtein import normalized_similarity

from weasel.domain.services.interfaces.estimator import EstimatorInterface


class DamerauLevenshteinEstimator(EstimatorInterface):
    """The Damerau-Levenshtein estimator."""

    @classmethod
    def estimate(cls, source: str, target: str) -> float:
        """Estimate whether `source` is derived from `target`."""
        return normalized_similarity(source, target)
