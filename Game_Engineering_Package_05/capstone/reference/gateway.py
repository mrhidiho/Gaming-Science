"""Finite-resource, loopback-only teaching gateway. One frame per connection.

The single acceptor serializes connection handling; Service has separately bounded
jobs. There is no authentication or encryption. Do not change the bind address.
"""
from concurrent.futures import CancelledError
import json
import socket
import threading
import time
from python.reference.lab_19_1 import encode_frame,recv_frame
from capstone.reference.service import Service,BusyError,WorkerError

class Gateway:
    def __init__(self, service: Service):
        self.service = service
        self.stop_event = threading.Event()
        self.errors = []
        self.listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.listener.bind(("127.0.0.1",0))
            self.listener.listen(4)
            self.listener.settimeout(0.1)
        except BaseException:
            self.listener.close()
            raise
        self.address = self.listener.getsockname()
        self.thread = threading.Thread(target=self._serve,name="forge-loopback")

    def _serve(self):
        while not self.stop_event.is_set():
            try:
                peer,_ = self.listener.accept()
            except socket.timeout:
                continue
            except OSError as error:
                if not self.stop_event.is_set():
                    self.errors.append(repr(error))
                break
            with peer:
                try:
                    payload = recv_frame(peer,time.monotonic()+1.0)
                    response = self.service.submit(payload).result(timeout=2.0)
                except (TimeoutError, socket.timeout):
                    response = {"status":"error","code":"UNKNOWN_OUTCOME",
                                "message":"Retry the same ID and payload; work may have committed."}
                except (ValueError,EOFError):
                    response = {"status":"error","code":"INVALID_REQUEST"}
                except BusyError:
                    response = {"status":"error","code":"BUSY"}
                except CancelledError:
                    response = {"status":"error","code":"CANCELLED"}
                except WorkerError:
                    response = {"status":"error","code":"WORKER_FAILED"}
                except Exception as error:
                    self.errors.append(type(error).__name__)
                    response = {"status":"error","code":"INTERNAL_ERROR"}
                try:
                    peer.settimeout(1.0)
                    peer.sendall(encode_frame(json.dumps(response,sort_keys=True).encode("utf-8")))
                except OSError:
                    pass # Lost reply is not evidence of a rolled-back transaction.

    def start(self):
        self.thread.start()
        return self

    def close(self):
        self.stop_event.set()
        self.listener.close()
        self.thread.join(timeout=5.0)
        if self.thread.is_alive():
            raise RuntimeError("gateway did not stop within the lab shutdown budget")

    def __enter__(self):
        return self.start()

    def __exit__(self,*_):
        self.close()


def exchange(address: tuple, payload: bytes, split: bool = False) -> dict:
    with socket.create_connection(address,timeout=2.0) as peer:
        wire = encode_frame(payload)
        if split:
            # TCP may coalesce these writes. Incremental-parser unit tests force
            # exact split points independently of actual OS segmentation.
            peer.sendall(wire[:2]); peer.sendall(wire[2:5]); peer.sendall(wire[5:])
        else:
            peer.sendall(wire)
        raw = recv_frame(peer,time.monotonic()+4.0)
    return json.loads(raw.decode("utf-8"))
