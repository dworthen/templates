"""Configuration Errors."""


class ConfigLoadingError(ValueError):
    """Configuration Loading Error."""

    def __init__(self, msg: str) -> None:
        """Initialize the ConfigLoadingError."""
        super().__init__(msg)


class ConfigParsingError(ValueError):
    """Configuration Parsing Error."""

    def __init__(self, msg: str) -> None:
        """Initialize the ConfigParsingError."""
        super().__init__(msg)
