"""Load configuration from a file or create a default configuration."""

from pathlib import Path
from typing import Any

from essex_config.config import load_config as lc
from essex_config.sources import ArgSource, FileSource, Source

from .config import Config
from .defaults import CONFIG_FILENAME, SUPPORTED_CONFIG_EXTENSIONS


def _search_for_config_in_root_dir(root: str | Path) -> Path | None:
    """Resolve the config path from the given root directory.

    Parameters
    ----------
    root : str | Path
        The path to the root directory containing the config file.
        Searches for a default config file (settings.{yaml,yml,json}).

    Returns
    -------
    Path | None
        returns a Path if there is a config in the root directory
        Otherwise returns None.
    """
    supported_configs = [
        f"{CONFIG_FILENAME}.{ext}" for ext in SUPPORTED_CONFIG_EXTENSIONS
    ]
    root = Path(root).resolve()

    if not root.is_dir():
        msg = f"Invalid config path: {root} is not a directory"
        raise FileNotFoundError(msg)

    for file in supported_configs:
        if (root / file).is_file():
            return root / file

    return None


def load_config(
    directory_or_file_path: str | Path | None = None, overrides: dict[str, Any] = {}
) -> Config:
    """Load configuration from a file or create a default configuration.

    If a config file is not found the default configuration is created.

    Parameters
    ----------
    directory_or_file_path : str | Path | None
        The directory or file path to the config file.
        If filepath, load the configuration from the file.
        If directory, search for a supported config file in the directory.
        If None, create a default configuration.

    Returns
    -------
    Config
        The configuration object.

    Raises
    ------
    FileNotFoundError
        If a config file is provided and cannot be found.
    """
    sources: list[Source] = []
    if directory_or_file_path:
        path = Path(directory_or_file_path).resolve()
        if path.is_dir():
            overrides["cwd"] = str(path)
            sources.append(ArgSource(**overrides))
            config_path = _search_for_config_in_root_dir(path)
            if config_path:
                sources.append(FileSource(config_path, required=True))
        else:
            if not path.is_file():
                raise FileNotFoundError(f"Config file not found: {path}")
            overrides["cwd"] = str(path.parent)
            sources.append(ArgSource(**overrides))
            sources.append(FileSource(path, required=True))
    else:
        sources.append(ArgSource(**overrides))
    return lc(Config, sources=sources, parse_env_values=True)
