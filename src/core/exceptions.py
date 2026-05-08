class ExternalApiError(Exception):
    def __init__(self, detail: str = "External API Error!") -> None:
        self.detail = detail


class InvalidIdError(Exception):
    def __init__(self, detail: str = "Invalid profile id") -> None:
        self.detail = detail


class ProfileNotFoundError(Exception):
    def __init__(self, detail: str = "Profile not found") -> None:
        self.detail = detail
