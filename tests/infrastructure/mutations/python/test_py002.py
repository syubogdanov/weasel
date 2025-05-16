import pytest

from weasel.domain.services.interfaces.mutation import MutationInterface
from weasel.infrastructure.mutations.python.py002 import PythonMutation


NO_TARGET = ""

BEFORE = """
def f1(a1: str, a2: int = 2, *a3: dict[bytes, bytes], **a4: list[float]) -> None:
    print(a1, a2, a3, a4)

async def f2(a1: str, a2: int = 2, *a3: dict[bytes, bytes], **a4: list[float]) -> None:
    print(a1, a2, a3, a4)

class C:

    def f3(self, a1: object, a2: str = '2', *a3: tuple[str, str], **a4: list[float]) -> None:
        print(a1, a2, a3, a4)
"""

AFTER = """
def f1(a1, a2=2, *a3, **a4):
    print(a1, a2, a3, a4)

async def f2(a1, a2=2, *a3, **a4):
    print(a1, a2, a3, a4)

class C:

    def f3(self, a1, a2='2', *a3, **a4):
        print(a1, a2, a3, a4)
"""


@pytest.fixture
def mutation() -> MutationInterface:
    """Fixture the mutation."""
    return PythonMutation()


class TestPythonMutation:
    """Test the mutation."""

    async def test__as_label(self, mutation: MutationInterface) -> None:
        """Test the `as_label` method."""
        assert mutation.as_label() == "PY002"

    async def test__mutate(self, mutation: MutationInterface) -> None:
        """Test the `mutate` method."""
        after = await mutation.mutate(BEFORE, NO_TARGET)

        assert after.strip() == AFTER.strip()
