# Hush

A lightweight, Redis-compatible in-memory data store implemented in Python with async/await support.

## Features

- **Redis Protocol Compatible**: Implements the RESP (Redis Serialization Protocol) for seamless integration with Redis clients
- **LRU Cache**: Built-in Least Recently Used cache with configurable capacity (default: 1000 items)
- **TTL Support**: Time-to-live functionality for automatic key expiration
- **Queue Operations**: Support for list operations like LPUSH and BLPOP
- **Async/Await**: Fully asynchronous implementation using Python's asyncio
- **Thread-Safe**: All operations are protected with async locks

## Supported Commands

### Cache Operations
- `SET key value [EX seconds]` - Set a key-value pair with optional TTL
- `GET key` - Retrieve the value for a key
- `DEL key` - Delete a key

### Queue Operations
- `LPUSH key value [value ...]` - Push values to the left of a list
- `BLPOP key [key ...] timeout` - Blocking pop from the left of lists

## Installation

### Prerequisites
- Python 3.12 or higher
- uv (recommended) or pip

### Using uv (recommended)
```bash
git clone https://github.com/gabrielalmir/hush
cd hush
uv sync
```

### Using pip
```bash
git clone https://github.com/gabrielalmir/hush
cd hush
pip install -e .
```

## Usage

### Starting the Server

```bash
# Using uv
uv run python main.py

# Using python directly
python main.py

# Custom port and host
python main.py --port 6380 --host 127.0.0.1
```

The server will start on `0.0.0.0:6379` by default (same as Redis).

### Connecting with Redis CLI

Since Hush implements the Redis protocol, you can use any Redis client:

```bash
# Using redis-cli
redis-cli -h localhost -p 6379

# Example commands
127.0.0.1:6379> SET mykey "Hello World"
OK
127.0.0.1:6379> GET mykey
"Hello World"
127.0.0.1:6379> SET tempkey "expires soon" EX 10
OK
127.0.0.1:6379> LPUSH mylist "item1" "item2"
(integer) 2
127.0.0.1:6379> BLPOP mylist 5
1) "mylist"
2) "item2"
```

### Using Python Redis Client

```python
import redis

# Connect to Hush server
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Cache operations
r.set('key1', 'value1')
print(r.get('key1'))  # Output: value1

# TTL operations
r.setex('temp_key', 10, 'expires in 10 seconds')

# Queue operations
r.lpush('myqueue', 'task1', 'task2')
result = r.blpop('myqueue', timeout=5)
print(result)  # Output: ('myqueue', 'task2')
```

## Architecture

### Components

- **HushServer**: Main server class that handles client connections and command routing
- **Cache**: LRU cache implementation with TTL support
- **Queue**: Queue operations using Python's deque for efficient list operations
- **RESP Parser**: Redis protocol parser and serializer

### Cache Implementation

- Uses a combination of hashmap and doubly-linked list for O(1) operations
- Automatic eviction of least recently used items when capacity is exceeded
- TTL-based expiration with automatic cleanup on access

### Concurrency

- All operations are async and use asyncio locks for thread safety
- Non-blocking I/O for handling multiple concurrent clients
- Efficient memory usage with Python's async/await patterns

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_cache.py
```

### Project Structure

```
hush/
├── src/
│   ├── __init__.py
│   ├── cache.py      # LRU cache implementation
│   ├── queue.py      # Queue operations
│   ├── resp.py       # Redis protocol parser
│   └── server.py     # Main server implementation
├── tests/
│   ├── test_cache.py
│   ├── test_queue.py
│   └── test_resp.py
├── main.py           # Server entry point
└── pyproject.toml    # Project configuration
```

## Performance Characteristics

- **Cache Operations**: O(1) average time complexity for GET, SET, DEL
- **Queue Operations**: O(1) for LPUSH, O(1) for BLPOP when items available
- **Memory Usage**: Efficient memory usage with automatic LRU eviction
- **Concurrency**: Supports multiple concurrent clients with async I/O

## Limitations

- In-memory only (data is not persisted to disk)
- Single-node deployment (no clustering support)
- Limited Redis command set (focused on core cache and queue operations)
- No authentication or access control

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Roadmap

- [ ] Additional Redis commands (HSET, HGET, SADD, etc.)
- [ ] Persistence options
- [ ] Configuration file support
- [ ] Metrics and monitoring
- [ ] Clustering support
- [ ] Authentication and authorization
