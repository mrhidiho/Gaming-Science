"""Four-byte big-endian length prefix, 1..4096 payload bytes."""
import socket
import struct
import time
MAX_PAYLOAD = 4096
MAX_CHUNK = 8192

def encode_frame(payload: bytes) -> bytes:
    if type(payload) is not bytes or not 1 <= len(payload) <= MAX_PAYLOAD:
        raise ValueError("payload must be 1..4096 bytes")
    return struct.pack("!I", len(payload)) + payload

class FrameDecoder:
    def __init__(self):
        self.buffer = bytearray()
        self.failed = False
        self.ended = False

    def feed(self, data: bytes) -> list[bytes]:
        if self.failed or self.ended:
            raise ValueError("decoder is closed")
        if type(data) is not bytes or len(data) > MAX_CHUNK:
            self.failed = True
            self.buffer.clear()
            raise ValueError("chunk must be at most 8192 bytes")
        self.buffer.extend(data)
        result = []
        while len(self.buffer) >= 4:
            size = struct.unpack("!I", self.buffer[:4])[0]
            if not 1 <= size <= MAX_PAYLOAD:
                self.failed = True
                self.buffer.clear()
                raise ValueError("invalid advertised length")
            if len(self.buffer) < 4 + size:
                break
            result.append(bytes(self.buffer[4:4+size]))
            del self.buffer[:4+size]
        return result

    def finish(self) -> None:
        self.ended = True
        if self.failed or self.buffer:
            self.failed = True
            self.buffer.clear()
            raise ValueError("truncated or invalid stream")

def recv_frame(sock: socket.socket, deadline: float) -> bytes:
    def read_exact(count: int) -> bytes:
        chunks = bytearray()
        while len(chunks) < count:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("frame deadline exceeded; remote outcome may be unknown")
            sock.settimeout(remaining)
            data = sock.recv(count-len(chunks))
            if not data:
                raise EOFError("connection closed before a complete frame")
            chunks.extend(data)
        return bytes(chunks)
    size = struct.unpack("!I", read_exact(4))[0]
    if not 1 <= size <= MAX_PAYLOAD:
        raise ValueError("invalid advertised length")
    return read_exact(size)
