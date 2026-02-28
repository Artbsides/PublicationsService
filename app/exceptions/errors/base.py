class BaseError(Exception):
    args: dict[str, str] | None = None
    status_code: int
