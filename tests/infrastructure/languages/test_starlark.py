from typing import TYPE_CHECKING

import pytest

from weasel.domain.types.language import LanguageType
from weasel.infrastructure.languages.starlark import StarlarkLanguage


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.language import LanguageInterface


GOLANG = """
package main
import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
"""

JAVA = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""

PYTHON = """
def hello_world() -> None:
    print("Hello, World!")
"""

SQL = """
SELECT 'Hello, World!';
"""

STARLARK = """
def hello_world():
    print("Hello, World!")
"""

TEXT = """
Hello, World!
"""


@pytest.fixture
def starlark() -> "LanguageInterface":
    """Fixture for *Starlark*."""
    return StarlarkLanguage()


class TestStarlarkLanguage:
    """Tests for *Starlark*."""

    async def test__recognizes(self, starlark: "LanguageInterface") -> None:
        """Test the `recognizes` method."""
        is_starlark = await starlark.recognizes(STARLARK)

        assert is_starlark

    @pytest.mark.parametrize("text", [GOLANG, JAVA, PYTHON, SQL, TEXT])
    async def test__recognizes__false(self, starlark: "LanguageInterface", text: str) -> None:
        """Test the `recognizes` method. Case: not *Starlark*."""
        is_starlark = await starlark.recognizes(text)

        assert not is_starlark

    @pytest.mark.parametrize("extension", [".BUILD", ".bazel", ".bzl", ".star"])
    async def test__get_extensions(self, starlark: "LanguageInterface", extension: str) -> None:
        """Test the `get_extensions` method."""
        assert extension in starlark.get_extensions()

    @pytest.mark.parametrize("extension", [".java", ".js", ".md", ".rst", ".py", ".sql", ".txt"])
    async def test__get_extensions__false(
        self, starlark: "LanguageInterface", extension: str
    ) -> None:
        """Test the `get_extensions` method. Case: not *Starlark*."""
        assert extension not in starlark.get_extensions()

    async def test__as_type(self, starlark: "LanguageInterface") -> None:
        """Test the `as_type` method."""
        language = starlark.as_type()

        assert language == LanguageType.STARLARK
