"""Main CLI entry point."""

import typer

from .command_one import command_one
from .command_two import command_two

app = typer.Typer()
app.add_typer(command_one, name="command_one")
app.add_typer(command_two, name="command_two")
