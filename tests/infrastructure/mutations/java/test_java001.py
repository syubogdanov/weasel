import pytest

from weasel.domain.services.interfaces.mutation import MutationInterface
from weasel.infrastructure.mutations.java.java001 import JavaMutation


NO_TARGET = ""

BEFORE = """\
/*
* This is a comment
*/

public class Test {
    // This is a public static void main
    static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}\
"""

AFTER = """\
public class Test {
    static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}\
"""


@pytest.fixture
def mutation() -> MutationInterface:
    """Fixture the mutation."""
    return JavaMutation()


class TestJavaMutation:
    """Test the mutation."""

    async def test__as_label(self, mutation: MutationInterface) -> None:
        """Test the `as_label` method."""
        assert mutation.as_label() == "JAVA001"

    async def test__mutate(self, mutation: MutationInterface) -> None:
        """Test the `mutate` method."""
        after = await mutation.mutate(BEFORE, NO_TARGET)

        assert after == AFTER
