from typing import TYPE_CHECKING

import pytest

from weasel.domain.types.language import LanguageType
from weasel.infrastructure.languages.sql import SQLLanguage


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
def sql() -> "LanguageInterface":
    """Fixture for *SQL*."""
    return SQLLanguage()


class TestSQLLanguage:
    """Tests for *SQL*."""

    async def test__recognizes(self, sql: "LanguageInterface") -> None:
        """Test the `recognizes` method."""
        is_sql = await sql.recognizes(SQL)

        assert is_sql

    @pytest.mark.parametrize("text", [GOLANG, JAVA, PYTHON, STARLARK, TEXT])
    async def test__recognizes__false(self, sql: "LanguageInterface", text: str) -> None:
        """Test the `recognizes` method. Case: not *SQL*."""
        is_sql = await sql.recognizes(text)

        assert not is_sql

    @pytest.mark.parametrize("extension", [".ddl", ".dml", ".sql"])
    async def test__get_extensions(self, sql: "LanguageInterface", extension: str) -> None:
        """Test the `get_extensions` method."""
        assert extension in sql.get_extensions()

    @pytest.mark.parametrize("extension", [".java", ".js", ".py", ".rst", ".txt"])
    async def test__get_extensions__false(self, sql: "LanguageInterface", extension: str) -> None:
        """Test the `get_extensions` method. Case: not *SQL*."""
        assert extension not in sql.get_extensions()

    async def test__as_type(self, sql: "LanguageInterface") -> None:
        """Test the `as_type` method."""
        language = sql.as_type()

        assert language == LanguageType.SQL
