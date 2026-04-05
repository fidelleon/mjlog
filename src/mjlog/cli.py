"""CLI command dispatcher using click."""

import click

from mjlog.db.models import Base
from mjlog.db.session import get_engine


@click.group()
def cli():
    """MJlog: Log management CLI."""
    pass


@cli.command()
def init_db():
    """Initialize database tables."""
    engine = get_engine()
    Base.metadata.create_all(engine)
    click.echo("Database initialized.")


if __name__ == "__main__":
    cli()
