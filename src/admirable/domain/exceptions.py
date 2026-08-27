"""Domain exception hierarchy. Pure Python, no framework imports."""


class DomainError(Exception):
    """Base class for every domain-level error."""


class EntityNotFoundError(DomainError):
    def __init__(self, entity: str, identifier: object) -> None:
        self.entity = entity
        self.identifier = identifier
        super().__init__(f"{entity} not found: {identifier!r}")


class ValidationError(DomainError):
    pass


class BusinessRuleViolationError(DomainError):
    pass


class InvalidAudioTransitionError(BusinessRuleViolationError):
    def __init__(self, src: str, dst: str) -> None:
        self.src = src
        self.dst = dst
        super().__init__(f"Cannot transition audio status from {src!r} to {dst!r}")


class CannotDeleteSuperAdminError(BusinessRuleViolationError):
    """Matches `UserService::deleteAdmin`: a superadmin account can never be
    deleted through the admin UI, regardless of how many others exist."""

    def __init__(self) -> None:
        super().__init__("Không thể xóa tài khoản superadmin.")


class SelfDeletionError(BusinessRuleViolationError):
    def __init__(self) -> None:
        super().__init__("Bạn không thể tự xóa tài khoản của mình.")


class DuplicateSlugError(BusinessRuleViolationError):
    def __init__(self, slug: str) -> None:
        self.slug = slug
        super().__init__(f"Slug already exists: {slug!r}")


class DuplicateValueError(BusinessRuleViolationError):
    """Raised when a unique business constraint in the repository is violated."""

    def __init__(self, field: str, value: str) -> None:
        self.field = field
        self.value = value
        super().__init__(f"Duplicate value for {field}: {value!r}")
