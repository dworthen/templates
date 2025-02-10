"""Global CLI options."""

from pathlib import Path
from typing import Any

import typer

cwd_option = typer.Option(
    help="The working directory.", default=str(Path.cwd()), show_default=True
)
config_path_option = typer.Option(
    help="The configuration file path.",
    default=None,
    show_default=True,
)
skip_cache_option = typer.Option(
    help="Disable caching.", default=False, show_default=True
)
clear_cache_option = typer.Option(
    help="Clear the cache.", default=False, show_default=True
)


def get_config_overrides(
    skip_cache: bool = False, clear_cache: bool = False
) -> dict[str, Any]:
    """Get the config overrides."""
    return {
        "cache": {
            "clear_cache": clear_cache,
            "skip_cache": skip_cache,
        }
    }
