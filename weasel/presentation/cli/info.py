import click

from weasel.container import WEASEL_CONTAINER


@click.command()
def info() -> None:
    """Show the 'weasel' configuration."""
    service_settings = WEASEL_CONTAINER.service_settings()
    title = f"{service_settings.name} {service_settings.version}"

    click.echo(title)
    click.echo("-" * len(title))

    click.echo()

    click.echo("Config:")
    click.echo(f"- cache:           {service_settings.cache_directory}")
    click.echo(f"- data:            {service_settings.data_directory}")

    click.echo()

    click.echo("URL:")
    click.echo(f"- documentation:   {service_settings.documentation}")
    click.echo(f"- homepage:        {service_settings.homepage}")
    click.echo(f"- repository:      {service_settings.repository}")

    click.echo()

    click.echo("License")
    click.echo(f"- SPDX:            {service_settings.license}")
    click.echo(f"- authors:         {', '.join(service_settings.authors)}")
