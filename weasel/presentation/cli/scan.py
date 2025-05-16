import asyncio
import sys

from datetime import UTC, datetime
from os import PathLike
from pathlib import Path
from tempfile import NamedTemporaryFile

import click

from pydantic import ValidationError

from weasel.container import WEASEL_CONTAINER
from weasel.domain.entities.contest import ContestEntity


@click.command()
@click.option("--from-json", type=click.Path(exists=True, dir_okay=False), help="Load from JSON.")
@click.option("--from-toml", type=click.Path(exists=True, dir_okay=False), help="Load from TOML.")
@click.option("--from-yaml", type=click.Path(exists=True, dir_okay=False), help="Load from YAML.")
@click.option("--to-json", help="Write to JSON.")
@click.option("--to-toml", help="Write to TOML.")
@click.option("--to-yaml", help="Write to YAML.")
def scan(  # noqa: C901, PLR0912, PLR0913, PLR0915
    from_json: str | PathLike[str] | None = None,
    from_toml: str | PathLike[str] | None = None,
    from_yaml: str | PathLike[str] | None = None,
    to_json: str | PathLike[str] | None = None,
    to_toml: str | PathLike[str] | None = None,
    to_yaml: str | PathLike[str] | None = None,
) -> None:
    """Scan multiple files or repositories."""
    scanner_service = WEASEL_CONTAINER.scanner_service()
    service_settings = WEASEL_CONTAINER.service_settings()

    from_files = [from_json, from_toml, from_yaml]
    from_files_count = sum(map(bool, from_files))

    to_files = [to_json, to_toml, to_yaml]
    to_files_count = sum(map(bool, to_files))

    if not from_files_count:
        detail = "The contest file is not provided (--from-*)."
        raise click.UsageError(detail)

    if from_files_count > 1:
        detail = "There must be exactly one contest file provided (--from-*)."
        raise click.UsageError(detail)

    if not to_files_count:
        detail = "The output file(s) is not provided (--to-*)."
        raise click.UsageError(detail)

    try:
        if from_json:
            contest = ContestEntity.from_json(Path(from_json))
        if from_toml:
            contest = ContestEntity.from_toml(Path(from_toml))
        if from_yaml:
            contest = ContestEntity.from_yaml(Path(from_yaml))

    except ValidationError as exception:
        detail = f"The contest file seems to be broken:\n\n{exception}"
        raise click.UsageError(detail) from exception

    except Exception as exception:
        detail = f"An unexpected error occurred while loading the contest file: {exception}"
        raise click.UsageError(detail) from exception

    title = f"{service_settings.name} {service_settings.version}"

    click.echo(title)
    click.echo("-" * len(title))

    click.echo()

    click.echo("This may take a while...")

    click.echo()

    click.echo("Start:")
    click.echo(f"- now:      {isoformat()}")

    click.echo()

    try:
        coroutine = scanner_service.scan(contest)
        report = asyncio.run(coroutine)

    except Exception as exception:  # noqa: BLE001
        click.echo(f"Error: {exception}")
        sys.exit(1)

    click.echo("Finish:")
    click.echo(f"- now:      {isoformat()}")

    click.echo()

    click.echo("Reports:")

    is_backup_used = False

    try:
        if to_json:
            path = Path(to_json)
            report.to_json(path)
            click.echo(f"- json:     {path}")

        if to_toml:
            path = Path(to_toml)
            report.to_toml(path)
            click.echo(f"- toml:     {path}")

        if to_yaml:
            path = Path(to_yaml)
            report.to_yaml(path)
            click.echo(f"- yaml:     {path}")

    except OSError:
        with NamedTemporaryFile(suffix=".json", delete=False) as file:
            is_backup_used = True
            path = Path(file.name)
            report.to_json(path)
            click.echo(f"- backup:   {path}")

    if is_backup_used:
        click.echo()
        click.echo("The output file(s) could not be written - the backup is provided.")


def isoformat() -> str:
    """Return the current time in ISO format."""
    return datetime.now(UTC).isoformat(sep=" ", timespec="milliseconds")
