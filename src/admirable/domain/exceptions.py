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


class LastSuperAdminDeletionError(BusinessRuleViolationError):
    def __init__(self) -> None:
        super().__init__("Cannot delete the last superadmin account")


class SelfDeletionError(BusinessRuleViolationError):
    def __init__(self) -> None:
        super().__init__("A user cannot delete their own account")


class DuplicateSlugError(BusinessRuleViolationError):
    def __init__(self, slug: str) -> None:
        self.slug = slug
        super().__init__(f"Slug already exists: {slug!r}")
