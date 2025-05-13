import statistics

from dataclasses import dataclass
from functools import reduce
from operator import mul

from weasel.domain.entities.metrics import MetricsEntity
from weasel.domain.services.interfaces.metrics import MetricsInterface


@dataclass
class MetricsAdapter(MetricsInterface):
    """The metrics adapter."""

    _precision: int

    def calculate(self, probabilities: list[float]) -> "MetricsEntity":
        """Calculate metrics based on probabilities."""
        return MetricsEntity(
            nolie=self._calculate_nolie(probabilities),
            mean=self._calculate_mean(probabilities),
            gmean=self._calculate_gmean(probabilities),
            median=self._calculate_median(probabilities),
            min=self._calculate_min(probabilities),
            max=self._calculate_max(probabilities),
            var=self._calculate_var(probabilities),
            std=self._calculate_std(probabilities),
            p75=self._calculate_p75(probabilities),
            p90=self._calculate_p90(probabilities),
            p95=self._calculate_p95(probabilities),
            p99=self._calculate_p99(probabilities),
            count=len(probabilities),
        )

    def _calculate_mean(self, probabilities: list[float]) -> float:
        """Calculate the mean."""
        value = statistics.mean(probabilities) if probabilities else 0.0
        return round(value, self._precision)

    def _calculate_gmean(self, probabilities: list[float]) -> float:
        """Calculate the geometric mean."""
        value = statistics.geometric_mean(probabilities) if probabilities else 0.0
        return round(value, self._precision)

    def _calculate_median(self, probabilities: list[float]) -> float:
        """Calculate the median."""
        value = statistics.median(probabilities) if probabilities else 0.0
        return round(value, self._precision)

    def _calculate_min(self, probabilities: list[float]) -> float:
        """Calculate the minimum."""
        value = min(probabilities) if probabilities else 0.0
        return round(value, self._precision)

    def _calculate_max(self, probabilities: list[float]) -> float:
        """Calculate the maximum."""
        value = max(probabilities) if probabilities else 0.0
        return round(value, self._precision)

    def _calculate_var(self, probabilities: list[float]) -> float:
        """Calculate the variance."""
        value = statistics.variance(probabilities) if probabilities else 0.0
        return round(value, self._precision)

    def _calculate_std(self, probabilities: list[float]) -> float:
        """Calculate the standard deviation."""
        value = statistics.stdev(probabilities) if probabilities else 0.0
        return round(value, self._precision)

    def _calculate_p75(self, probabilities: list[float]) -> float:
        """Calculate the 75th percentile."""
        value = statistics.quantiles(probabilities, n=4)[2] if probabilities else 0.0
        return round(value, self._precision)

    def _calculate_p90(self, probabilities: list[float]) -> float:
        """Calculate the 90th percentile."""
        if not probabilities:
            return 0.0

        intervals = statistics.quantiles(probabilities, n=10)
        return round(intervals[8], self._precision)

    def _calculate_p95(self, probabilities: list[float]) -> float:
        """Calculate the 95th percentile."""
        if not probabilities:
            return 0.0

        intervals = statistics.quantiles(probabilities, n=20)
        return round(intervals[18], self._precision)

    def _calculate_p99(self, probabilities: list[float]) -> float:
        """Calculate the 99th percentile."""
        if not probabilities:
            return 0.0

        intervals = statistics.quantiles(probabilities, n=100)
        return round(intervals[98], self._precision)

    def _calculate_nolie(self, probabilities: list[float]) -> float:
        """Calculate the *NO-LIE* metric."""
        if not probabilities:
            return 0.0

        if (maximum := max(probabilities)) < 0.5:
            return round(maximum, self._precision)

        plus = [proba for proba in probabilities if proba >= 0.5]
        minus = [1.0 - proba for proba in plus]

        numerator = reduce(mul, plus)
        denominator = numerator + reduce(mul, minus)

        return round(numerator / denominator, self._precision)
