class NotAuthenticatedError(Exception):
    pass


class AlreadyAuthenticatedError(Exception):
    """Raised when an authenticated user accesses a guest-only route."""


class ForbiddenError(Exception):
    def __init__(self, message: str = "Bạn không có quyền truy cập trang này.") -> None:
        self.message = message
        super().__init__(message)


class FormValidationError(Exception):
    """Raised by forms/base.py; caught by the error handler and turned into
    a redirect-back with flashed errors + old input."""

    def __init__(
        self, errors: dict[str, list[str]], old_input: dict[str, object], redirect_to: str
    ) -> None:
        self.errors = errors
        self.old_input = old_input
        self.redirect_to = redirect_to
        super().__init__(f"Validation failed: {errors}")
