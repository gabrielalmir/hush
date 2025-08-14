import pytest
import asyncio

from src.resp import serialize_resp, parse_resp

def test_serialize_resp():
    assert serialize_resp("OK") == b"+OK\r\n"
    assert serialize_resp(None) == b"$-1\r\n"
    assert serialize_resp(["key", "value"]) == b"*2\r\n$3\r\nkey\r\n$5\r\nvalue\r\n"

@pytest.mark.asyncio
async def test_consume_crlf():
    data = b"$5\r\nhello\r\n"
    reader = asyncio.StreamReader()
    reader.feed_data(data)
    reader.feed_eof()
    assert await parse_resp(reader) == b"hello"

