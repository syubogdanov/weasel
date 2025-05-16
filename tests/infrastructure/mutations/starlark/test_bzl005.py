import pytest

from weasel.domain.services.interfaces.mutation import MutationInterface
from weasel.infrastructure.adapters.estimator import EstimatorAdapter
from weasel.infrastructure.mutations.starlark.bzl005 import StarlarkMutation


TARGET = """
def b():
    print('B')
    return 2

def a():
    print('A')
    return 1
"""

BEFORE = """
def a():
    print('A')
    return 1

def unused():
    print('This is unused')
    return 42

def b():
    print('B')
    return 2
"""

AFTER = """
def unused():
    print('This is unused')
    return 42

def b():
    print('B')
    return 2

def a():
    print('A')
    return 1
"""


@pytest.fixture
def mutation() -> MutationInterface:
    """Fixture the mutation."""
    estimator = EstimatorAdapter(_precision=3)
    return StarlarkMutation(_estimator=estimator)


class TestStarlarkMutation:
    """Test the mutation."""

    async def test__as_label(self, mutation: MutationInterface) -> None:
        """Test the `as_label` method."""
        assert mutation.as_label() == "BZL005"

    async def test__mutate(self, mutation: MutationInterface) -> None:
        """Test the `mutate` method."""
        after = await mutation.mutate(BEFORE, TARGET)

        assert after.strip() == AFTER.strip()
