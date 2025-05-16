import asyncio
import os

from difflib import HtmlDiff
from os import PathLike
from pathlib import Path
from tempfile import mkstemp
from typing import Final

import click

from weasel.container import WEASEL_CONTAINER
from weasel.domain.services.interfaces.mutation import MutationInterface


ENCODING: Final[str] = "utf-8"
ERRORS: Final[str] = "replace"


@click.command()
@click.argument("source", type=click.Path(exists=True, dir_okay=False))
@click.argument("target", type=click.Path(exists=True, dir_okay=False))
def diff(source: str | PathLike[str], target: str | PathLike[str]) -> None:
    """Compare files and highlight differences."""
    languages = WEASEL_CONTAINER.languages()
    matcher_service = WEASEL_CONTAINER.matcher_service()
    service_settings = WEASEL_CONTAINER.service_settings()

    source = Path(source)
    target = Path(target)

    if not source.suffix or not target.suffix:
        detail = "The files are missing extensions... Please, add them."
        raise click.UsageError(detail)

    extensions = {extension for language in languages for extension in language.get_extensions()}
    if source.suffix not in extensions or target.suffix not in extensions:
        detail = "At least one of the files has an unsupported extension!"
        raise click.UsageError(detail)

    coroutine = matcher_service.maybe_match(source, target)
    maybe_match = asyncio.run(coroutine)

    if maybe_match is None:
        detail = f"'{source}' and '{target}' seem to be different languages..."
        raise click.UsageError(detail)

    source_text = source.read_text(encoding=ENCODING, errors=ERRORS)
    target_text = target.read_text(encoding=ENCODING, errors=ERRORS)
    mutated_text = mutate_from_labels(source_text, target_text, maybe_match.labels)

    simple_highlight = highlight(source_text, target_text)
    smart_highlight = highlight(mutated_text, target_text)

    title = f"{service_settings.name} {service_settings.version}"
    labels_or_hyphen = ", ".join(maybe_match.labels) if maybe_match.labels else "-"

    click.echo(title)
    click.echo("-" * len(title))

    click.echo()

    click.echo("Files:")
    click.echo(f"- source:        {source.as_posix()}")
    click.echo(f"- target:        {target.as_posix()}")

    click.echo()

    click.echo("Match:")
    click.echo(f"- language:      {maybe_match.language}")
    click.echo(f"- probability:   {maybe_match.probability}")
    click.echo(f"- labels:        {labels_or_hyphen}")

    click.echo()

    click.echo("Highlights:")
    click.echo(f"- simple:        {simple_highlight.as_posix()}")

    if maybe_match.labels:
        click.echo(f"- smart:         {smart_highlight.as_posix()}")


def mutate_from_labels(source: str, target: str, labels: str) -> str:
    """Mutate `source` based on `target` and `labels`."""
    for mutation in mutations_from_labels(labels):
        coroutine = mutation.mutate(source, target)
        source = asyncio.run(coroutine)
    return source


def highlight(source: str, target: str) -> Path:
    """Highlight the differences and save to a temporary file."""
    source_lines = source.splitlines(keepends=True)
    target_lines = target.splitlines(keepends=True)

    differ = HtmlDiff()
    html = differ.make_file(source_lines, target_lines, fromdesc="Source", todesc="Target")

    fd, path = mkstemp(suffix=".html")
    os.write(fd, html.encode(ENCODING, ERRORS))
    os.close(fd)

    return Path(path)


def mutations_from_labels(labels: list[str]) -> list[MutationInterface]:
    """Convert labels to mutations."""
    factories = [getattr(MutationInterface, label.lower()) for label in labels]
    return [factory() for factory in factories]
