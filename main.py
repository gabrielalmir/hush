import sys
import asyncio
from src.server import run_server

def arg(name: str, default: str = None) -> str:
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default

if __name__ == "__main__":
    port = int(arg("--port", "6379"))
    host = arg("--host", "0.0.0.0")

    print(f"Server running at {host}:{port}")
    asyncio.run(run_server(host, port))
