import asyncio
import os

from collections.abc import AsyncGenerator
from contextlib import aclosing
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import TYPE_CHECKING

from weasel.domain.entities.comparison import ComparisonEntity
from weasel.domain.entities.contest import ContestEntity
from weasel.domain.entities.match import MatchEntity
from weasel.domain.entities.report import ReportEntity
from weasel.domain.entities.review import ReviewEntity
from weasel.domain.entities.submission import SubmissionEntity
from weasel.domain.entities.task import TaskEntity


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.git import GitInterface
    from weasel.domain.services.interfaces.metrics import MetricsInterface
    from weasel.domain.services.interfaces.sealer import SealerInterface
    from weasel.domain.services.matcher import MatcherService


@dataclass
class ScannerService:
    """The scanner service."""

    _bitbucket: "GitInterface"
    _github: "GitInterface"
    _matcher: "MatcherService"
    _metrics: "MetricsInterface"
    _sealer: "SealerInterface"

    async def scan(self, contest: "ContestEntity") -> "ReportEntity":
        """Scan the contest and return a report."""
        contest = await self._seal_contest(contest)
        coroutines = [self._review(task) for task in contest.tasks]
        reviews = await asyncio.gather(*coroutines)
        return ReportEntity(reviews=reviews)

    async def _review(self, task: "TaskEntity") -> "ReviewEntity":
        """Review the task.

        Notes
        -----
        * Comparisons are asymmetric.
        """
        coroutines = [
            coroutine
            for s1, s2 in combinations(task.submissions, r=2)
            for coroutine in (self._compare(s1, s2), self._compare(s2, s1))
        ]
        comparisons = await asyncio.gather(*coroutines)
        return ReviewEntity(name=task.name, comparisons=comparisons)

    async def _compare(self, s1: "SubmissionEntity", s2: "SubmissionEntity") -> "ComparisonEntity":
        """Compare submissions.

        Notes
        -----
        * Limit the number of concurrent tasks to avoid memory issues.
        """
        if not s1.path or not s2.path:
            detail = "The submissions seem to be broken..."
            raise ValueError(detail)

        source_files, target_files = await asyncio.gather(
            self._list_files(s1.path), self._list_files(s2.path)
        )

        coroutines = [
            self._matcher.maybe_match(source_file, target_file)
            for source_file in source_files
            for target_file in target_files
        ]

        matches = [
            MatchEntity(
                source=maybe_match.source.relative_to(s1.path),
                target=maybe_match.target.relative_to(s2.path),
                language=maybe_match.language,
                probability=maybe_match.probability,
                labels=maybe_match.labels,
            )
            for maybe_match in await asyncio.gather(*coroutines)
            if maybe_match
        ]

        probabilities = [match.probability for match in matches]
        metrics = self._metrics.calculate(probabilities)

        matches.sort(key=lambda match: match.probability, reverse=True)
        return ComparisonEntity(source=s1.name, target=s2.name, metrics=metrics, matches=matches)

    async def _seal_contest(self, contest: "ContestEntity") -> "ContestEntity":
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
    async def _list_files(cls, dirpath: Path) -> list[Path]:
        """List the directory files."""
        async with aclosing(cls._iterate_over_files(dirpath)) as files:
            return [file async for file in files]

    @classmethod
    async def _iterate_over_files(cls, dirpath: Path) -> AsyncGenerator[Path]:
        """Scan the directory."""
        iterator = os.scandir(dirpath)
        entries = await asyncio.to_thread(list, iterator)

        for entry in entries:
            path = Path(entry.path)

            if entry.is_file(follow_symlinks=False):
                yield path

            elif entry.is_dir(follow_symlinks=False):
                async with aclosing(cls._iterate_over_files(path)) as files:
                    async for file in files:
                        yield file
