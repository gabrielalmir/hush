import pytest
from src.resp import serialize_resp
from src.errors import InvalidRespProtocol

def test_serialize_resp():
    assert serialize_resp("OK") == b"+OK\r\n"
    assert serialize_resp(None) == b"$-1\r\n"
    assert serialize_resp(["key", "value"]) == b"*2\r\n$3\r\nkey\r\n$5\r\nvalue\r\n"

