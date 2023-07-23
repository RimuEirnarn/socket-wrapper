"""Unix Server"""

from selectors import DefaultSelector, EVENT_READ
from socket import socket as Socket, SOCK_STREAM, SHUT_RDWR

try:
    from socket import AF_UNIX
except ImportError: # Feature Error
    AF_UNIX = -100

from os import remove
from .errors import FeatureError
from .typings import Addr
from .utils import validate_data, _read
from ._base import BaseConnection

class UNIXServer(BaseConnection):
    """Base Server class."""

    def __init__(self, path: str, connections: int = 0):
        if AF_UNIX == -100:
            raise FeatureError("Unix socket feature is missing.")
        super().__init__(path, 0)
        self._running = False
        self._sel = DefaultSelector()
        self._server_sock = Socket(AF_UNIX, SOCK_STREAM)
        self._server_sock.bind(path)
        self._server_sock.listen()
        self._server_sock.setblocking(False)
        self._sel.register(self._server_sock, EVENT_READ, self._incoming)
        self._clients: list[Socket] = []
        self._allows = connections
        self._path = path

    def run(self):
        """Run server logic. This is used by `.start` function"""
        if self._running:
            return

        self._running = True
        try:
            while self._running:
                for key, _ in self._sel.select(1):
                    callback = key.data
                    callback(key.fileobj)
        except KeyboardInterrupt:
            self.stop()
            return

    def _on_reject(self, sock: Socket, addr: Addr):
        sock.send(b'\r\n')
        sock.close()

    def _incoming(self, sock: Socket):
        conn, addr = sock.accept()
        if len(self._clients) >= self._allows and self._allows != 0:
            self._on_reject(conn, addr)
            return
        self._on_accept(conn, addr)

    def _on_accept(self, sock: Socket, addr: Addr):
        sock.setblocking(False)
        self._clients.append(sock)
        self._sel.register(sock, EVENT_READ, self._receive_data)

    def stop(self):
        """Stop server thread"""
        for sock in self._clients.copy():
            self._close(sock)
        self._running = False
        self._server_sock.shutdown(SHUT_RDWR)
        remove(self._path)

    def _on_close(self, sock: Socket):  # pylint: disable=unused-argument
        return

    def _close(self, sock: Socket):
        self._on_close(sock)
        self._sel.unregister(sock)
        sock.close()
        self._clients.remove(sock)

    def _on_receive(self, sock: Socket, data: bytes, raw: bytes):
        print(data)
        sock.send(raw)

    def _receive_data(self, conn: Socket):
        try:
            data = _read(conn)
            if not data:
                self._close(conn)
                return
            decoded_data = validate_data(data[:-2])
            if decoded_data:
                # Do something with the data
                self._on_receive(conn, decoded_data, data)
            else:
                # Invalid data
                pass
        except Exception:
            self._close(conn)
