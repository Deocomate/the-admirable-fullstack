from redis.asyncio import Redis, from_url

from admirable.infrastructure.security.redis_token_store import RedisTokenStore

_TEST_REDIS_URL = "redis://127.0.0.1:6379/1"  # DB 1, separate from app default DB 0


async def _redis() -> Redis:
    client = from_url(_TEST_REDIS_URL)
    await client.flushdb()
    return client


async def test_issue_and_consume_token() -> None:
    redis = await _redis()
    try:
        store = RedisTokenStore(redis)
        token = await store.issue("admin@example.com")
        assert token

        email = await store.consume(token)
        assert email == "admin@example.com"
    finally:
        await redis.aclose()


async def test_token_is_single_use() -> None:
    redis = await _redis()
    try:
        store = RedisTokenStore(redis)
        token = await store.issue("admin@example.com")

        first = await store.consume(token)
        second = await store.consume(token)

        assert first == "admin@example.com"
        assert second is None
    finally:
        await redis.aclose()


async def test_unknown_token_returns_none() -> None:
    redis = await _redis()
    try:
        store = RedisTokenStore(redis)
        assert await store.consume("bogus-token") is None
    finally:
        await redis.aclose()


async def test_token_has_ttl() -> None:
    redis = await _redis()
    try:
        store = RedisTokenStore(redis)
        token = await store.issue("admin@example.com")
        ttl = await redis.ttl(f"pwreset:{token}")
        assert 0 < ttl <= 3600
    finally:
        await redis.aclose()
