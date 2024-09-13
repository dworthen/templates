"""App Configuration."""

import os
from typing import Annotated, Any

from essex_config.field_annotations import Updatable
from pydantic import BaseModel, Field, model_validator


class PluginConfig(BaseModel):
    """Plugin Configuration."""

    id: str = Field(description="The id of the plugin.")
    settings: Annotated[dict[str, Any], Updatable(lambda x, y: {**x, **y})] = Field(
        description="Settings for the plugin.", default={}
    )


# @config()
class Config(BaseModel):
    """App Configuration."""

    cwd: str = Field(description="The current working directory.", default=os.getcwd())
    logging: list[PluginConfig] = Field(
        description="The logging configuration.",
        default=[PluginConfig(id="LogPluginFileSystem")],
    )

    @model_validator(mode="after")
    def _validate_model(self):
        # Rollup/rolldown logic for setting properties
        # Resolve timestamp paths upfront
        return self
