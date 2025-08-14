from src.errors import InvalidRespProtocol

async def parse_resp(reader):
    header = await reader.read(1)

    if not header:
        return None

    match header:
        case b'*':
            num_args = int((await reader.readline()).decode().strip())
            args = []
            for _ in range(num_args):
                arg = await parse_resp(reader)
                args.append(arg)
            return args
        case b'$':
            length = int((await reader.readline()).decode().strip())
            if length == -1:
                return None
            data = await reader.readexactly(length)
            await reader.readline()  # Consume the CRLF
            return data
        case b'+':
            return (await reader.readline()).decode().strip()
        case b':':
            return int((await reader.readline()).decode().strip())
        case _:
            raise InvalidRespProtocol("Invalid RESP protocol")

def serialize_resp(response):
    if response is None:
        return b"$-1\r\n"
    elif response == "OK":
        return b"+OK\r\n"
    elif isinstance(response, str):
        return f"${len(response)}\r\n{response}\r\n".encode()
    elif isinstance(response, int):
        return f":{response}\r\n".encode()
    elif isinstance(response, list):
        parts = [f"*{len(response)}\r\n".encode()]
        for item in response:
            parts.append(serialize_resp(item))
        return b''.join(parts)
    else:
        return b"-ERR\r\n"
