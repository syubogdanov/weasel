import pytest

from weasel.domain.services.interfaces.mutation import MutationInterface
from weasel.infrastructure.mutations.starlark.bzl002 import StarlarkMutation


NO_TARGET = ""

BEFORE = """
True
False


def function(who) -> None:
    '''This is a docstring.'''
    print('Hello,', who)

1
2
3

'I am an unused string.'
"""

AFTER = """
def function(who) -> None:
    print('Hello,', who)
"""


@pytest.fixture
def mutation() -> MutationInterface:
    """Fixture the mutation."""
    return StarlarkMutation()


class TestStarlarkMutation:
    """Test the mutation."""

    async def test__as_label(self, mutation: MutationInterface) -> None:
        """Test the `as_label` method."""
        assert mutation.as_label() == "BZL002"

    async def test__mutate(self, mutation: MutationInterface) -> None:
        """Test the `mutate` method."""
        after = await mutation.mutate(BEFORE, NO_TARGET)

        assert after.strip() == AFTER.strip()
