from pydantic import BaseModel

from admirable.domain.value_objects.role import Role


class CreateUserCommand(BaseModel):
    name: str
    email: str
    password: str


class UpdateUserCommand(BaseModel):
    user_id: int
    name: str
    email: str
    password: str | None = None


class UserDTO(BaseModel):
    id: int
    name: str
    email: str
    role: Role
