import pytest

from admirable.infrastructure.queue.broker import broker
from admirable.infrastructure.queue.taskiq_queue import TaskiqQueue


def test_broker_disables_socket_timeout_for_blocking_brpop() -> None:
    """Regression test: redis-py 8.x defaults socket_timeout to 5s, which
    fights ListQueueBroker's indefinitely-blocking BRPOP poll and crash-loops
    the worker (verified live against `docker compose` — both worker
    subprocesses died and respawned every 1-2s, silently losing an enqueued
    task). socket_timeout must stay None."""
    assert broker.connection_pool.connection_kwargs.get("socket_timeout") is None


def test_broker_has_generate_audio_task_registered() -> None:
    # Importing tasks.py (done transitively via taskiq_queue's lazy import
    # inside enqueue_audio_generation) registers the task on this broker.
    from admirable.infrastructure.queue import tasks  # noqa: F401

    assert "generate_audio" in broker.get_all_tasks()


async def test_enqueue_audio_generation_calls_kiq(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[str, int]] = []

    async def fake_kiq(kind: str, entity_id: int) -> None:
        calls.append((kind, entity_id))

    from admirable.infrastructure.queue import tasks

    monkeypatch.setattr(tasks.generate_audio_task, "kiq", fake_kiq)

    queue = TaskiqQueue()
    await queue.enqueue_audio_generation("figure", 42)

    assert calls == [("figure", 42)]
