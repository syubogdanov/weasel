import pytest

from weasel.domain.services.interfaces.mutation import MutationInterface
from weasel.infrastructure.mutations.starlark.bzl001 import StarlarkMutation


NO_TARGET = ""

BEFORE = """
def pep8() -> None:
    print(1+2+3+4+5)

# There are some comments
# 1. This is a comment
# 2. This is another comment
"""

AFTER = """
def pep8() -> None:
    print(1 + 2 + 3 + 4 + 5)
"""


@pytest.fixture
def mutation() -> MutationInterface:
    """Fixture the mutation."""
    return StarlarkMutation()


class TestStarlarkMutation:
    """Test the mutation."""

    async def test__as_label(self, mutation: MutationInterface) -> None:
        """Test the `as_label` method."""
        assert mutation.as_label() == "BZL001"

    async def test__mutate(self, mutation: MutationInterface) -> None:
        """Test the `mutate` method."""
        after = await mutation.mutate(BEFORE, NO_TARGET)

        assert after.strip() == AFTER.strip()
