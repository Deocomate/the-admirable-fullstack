"""Ports `UserController::store`/`::update`'s inline `$request->validate()`
rules. `password_confirmation`/the `confirmed` rule and `unique:users,email`
both need cross-field/DB checks, so they're enforced in the router and use
case respectively, not here (same split as `category_form.py`)."""

from pydantic import BaseModel, Field

USER_FIELD_LABELS = {
    "name": "Tên hiển thị",
    "email": "Email",
    "password": "Mật khẩu",
}


class CreateUserForm(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=1)
    password: str = Field(min_length=8)
    password_confirmation: str = ""


class UpdateUserForm(BaseModel):
    """`password` is optional here ("leave blank to keep it unchanged") — its
    min-length is checked in the router only when non-empty, since Pydantic's
    `Field(min_length=...)` would otherwise reject the common blank case."""

    name: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=1)
    password: str = ""
    password_confirmation: str = ""
