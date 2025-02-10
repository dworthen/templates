"""Plugin Errors."""


class FailedToLoadPluginSettingsError(ValueError):
    """Failed to load plugin settings error."""

    def __init__(self, key: str) -> None:
        """Initialize the error."""
        msg = f"Failed to load plugin settings for '{key}'."
        super().__init__(msg)
