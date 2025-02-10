"""App Configuration."""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, model_validator


class PluginConfig(BaseModel):
    """Plugin Configuration.

    Validation of plugin settings occur in the plugin itself.
    """

    plugin_id: str = Field(description="The id of the plugin.")
    settings: dict[str, Any] = Field(description="Settings for the plugin.", default={})


class CacheConfig(BaseModel):
    """Cache Configuration."""

    skip_cache: bool = Field(description="Disable caching.", default=False)
    clear_cache: bool = Field(description="Clear the cache.", default=False)
    plugin: PluginConfig = Field(
        description="The cache plugin.",
        default=PluginConfig(plugin_id="FileSystemCache"),
    )


class LoggingConfig(BaseModel):
    """Logging Configuration."""

    source: bool = Field(description="Log the source of the log message.", default=True)
    plugins: list[PluginConfig] = Field(
        description="The logging plugin.",
        default=[PluginConfig(plugin_id="FileSystemLoggerPlugin")],
    )


class Config(BaseModel):
    """App Configuration."""

    cwd: str = Field(
        description="The current working directory.", default=str(Path.cwd())
    )
    logging: LoggingConfig = Field(
        description="The logging configuration.",
        default=LoggingConfig(),
    )
    cache: CacheConfig = Field(
        description="The cache configuration.", default=CacheConfig()
    )

    @model_validator(mode="after")
    def _validate_model(self):
        # Rollup/rolldown logic for setting properties
        # Resolve timestamp paths upfront
        return self
