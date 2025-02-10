"""Base plugin class."""

from abc import abstractmethod
from pathlib import Path
from typing import Any, Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel

T = TypeVar("T", covariant=True, bound=BaseModel)


@runtime_checkable
class Plugin(Protocol[T]):
    """Base class for plugins."""

    @staticmethod
    @abstractmethod
    def get_settings(
        cwd: Path,
        **kwargs: Any,
    ) -> T:
        """Get settings for the class."""
        raise NotImplementedError

    def __init__(self, settings: T) -> None:
        """Initialize the plugin."""
        raise NotImplementedError
