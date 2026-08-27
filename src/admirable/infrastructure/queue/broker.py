"""Taskiq broker wired to Redis. Tasks are registered in `tasks.py`.

`socket_timeout=None` is required: ListQueueBroker polls with a blocking
BRPOP (no protocol-level timeout), but redis-py 8.x defaults the *client*
socket_timeout to 5s. Left at the default, every idle BRPOP wait past 5s
raises a client-side TimeoutError, which crashes and restarts the worker
process in a tight loop — verified against a running `docker compose`
worker: without this, both worker subprocesses died and respawned every
1-2 seconds and a real enqueued task was lost with the DB left stuck in
`processing` forever.
"""

from taskiq_redis import ListQueueBroker

from admirable.config import get_settings

broker = ListQueueBroker(url=get_settings().redis.url, socket_timeout=None)
