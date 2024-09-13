"""File System Log Plugin."""

import logging
import os
from collections.abc import Callable
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, model_validator


class LogPluginFileSystemSettings(BaseModel):
    """File System Log Plugin Settings."""

    cwd: str = Field(description="The current working directory.", default=os.getcwd())
    directory: str = Field(description="The log directory.", default="logs")
    max_bytes: int = Field(
        description="The maximum log file size in bytes.", default=1_000_000
    )
    max_num_files: int = Field(
        description="The maximum number of log files to keep.", default=10
    )
    filename: str = Field(description="The log file name.", default="logs.txt")
    filemode: str = Field(description="The file mode.", default="a")
    format: str = Field(
        description="The log format.",
        default="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    )
    datefmt: str = Field(description="The date format.", default="%H:%M:%S")
    level: int = Field(description="The log level.", default=logging.INFO)

    @model_validator(mode="after")
    def _validate_model(self):
        if self.filename == "":
            msg = "The log filename cannot be empty."
            raise ValueError(msg)
        self.filename = str((Path(self.cwd) / self.directory / self.filename).resolve())
        if self.max_bytes < 0:
            msg = "The maximum log file size cannot be negative."
            raise ValueError(msg)
        if self.max_bytes > 0 and self.max_num_files < 1:
            msg = "The maximum number of log files must be at least 1."
            raise ValueError(msg)
        return self


class LogPluginFileSystem:
    """File System Log Plugin."""

    @staticmethod
    def get_settings(cwd: Path, **settings: Any) -> LogPluginFileSystemSettings:
        """Get settings for the class."""
        settings["cwd"] = str(cwd.resolve())
        return LogPluginFileSystemSettings(**settings)

    def __init__(self, settings: LogPluginFileSystemSettings) -> None:
        self.settings = settings
        Path(settings.filename).parent.mkdir(parents=True, exist_ok=True)
        self.log_mapping: dict[int, Callable[[str], None]] = {
            logging.DEBUG: self.debug,
            logging.INFO: self.info,
            logging.WARNING: self.warning,
            logging.ERROR: self.error,
            logging.CRITICAL: self.critical,
            logging.FATAL: self.fatal,
        }

        if settings.max_bytes > 0:
            handler = RotatingFileHandler(
                settings.filename,
                maxBytes=settings.max_bytes,
                backupCount=settings.max_num_files,
            )
            handler.setFormatter(logging.Formatter(settings.format, settings.datefmt))
            logging.basicConfig(
                format=settings.format,
                datefmt=settings.datefmt,
                level=settings.level,
                handlers=[handler],
            )
        else:
            logging.basicConfig(
                filename=settings.filename,
                filemode=settings.filemode,
                format=settings.format,
                datefmt=settings.datefmt,
                level=settings.level,
            )

    def debug(self, msg: str) -> None:
        """Log Debug."""
        logging.debug(msg)

    def info(self, msg: str) -> None:
        """Log Info."""
        logging.info(msg)

    def warning(self, msg: str) -> None:
        """Log Warning."""
        logging.warning(msg)

    def error(self, msg: str) -> None:
        """Log Error."""
        logging.error(msg)

    def critical(self, msg: str) -> None:
        """Log Critical."""
        logging.critical(msg)

    def fatal(self, msg: str) -> None:
        """Log Fatal."""
        logging.fatal(msg)

    def log(self, level: int, msg: str) -> None:
        """Log."""
        if level not in self.log_mapping:
            raise ValueError(f"Invalid log level {level}.")
        self.log_mapping[level](msg)
