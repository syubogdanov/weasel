import pytest

from weasel.domain.services.interfaces.mutation import MutationInterface
from weasel.infrastructure.mutations.python.py005 import PythonMutation


NO_TARGET = ""

BEFORE = """
1 + 1
2 * 2
3 ** 3
4 / 4
5 // 5
6 % 6
7 & 7
8 | 8
9 ^ 9
10 << 10
11 >> 11
-(-12)
+(+13)
(not (not False))
(True or False)
"""

AFTER = """
2
4
27
1.0
1
0
7
8
0
10240
0
12
13
False
True
"""


@pytest.fixture
def mutation() -> MutationInterface:
    """Fixture the mutation."""
    return PythonMutation()


class TestPythonMutation:
    """Test the mutation."""

    async def test__as_label(self, mutation: MutationInterface) -> None:
        """Test the `as_label` method."""
        assert mutation.as_label() == "PY005"

    async def test__mutate(self, mutation: MutationInterface) -> None:
        """Test the `mutate` method."""
        after = await mutation.mutate(BEFORE, NO_TARGET)

        assert after.strip() == AFTER.strip()
