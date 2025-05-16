import pytest

from weasel.domain.services.interfaces.mutation import MutationInterface
from weasel.infrastructure.adapters.estimator import EstimatorAdapter
from weasel.infrastructure.mutations.python.py006 import PythonMutation


TARGET = """
def b():
    print('B')
    return 2

def a():
    print('A')
    return 1

class B:

    def method2(self):
        return 'method2'

    def method1(self):
        return 'method1'

class A:

    def method(self):
        x = 10
        return x * 2
"""

BEFORE = """
def a():
    print('A')
    return 1

def unused():
    print('This is unused')
    return 42

class A:

    def method(self):
        x = 10
        return x * 2

def b():
    print('B')
    return 2

class B:

    def method1(self):
        return 'method1'

    def method2(self):
        return 'method2'
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

class B:

    def method2(self):
        return 'method2'

    def method1(self):
        return 'method1'

class A:

    def method(self):
        x = 10
        return x * 2
"""


@pytest.fixture
def mutation() -> MutationInterface:
    """Fixture the mutation."""
    estimator = EstimatorAdapter(_precision=3)
    return PythonMutation(_estimator=estimator)


class TestPythonMutation:
    """Test the mutation."""

    async def test__as_label(self, mutation: MutationInterface) -> None:
        """Test the `as_label` method."""
        assert mutation.as_label() == "PY006"

    async def test__mutate(self, mutation: MutationInterface) -> None:
        """Test the `mutate` method."""
        after = await mutation.mutate(BEFORE, TARGET)

        assert after.strip() == AFTER.strip()
