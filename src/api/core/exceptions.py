class ExternalApiError(Exception):
    """
    Raised when an external API request fails or returns an invalid response.

    Args:
        name: Name of the external API.
    """

    def __init__(self, name: str = "External API") -> None:
        self.detail = f"{name} returned an invalid response."


class InvalidIdError(Exception):
    """
    Raised when a provided resource ID is invalid or malformed.

    Args:
        name: Name of the resource.
    """

    def __init__(self, name: str = "Resource") -> None:
        self.detail = f"{name} ID is invalid."


class ResourceNotFoundError(Exception):
    """
    Raised when a requested resource cannot be found in the database.

    Args:
        name: Name of the missing resource.
    """

    def __init__(self, name: str = "Resource") -> None:
        self.detail = f"{name} not found."


class DuplicateResourceError(Exception):
    """
    Raised when attempting to create a resource that already exists.

    Args:
        name: Name of the resource that already exists.
    """

    def __init__(self, name: str = "Resource") -> None:
        self.detail = f"{name} already exists!"


class InvalidTokenError(Exception):
    """
    Raised when decoding an invalid token.

    Args:
        detail: Description of the error.
    """

    def __init__(self, detail: str = "Token is invalid") -> None:
        self.detail = detail
