from collections import deque, defaultdict
import asyncio
import time

class Queue:
    def __init__(self):
        self._queues = defaultdict(deque)
        self._waiters = defaultdict(list)
        self._lock = asyncio.Lock()

    async def lpush(self, key: str, *values: str) -> int:
        async with self._lock:
            queue = self._queues[key]
            for value in values:
                queue.appendleft(value)
            if self._waiters[key]:
                waiter = self._waiters[key].pop(0)
                waiter.set_result((key, queue.pop()))
            return len(queue)

    async def blpop(self, keys: list[str], timeout: float) -> list[str]:
        start = time.time()
        while time.time() - start < timeout:
            async with self._lock:
                for key in keys:
                    if self._queues[key]:
                        return [key, self._queues[key].pop()]
                future = asyncio.get_event_loop().create_future()
                for key in keys:
                    self._waiters[key].append(future)
            try:
                return await asyncio.wait_for(future, timeout - (time.time() - start))
            except asyncio.TimeoutError:
                async with self._lock:
                    for key in keys:
                        self._waiters[key] = [w for w in self._waiters[key] if w != future]
                return None
        return None
