"""Taskiq broker wired to Redis. Tasks are registered in Phase 6."""

from taskiq_redis import ListQueueBroker

from admirable.config import get_settings

broker = ListQueueBroker(url=get_settings().redis.url)
