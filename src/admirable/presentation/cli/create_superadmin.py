"""Interactive superadmin creation — for bootstrapping a fresh VPS.

Usage: uv run python -m admirable.presentation.cli.create_superadmin
"""

import asyncio
import getpass

import typer

from admirable.config import get_settings
from admirable.domain.entities.user import User
from admirable.domain.value_objects.role import Role
from admirable.infrastructure.container import build_worker_scope

app = typer.Typer(add_completion=False)


async def _run(name: str, email: str, password: str) -> None:
    settings = get_settings()
    async with build_worker_scope(settings) as container:
        if await container.users.get_by_email(email) is not None:
            typer.echo(f"A user with email {email} already exists.", err=True)
            raise typer.Exit(1)

        await container.users.add(
            User(
                id=None,
                name=name,
                email=email,
                password_hash=container.hasher.hash(password),
                role=Role.SUPERADMIN,
            )
        )
    typer.echo(f"Superadmin created: {email}")


@app.command()
def main() -> None:
    name = typer.prompt("Full name")
    email = typer.prompt("Email")
    password = getpass.getpass("Password: ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        typer.echo("Passwords do not match.", err=True)
        raise typer.Exit(1)
    if len(password) < 8:
        typer.echo("Password must be at least 8 characters.", err=True)
        raise typer.Exit(1)

    asyncio.run(_run(name, email, password))


if __name__ == "__main__":
    app()
