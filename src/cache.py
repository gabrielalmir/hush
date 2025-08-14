import time
import asyncio

class Node:
    def __init__(self, key: str, value: str, ttl: float = None):
        self.key = key
        self.value = value
        self.ttl = ttl
        self.next = None
        self.prev = None


class LruCache:
    # linked-list and hashmap
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._store = {}
        self._lock = asyncio.Lock()

        self._head = Node("head", "head")
        self._tail = Node("tail", "tail")
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0


    def _add_node(self, node: Node):
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._size += 1
        self._head.next = node

    def _remove_node(self, node: Node):
        node.prev.next = node.next
        self._size -= 1
        node.next.prev = node.prev

    def _move_to_head(self, node: Node):
        self._remove_node(node)
        self._add_node(node)

    def _evict(self):
        node = self._tail.prev
        self._remove_node(node)
        del self._store[node.key]

    async def set(self, key: str, value: str, ttl: float = None) -> str:
        async with self._lock:
            # Convert TTL from duration to absolute expiration time
            expiration_time = None if ttl is None else time.time() + ttl
            
            if key in self._store:
                node = self._store[key]
                node.value = value
                node.ttl = expiration_time
                self._move_to_head(node)
            else:
                node = Node(key, value, expiration_time)
                self._add_node(node)
                self._store[key] = node
                if self._size > self._capacity:
                    self._evict()
            return "OK"

    async def get(self, key: str) -> str:
        async with self._lock:
            if key in self._store:
                node = self._store[key]
                if node.ttl is not None and time.time() > node.ttl:
                    self._remove_node(node)
                    del self._store[key]
                    return None
                self._move_to_head(node)
                return node.value
            return None

    async def delete(self, key: str) -> str:
        async with self._lock:
            if key in self._store:
                node = self._store[key]
                self._remove_node(node)
                del self._store[key]
                return "OK"
            return "OK"

class Cache:
    def __init__(self):
        self._store = LruCache(1000)
        self._lock = asyncio.Lock()

    async def set(self, key: str, value: str, ttl: float = None) -> str:
        async with self._lock:
            await self._store.set(key, value, ttl)
            return "OK"

    async def get(self, key: str) -> str:
        async with self._lock:
            value = await self._store.get(key)
            if value is None:
                return None
            return value

    async def delete(self, key: str) -> str:
        async with self._lock:
            await self._store.delete(key)
            return "OK"
