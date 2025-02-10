"""File System Log Plugin."""

import json
import logging
from collections.abc import Callable
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, computed_field, model_validator

LOG_LEVEL = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "FATAL"]


class FileSystemLoggerPluginSettings(BaseModel):
    """File System Log Plugin Settings."""

    cwd: str = Field(
        description="The current working directory.", default=str(Path.cwd())
    )
    directory: str = Field(description="The log directory.", default="logs")
    filename: str = Field(description="The log file name.", default="logs.json")
    filemode: str = Field(description="The file mode.", default="a")
    encoding: str = Field(description="The file encoding.", default="utf-8")
    structured_logging: bool = Field(
        description="Log in a structured format using JSON.", default=True
    )

    datefmt: str | None = Field(
        description="The date format.", default="%Y-%m-%d %H:%M:%S"
    )
    level: LOG_LEVEL = Field(description="The log level.", default="INFO")
    clear: bool = Field(description="Clear the log file on startup.", default=True)
    format: str = Field(
        description="The log format.",
        default="",
    )

    def _validate_format(self):
        if self.format.strip() != "":
            return
        if self.structured_logging:
            self.format = "%(message)s"
        else:
            self.format = "%(asctime)s,%(msecs)d %(levelname)s: %(message)s"

    max_bytes: int = Field(
        description="The maximum log file size in bytes.", default=1_000_000
    )
    max_num_files: int = Field(
        description="The maximum number of log files to keep.", default=10
    )

    @computed_field
    @property
    def log_level(self) -> int:
        """Get the log level."""
        match self.level:
            case "DEBUG":
                return logging.DEBUG
            case "INFO":
                return logging.INFO
            case "WARNING":
                return logging.WARNING
            case "ERROR":
                return logging.ERROR
            case "CRITICAL":
                return logging.CRITICAL
            case "FATAL":
                return logging.FATAL
            case _:
                return 0

    @model_validator(mode="after")
    def _validate_model(self):
        if self.directory.strip() == "":
            msg = "The log directory cannot be empty."
            raise ValueError(msg)
        if self.filename.strip() == "":
            msg = "The log filename cannot be empty."
            raise ValueError(msg)
        self.filename = str((Path(self.cwd) / self.directory / self.filename).resolve())
        if self.max_bytes < 0:
            msg = "The maximum log file size cannot be negative."
            raise ValueError(msg)
        if self.max_bytes > 0 and self.max_num_files < 1:
            msg = "The maximum number of log files must be at least 1."
            raise ValueError(msg)
        self._validate_format()
        return self


class _M:
    """Format log messages."""

    def __init__(
        self, structured: bool, level: str, datefmt: str | None, msg: str, /, **kwargs
    ) -> None:
        self.structured = structured
        self.level = level
        self.datefmt = (
            datefmt if datefmt is not None and datefmt.strip() != "" else None
        )
        now = datetime.now(tz=UTC)
        self.timestamp = now.strftime(datefmt) if datefmt is not None else None
        self.msg = msg
        self.kwargs = kwargs

    def _get_message(self) -> str:
        if self.structured:
            return json.dumps(
                {
                    **(
                        {"timestamp": self.timestamp}
                        if self.timestamp is not None
                        else {}
                    ),
                    "level": self.level,
                    "msg": self.msg,
                    **self.kwargs,
                }
            )
        msg = self.msg
        for key, value in self.kwargs.items():
            msg = msg + f", {key}={value}"
        return msg

    def __str__(self) -> str:
        return self._get_message()


class FileSystemLoggerPlugin:
    """File System Log Plugin."""

    @staticmethod
    def get_settings(cwd: Path, **settings: Any) -> FileSystemLoggerPluginSettings:
        """Get settings for the class."""
        settings["cwd"] = str(cwd.resolve())
        return FileSystemLoggerPluginSettings(**settings)

    def __init__(self, settings: FileSystemLoggerPluginSettings) -> None:
        self.settings = settings
        self.file_path = Path(settings.filename).resolve()
        Path(settings.filename).parent.mkdir(parents=True, exist_ok=True)

        if settings.clear:
            with self.file_path.open("w", encoding=self.settings.encoding) as file:
                file.write("")

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
                level=settings.log_level,
                handlers=[handler],
            )
        else:
            logging.basicConfig(
                filename=settings.filename,
                filemode=settings.filemode,
                format=settings.format,
                datefmt=settings.datefmt,
                level=settings.log_level,
            )

    def _log(self, log_level: LOG_LEVEL, msg: str, **kwargs: Any) -> None:
        timestamp = ""
        if self.settings.datefmt is not None and self.settings.datefmt.strip() != "":
            now = datetime.now(tz=UTC)
            timestamp = now.strftime(self.settings.datefmt)
        if self.settings.structured_logging:
            log_msg = json.dumps(
                {
                    **({"timestamp": timestamp} if timestamp != "" else {}),
                    "level": log_level,
                    "msg": msg,
                    **kwargs,
                }
            )
        else:
            log_msg = f"{log_level}: {msg}"
            if timestamp != "":
                log_msg = f"{timestamp} {log_msg}"
            for key, value in kwargs.items():
                log_msg = log_msg + f", {key}={value}"
        with self.file_path.open(
            self.settings.filemode, encoding=self.settings.encoding
        ) as file:
            file.write(log_msg + "\n")

    def debug(self, msg: str, **kwargs: Any) -> None:
        """Log Debug."""
        logging.debug(
            _M(
                self.settings.structured_logging,
                "DEBUG",
                self.settings.datefmt,
                msg,
                **kwargs,
            )
        )

    def info(self, msg: str, **kwargs: Any) -> None:
        """Log Info."""
        logging.info(
            _M(
                self.settings.structured_logging,
                "INFO",
                self.settings.datefmt,
                msg,
                **kwargs,
            )
        )

    def warning(self, msg: str, **kwargs: Any) -> None:
        """Log Warning."""
        logging.warning(
            _M(
                self.settings.structured_logging,
                "WARNING",
                self.settings.datefmt,
                msg,
                **kwargs,
            )
        )

    def error(self, msg: str, **kwargs: Any) -> None:
        """Log Error."""
        logging.error(
            _M(
                self.settings.structured_logging,
                "ERROR",
                self.settings.datefmt,
                msg,
                **kwargs,
            )
        )

    def critical(self, msg: str, **kwargs: Any) -> None:
        """Log Critical."""
        logging.critical(
            _M(
                self.settings.structured_logging,
                "CRITICAL",
                self.settings.datefmt,
                msg,
                **kwargs,
            )
        )

    def fatal(self, msg: str, **kwargs: Any) -> None:
        """Log Fatal."""
        logging.fatal(
            _M(
                self.settings.structured_logging,
                "FATAL",
                self.settings.datefmt,
                msg,
                **kwargs,
            )
        )

    def log(self, level: int, msg: str, **kwargs: Any) -> None:
        """Log."""
        if level not in self.log_mapping:
            err = f"Invalid log level {level}."
            raise ValueError(err)
        self.log_mapping[level](msg, **kwargs)
