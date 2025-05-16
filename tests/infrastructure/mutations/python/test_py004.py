import pytest

from weasel.domain.services.interfaces.mutation import MutationInterface
from weasel.infrastructure.mutations.python.py004 import PythonMutation


NO_TARGET = ""

BEFORE = """
def maybe_raise(who: str) -> None:
    if who:
        detail = 'This is a strange exception!'
        raise RuntimeError(detail)

        '''However, this code is unreachable...'''
        print('Hello,', who)
        if who == 'weasel':
            print('I love you, weasel!')
        print('Goodbye,', who)

    return 'who is an empty string'
    print('This is an unreachable code.')
for d in range(23):
    print(i)
    continue
    print('This is an unreachable code.')
    break
for m in range(4):
    print(i)
    break
    print('This is an unreachable code.')
"""

AFTER = """
def maybe_raise(who: str) -> None:
    if who:
        detail = 'This is a strange exception!'
        raise RuntimeError(detail)
    return 'who is an empty string'
for d in range(23):
    print(i)
    continue
for m in range(4):
    print(i)
    break
"""


@pytest.fixture
def mutation() -> MutationInterface:
    """Fixture the mutation."""
    return PythonMutation()


class TestPythonMutation:
    """Test the mutation."""

    async def test__as_label(self, mutation: MutationInterface) -> None:
        """Test the `as_label` method."""
        assert mutation.as_label() == "PY004"

    async def test__mutate(self, mutation: MutationInterface) -> None:
        """Test the `mutate` method."""
        after = await mutation.mutate(BEFORE, NO_TARGET)

        assert after.strip() == AFTER.strip()
