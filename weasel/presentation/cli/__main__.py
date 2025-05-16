import click

from weasel.presentation.cli.diff import diff
from weasel.presentation.cli.info import info
from weasel.presentation.cli.scan import scan


@click.group(epilog="MIT License, Copyright (c) 2025 Sergei Y. Bogdanov.")
def main() -> None:
    """Hunt plagiarism - line by line, byte by byte."""


main.add_command(diff)
main.add_command(info)
main.add_command(scan)


if __name__ == "__main__":
    main()
