"""Implements TokenStorePort on Redis: single-use, TTL-bound password-reset tokens."""

import secrets

from redis.asyncio import Redis

_KEY_PREFIX = "pwreset:"
_TTL_SECONDS = 3600

# GET + DEL atomically so a token can only ever be consumed once, even under
# concurrent requests for the same token.
_CONSUME_SCRIPT = """
local value = redis.call('GET', KEYS[1])
if value then
    redis.call('DEL', KEYS[1])
end
return value
"""


class RedisTokenStore:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def issue(self, email: str) -> str:
        token = secrets.token_urlsafe(32)
        await self._redis.set(f"{_KEY_PREFIX}{token}", email, ex=_TTL_SECONDS)
        return token

    async def consume(self, token: str) -> str | None:
        result = await self._redis.eval(_CONSUME_SCRIPT, 1, f"{_KEY_PREFIX}{token}")
        return result.decode("utf-8") if isinstance(result, bytes) else result
