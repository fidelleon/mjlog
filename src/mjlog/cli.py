"""CLI command dispatcher using click."""

import click

from mjlog.db.models import Base
from mjlog.db.session import get_engine, get_session


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


@cli.command()
@click.option("--title", prompt="Entry title", help="Title of the log entry.")
@click.option(
    "--content",
    prompt="Entry content",
    default="",
    help="Content of the log entry.",
)
def add(title, content):
    """Add a new log entry."""
    from mjlog.db.models import Entry

    session = get_session()
    try:
        entry = Entry(title=title, content=content)
        session.add(entry)
        session.commit()
        click.echo(f"Added entry: {entry}")
    finally:
        session.close()


@cli.command()
def list_entries():
    """List all log entries."""
    from mjlog.db.models import Entry

    session = get_session()
    try:
        entries = session.query(Entry).all()
        if not entries:
            click.echo("No entries found.")
        else:
            for entry in entries:
                click.echo(f"[{entry.id}] {entry.title} ({entry.created_at})")
    finally:
        session.close()


if __name__ == "__main__":
    cli()
