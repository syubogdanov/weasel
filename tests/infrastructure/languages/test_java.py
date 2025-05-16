from typing import TYPE_CHECKING

import pytest

from weasel.domain.types.language import LanguageType
from weasel.infrastructure.languages.java import JavaLanguage


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
def java() -> "LanguageInterface":
    """Fixture for *Java*."""
    return JavaLanguage()


class TestJavaLanguage:
    """Tests for *Java*."""

    async def test__recognizes(self, java: "LanguageInterface") -> None:
        """Test the `recognizes` method."""
        is_java = await java.recognizes(JAVA)

        assert is_java

    @pytest.mark.parametrize("text", [GOLANG, PYTHON, SQL, STARLARK, TEXT])
    async def test__recognizes__false(self, java: "LanguageInterface", text: str) -> None:
        """Test the `recognizes` method. Case: not *Java*."""
        is_java = await java.recognizes(text)

        assert not is_java

    @pytest.mark.parametrize("extension", [".jav", ".java"])
    async def test__get_extensions(self, java: "LanguageInterface", extension: str) -> None:
        """Test the `get_extensions` method."""
        assert extension in java.get_extensions()

    @pytest.mark.parametrize("extension", [".js", ".py", ".sql", ".txt"])
    async def test__get_extensions__false(self, java: "LanguageInterface", extension: str) -> None:
        """Test the `get_extensions` method. Case: not *Java*."""
        assert extension not in java.get_extensions()

    async def test__as_type(self, java: "LanguageInterface") -> None:
        """Test the `as_type` method."""
        language = java.as_type()

        assert language == LanguageType.JAVA
