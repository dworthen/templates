"""Command Two."""

import typer

command_two = typer.Typer()


@command_two.command("run")
def run_command():
    """Run command two."""
    print("Running command two")
