from pydantic import BaseModel

from admirable.domain.value_objects.role import Role


class LoginCommand(BaseModel):
    email: str
    password: str


class AuthenticatedUserDTO(BaseModel):
    id: int
    name: str
    email: str
    role: Role


class RequestPasswordResetCommand(BaseModel):
    email: str


class ResetPasswordCommand(BaseModel):
    token: str
    email: str
    password: str
