"""Global CLI options."""

from pathlib import Path

import typer

cwd_option = typer.Option(
    help="The working directory.", default=str(Path.cwd()), show_default=True
)
config_path_option = typer.Option(
    help="The configuration file path.",
    default=None,
    show_default=True,
)
