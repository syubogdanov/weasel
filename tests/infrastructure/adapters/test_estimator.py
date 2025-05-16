from math import isclose

import pytest

from weasel.domain.services.interfaces.estimator import EstimatorInterface
from weasel.infrastructure.adapters.estimator import EstimatorAdapter


@pytest.fixture
def estimator() -> EstimatorInterface:
    """Fixture the estimator."""
    return EstimatorAdapter(_precision=3)


class TestEstimatorAdapter:
    """Test the estimator."""

    @pytest.mark.parametrize(
        ("source", "target", "expected_probability"),
        [
            ("", "", 1.0),
            ("", "a", 0.0),
            ("a", "", 0.0),
            ("a", "a", 1.0),
            ("a", "b", 0.0),
            ("a", "ab", 0.5),
            ("ab", "a", 0.5),
            ("ab", "b", 0.5),
            ("ab", "c", 0.0),
            ("ab", "abc", 0.667),
            ("abc", "ab", 0.667),
            ("abc", "a", 0.333),
            ("abc", "b", 0.333),
            ("abc", "c", 0.333),
            ("abc", "abcd", 0.75),
            ("abcd", "abc", 0.75),
            ("abcd", "a", 0.25),
            ("abcd", "b", 0.25),
            ("abcd", "c", 0.25),
            ("abcd", "d", 0.25),
            ("abcde", "abcde", 1.0),
            ("abc", "def", 0.0),
            ("abcd", "defg", 0.0),
        ],
    )
    async def test__estimate(
        self, estimator: EstimatorInterface, source: str, target: str, expected_probability: float
    ) -> None:
        """Test the `estimate` method."""
        actual_probability = await estimator.estimate(source, target)

        assert isclose(actual_probability, expected_probability)
