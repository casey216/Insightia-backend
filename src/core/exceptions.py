class ExternalApiError(Exception):
    def __init__(self, detail: str = "External API Error!"):
        self.detail = detail