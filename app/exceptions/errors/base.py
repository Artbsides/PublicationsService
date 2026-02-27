from typing import Optional


class BaseError(Exception):
    args: Optional[dict[str, str]] = None
    status_code: int
