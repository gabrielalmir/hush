import pytest
from src.queue import Queue

@pytest.mark.asyncio
async def test_queue_lpush_blpop():
    queue = Queue()
    assert await queue.lpush("queue", "msg1", "msg2") == 2
    assert await queue.blpop(["queue"], 1) == ["queue", "msg1"]

