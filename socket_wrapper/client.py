"""Client"""
from selectors import DefaultSelector, EVENT_READ
from socket import socket as Socket, AF_INET, SOCK_STREAM
from base64 import b64encode
from time import sleep

from .utils import validate_data, _read
from ._base import BaseConnection


class Client(BaseConnection):
    """Base Client class."""

    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self._sel = DefaultSelector()
        self._sock = Socket(AF_INET, SOCK_STREAM)
        self._sock.connect((host, port))
        self._sock.setblocking(False)
        self._sel.register(self._sock, EVENT_READ, self._receive_data)
        self._received_data = b""
        self._running = False

    def read(self) -> str:
        """Read decoded data"""
        data = validate_data(self._received_data).decode('utf-8')
        self._received_data = b''
        return data

    def block_read(self):
        """Read decoded data... but blocked?"""
        while self._received_data == b'':
            sleep(1)
        return self.read()

    def send(self, data: str):
        """Send data to server"""
        packed = b64encode(data.encode('utf-8'))
        return self._sock.send(packed + b"\r\n")

    def run(self):
        """Run client logic. This is used by `.start` function."""
        if self._running:
            return

        self._running = True
        while self._running:
            try:
                events = self._sel.select(1)
                for key, _ in events:
                    self._receive_data(key.fileobj)  # type: ignore
            except Exception:
                self._running = False

    def stop(self):
        """Stop client thread."""
        self._running = False
        self._sock.close()
        self.thread.join()

    def _receive_data(self, conn: Socket):
        try:
            received_data = b''
            data = _read(conn)
            received_data += data[:-2]
            if validate_data(received_data):
                # Do something with the data
                self._received_data = data[:-2]
        except OSError:
            self._sel.unregister(conn)
            conn.close()
