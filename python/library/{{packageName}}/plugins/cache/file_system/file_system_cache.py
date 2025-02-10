"""File system cache plugin."""

from pathlib import Path
from typing import Any

import xxhash
from pydantic import BaseModel, Field, model_validator


class FileSystemCacheSettings(BaseModel):
    """File system cache settings."""

    cwd: str = Field(description="Current working directory", default=str(Path.cwd()))
    directory: str = Field(description="Directory to store cache", default="cache")
    encoding: str = Field(description="Encoding to use", default="utf-8")

    @model_validator(mode="after")
    def _validate_model(self):
        if self.cwd.strip() == "":
            msg = "The current working directory is a required field."
            raise ValueError(msg)
        self.cwd = str(Path(self.cwd).resolve())
        if self.directory.strip() == "":
            msg = "The directory is a required field."
            raise ValueError(msg)
        self.directory = str((Path(self.cwd) / self.directory).resolve())
        return self


class FileSystemCache:
    """File system cache plugin."""

    @staticmethod
    def get_settings(cwd: Path, **settings: Any) -> FileSystemCacheSettings:
        """Get settings for the class."""
        settings["cwd"] = str(cwd.resolve())
        return FileSystemCacheSettings(**settings)

    @staticmethod
    def get_settings_type() -> type[FileSystemCacheSettings]:
        """Get the settings type."""
        return FileSystemCacheSettings

    def __init__(self, settings: FileSystemCacheSettings) -> None:
        """Initialize the plugin."""
        self.settings = settings
        self.cache_directory = Path(settings.directory).resolve()
        self.cache_directory.mkdir(parents=True, exist_ok=True)

    def _get_key(self, key: str) -> str:
        return xxhash.xxh64(key).hexdigest()

    def get(self, key: str) -> str | None:
        """Get."""
        cache_file = self.cache_directory / self._get_key(key)
        if cache_file.exists():
            return cache_file.read_text(encoding=self.settings.encoding)
        return None

    def set(self, key: str, value: str) -> None:
        """Set."""
        cache_file = self.cache_directory / self._get_key(key)
        cache_file.write_text(value, encoding=self.settings.encoding)

    def delete(self, key: str) -> None:
        """Delete."""
        cache_file = self.cache_directory / self._get_key(key)
        if cache_file.exists():
            cache_file.unlink()

    def clear(self) -> None:
        """Clear."""
        if self.cache_directory.exists():
            for cache_file in self.cache_directory.glob("*"):
                cache_file.unlink()

    def __contains__(self, key: str) -> bool:
        """Contains in cache."""
        cache_file = self.cache_directory / self._get_key(key)
        return cache_file.exists()
