import asyncio

from os import PathLike
from pathlib import Path

import click

from weasel.container import WEASEL_CONTAINER


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

    title = f"{service_settings.name} {service_settings.version}"
    maybe_labels = ", ".join(maybe_match.labels) if maybe_match.labels else "null"

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
    click.echo(f"- labels:        {maybe_labels}")

    click.echo()

    click.echo("Highlights:")
    click.echo("- simple:         ...")
    click.echo("- smart:          ...")
