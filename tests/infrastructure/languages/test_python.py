from typing import TYPE_CHECKING

import pytest

from weasel.domain.types.language import LanguageType
from weasel.infrastructure.languages.python import PythonLanguage


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
def python() -> "LanguageInterface":
    """Fixture for *Python*."""
    return PythonLanguage()


class TestPythonLanguage:
    """Tests for *Python*."""

    @pytest.mark.parametrize("text", [PYTHON, STARLARK])
    async def test__recognizes(self, python: "LanguageInterface", text: str) -> None:
        """Test the `recognizes` method."""
        is_python = await python.recognizes(text)

        assert is_python

    @pytest.mark.parametrize("text", [GOLANG, JAVA, SQL, TEXT])
    async def test__recognizes__false(self, python: "LanguageInterface", text: str) -> None:
        """Test the `recognizes` method. Case: not *Python*."""
        is_python = await python.recognizes(text)

        assert not is_python

    @pytest.mark.parametrize("extension", [".py", ".py3", ".pyi"])
    async def test__get_extensions(self, python: "LanguageInterface", extension: str) -> None:
        """Test the `get_extensions` method."""
        assert extension in python.get_extensions()

    @pytest.mark.parametrize("extension", [".java", ".js", ".md", ".rst", ".sql", ".txt"])
    async def test__get_extensions__false(
        self, python: "LanguageInterface", extension: str
    ) -> None:
        """Test the `get_extensions` method. Case: not *Python*."""
        assert extension not in python.get_extensions()

    async def test__as_type(self, python: "LanguageInterface") -> None:
        """Test the `as_type` method."""
        language = python.as_type()

        assert language == LanguageType.PYTHON
