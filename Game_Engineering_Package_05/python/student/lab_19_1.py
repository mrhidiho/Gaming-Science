"""Student exercise: deliberately unfinished. See LAB_WORKBOOK."""
MAX_PAYLOAD=4096
MAX_CHUNK=8192

def encode_frame(payload: bytes) -> bytes:
    raise NotImplementedError("19.1: validated length prefix")
class FrameDecoder:
    def __init__(self):
        self.buffer=bytearray()
        self.failed=False
        self.ended=False
    def feed(self,data):
        raise NotImplementedError("19.1: fragmented/coalesced stream")
    def finish(self):
        raise NotImplementedError("19.1: detect truncated EOF")
def recv_frame(sock,deadline):
    raise NotImplementedError("19.1: absolute deadline and exact reads")
