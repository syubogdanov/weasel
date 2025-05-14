import asyncio

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from weasel.domain.entities.comparison import ComparisonEntity
from weasel.domain.entities.contest import ContestEntity
from weasel.domain.entities.match import MatchEntity
from weasel.domain.entities.report import ReportEntity
from weasel.domain.entities.review import ReviewEntity
from weasel.domain.entities.submission import SubmissionEntity
from weasel.domain.entities.task import TaskEntity


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface
    from weasel.domain.services.interfaces.git import GitInterface
    from weasel.domain.services.interfaces.language import LanguageInterface
    from weasel.domain.services.interfaces.mutation_tree import MutationTreeInterface
    from weasel.domain.services.interfaces.sealer import SealerInterface
    from weasel.domain.types.language import LanguageType


@dataclass
class ScannerService:
    """The scanner service."""

    _bitbucket: "GitInterface"
    _estimator: "EstimatorInterface"
    _github: "GitInterface"
    _languages: list["LanguageInterface"]
    _mutation_trees: dict["LanguageType", "MutationTreeInterface"]
    _sealer: "SealerInterface"

    _encoding: ClassVar[str] = "utf-8"
    _errors: ClassVar[str] = "replace"

    async def scan(self, contest: "ContestEntity") -> "ReportEntity":
        """Scan the contest and return a report."""
        contest = await self._seal_contest(contest)
        coroutines = [self._review(task) for task in contest.tasks]
        reviews = await asyncio.gather(*coroutines)
        return ReportEntity(reviews=reviews)

    async def _review(self, task: "TaskEntity") -> "ReviewEntity":
        """Review the task."""
        coroutines = [self._compare(s1, s2) for s1, s2 in combinations(task.submissions, r=2)]
        comparisons = await asyncio.gather(*coroutines)
        return ReviewEntity(name=task.name, comparisons=comparisons)

    async def _compare(self, s1: "SubmissionEntity", s2: "SubmissionEntity") -> "ComparisonEntity":
        """Compare submissions."""
        return ComparisonEntity(
            source=s1.name,
            target=s2.name,
            metrics=...,
            matches=[],
        )

    async def _maybe_match(self, source: Path, target: Path) -> MatchEntity | None:
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

    async def _seal_contest(self, contest: "ContestEntity") -> None:
        """Seal the contest."""
        coroutines = [self._seal_task(task) for task in contest.tasks]
        tasks = await asyncio.gather(*coroutines)
        return ContestEntity(tasks=tasks)

    async def _seal_task(self, task: "TaskEntity") -> "TaskEntity":
        """Seal the task."""
        coroutines = [self._seal_submission(submission) for submission in task.submissions]
        submissions = await asyncio.gather(*coroutines)
        return TaskEntity(name=task.name, submissions=submissions)

    async def _seal_submission(self, submission: "SubmissionEntity") -> "SubmissionEntity":
        """Seal the submission."""
        path = await self._maybe_download(submission)
        path = await self._sealer.seal(path)
        return SubmissionEntity(name=submission.name, path=path)

    async def _maybe_download(self, submission: "SubmissionEntity") -> Path:
        """Download the submission if required."""
        if submission.bitbucket:
            return await self._bitbucket.clone(
                user=submission.bitbucket.user,
                repo=submission.bitbucket.repo,
                commit=submission.bitbucket.commit,
                branch=submission.bitbucket.branch,
                tag=submission.bitbucket.tag,
            )

        if submission.github:
            return await self._github.clone(
                user=submission.github.user,
                repo=submission.github.repo,
                commit=submission.github.commit,
                branch=submission.github.branch,
                tag=submission.github.tag,
            )

        if not submission.path:
            detail = "The submission seems to be broken..."
            raise ValueError(detail)

        return submission.path

    @classmethod
    async def _read_file(cls, path: Path) -> str:
        """Read the file."""
        return await asyncio.to_thread(path.read_text, encoding=cls._encoding, errors=cls._errors)
