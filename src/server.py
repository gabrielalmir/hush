import asyncio
from .resp import parse_resp, serialize_resp
from .cache import Cache
from .queue import Queue

class HushServer:
    def __init__(self):
        self.cache = Cache()
        self.queue = Queue()

    async def handle_command(self, command):
        if not command or not isinstance(command, list):
            return "ERR"
        cmd = command[0].upper()

        try:
            if cmd == "SET" and len(command) >= 3:
                ttl = None
                if len(command) > 4 and command[3].upper() == "EX":
                    ttl = float(command[4])
                if len(command) > 4 and command[3].upper() == "PX":
                    ttl = float(command[4]) / 1000

                return await self.cache.set(command[1], command[2], ttl)
            elif cmd == "GET" and len(command) == 2:
                return await self.cache.get(command[1])
            elif cmd == "DEL" and len(command) == 2:
                return await self.cache.delete(command[1])
            elif cmd == "LPUSH" and len(command) >= 3:
                return await self.queue.lpush(command[1], *command[2:])
            elif cmd == "BLPOP" and len(command) >= 3:
                return await self.queue.blpop(command[1:-1], float(command[-1]))
            else:
                return "ERR"
        except Exception as e:
            return f"ERR {str(e)}"

async def handle_client(server, reader, writer):
    while True:
        try:
            command = await parse_resp(reader)
            if command is None:
                break
            response = await server.handle_command(command)
            writer.write(serialize_resp(response))
            await writer.drain()
        except Exception as e:
            writer.write(serialize_resp(f"ERR {str(e)}"))
            await writer.drain()
            break
    writer.close()
    await writer.wait_closed()

async def run_server(host='0.0.0.0', port=6379):
    server = HushServer()
    tcp_server = await asyncio.start_server(lambda r, w: handle_client(server, r, w), host, port)
    async with tcp_server:
        await tcp_server.serve_forever()
