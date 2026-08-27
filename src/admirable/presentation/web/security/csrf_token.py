import secrets

from admirable.presentation.web.middleware.session import Session

_SESSION_KEY = "csrf_token"


def get_or_create_csrf_token(session: Session) -> str:
    token = session.get(_SESSION_KEY)
    if not isinstance(token, str) or not token:
        token = secrets.token_urlsafe(32)
        session[_SESSION_KEY] = token
    return token
