"""Console Log Plugin."""

import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class LogPluginFileConsoleSettings(BaseModel):
    """File System Log Plugin Settings."""

    name: str = Field(description="Logger name.", default="Console")


class LogPluginConsole:
    """File System Log Plugin."""

    @staticmethod
    def get_settings(_: Path, **settings: Any) -> LogPluginFileConsoleSettings:
        """Get settings for the class."""
        return LogPluginFileConsoleSettings(**settings)

    def __init__(self, settings: LogPluginFileConsoleSettings) -> None:
        self.settings = settings
        self.log_mapping: dict[int, Callable[[str], None]] = {
            logging.DEBUG: self.debug,
            logging.INFO: self.info,
            logging.WARNING: self.warning,
            logging.ERROR: self.error,
            logging.CRITICAL: self.critical,
            logging.FATAL: self.fatal,
        }

    def debug(self, msg: str) -> None:
        """Log Debug."""
        print(f"{self.settings.name} DEBUG: {msg}")

    def info(self, msg: str) -> None:
        """Log Info."""
        print(f"{self.settings.name} INFO: {msg}")

    def warning(self, msg: str) -> None:
        """Log Warning."""
        print(f"{self.settings.name} WARNING: {msg}")

    def error(self, msg: str) -> None:
        """Log Error."""
        print(f"{self.settings.name} ERROR: {msg}")

    def critical(self, msg: str) -> None:
        """Log Critical."""
        print(f"{self.settings.name} CRITICAL: {msg}")

    def fatal(self, msg: str) -> None:
        """Log Fatal."""
        print(f"{self.settings.name} FATAL: {msg}")

    def log(self, level: int, msg: str) -> None:
        """Log."""
        if level not in self.log_mapping:
            raise ValueError(f"Invalid log level {level}.")
        self.log_mapping[level](msg)
