import asyncio

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from weasel.domain.entities.match import MatchEntity


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface
    from weasel.domain.services.interfaces.language import LanguageInterface
    from weasel.domain.services.interfaces.mutation_tree import MutationTreeInterface
    from weasel.domain.types.language import LanguageType


@dataclass
class MatcherService:
    """The matcher service."""

    _estimator: "EstimatorInterface"
    _languages: list["LanguageInterface"]
    _mutation_trees: dict["LanguageType", "MutationTreeInterface"]

    _encoding: ClassVar[str] = "utf-8"
    _errors: ClassVar[str] = "replace"

    async def maybe_match(self, source: Path, target: Path) -> MatchEntity | None:
        """Match `source` and `target` if possible."""
        for language in self._languages:
            extensions = language.get_extensions()

            if not extensions.issuperset({source.suffix, target.suffix}):
                continue

            source_text = await self._read_file(source)
            if not await language.recognizes(source_text):
                return None

            target_text = await self._read_file(target)
            if not await language.recognizes(target_text):
                return None

            mutation_tree = self._mutation_trees[language.as_type()]
            mutations = await mutation_tree.get_mutations(source_text, target_text)

            for mutation in mutations:
                source_text = await mutation.mutate(source_text, target_text)

            probability = await self._estimator.estimate(source_text, target_text)
            labels = [mutation.as_label() for mutation in mutations]

            return MatchEntity(
                source=source,
                target=target,
                language=language.as_type(),
                probability=probability,
                labels=labels,
            )

        return None

    @classmethod
    async def _read_file(cls, path: Path) -> str:
        """Read the file."""
        return await asyncio.to_thread(path.read_text, encoding=cls._encoding, errors=cls._errors)
