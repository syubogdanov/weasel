from weasel.domain.services.interfaces.language import LanguageInterface


class StarlarkLanguage(LanguageInterface):
    """The *Starlark* language."""

    def recognizes(self, code: str) -> bool:
        """Check if code matches the language."""
        raise NotImplementedError

    @classmethod
    def get_extensions(cls) -> set[str]:
        """List the language extensions."""
        return {".BUILD", ".bazel", ".bzl", ".star"}
