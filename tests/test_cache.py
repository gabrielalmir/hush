import asyncio
import pytest

from src.cache import Cache

@pytest.mark.asyncio
async def test_cache_set_get():
    cache = Cache()
    assert await cache.set('key', 'value', 1) == 'OK'
    assert await cache.get('key') == 'value'
    await asyncio.sleep(1.1)
    assert await cache.get('key') is None

@pytest.mark.asyncio
async def test_cache_delete():
    cache = Cache()
    assert await cache.set('key', 'value', 1) == 'OK'
    assert await cache.get('key') == 'value'
    assert await cache.delete('key') == 'OK'
    assert await cache.get('key') is None
