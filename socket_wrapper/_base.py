"""Base of connection types. Well, for Server and Clients"""
# pylint: disable=unused-argument
from threading import Thread
from socket import socket as Socket


class BaseConnection:
    """Base Connection"""

    def __init__(self, host: str, port: int):
        self._thread = None

    @property
    def thread(self):
        """Server thread"""
        if not isinstance(self._thread, Thread):
            raise ValueError("Server thread is not initialised.")
        return self._thread

    @thread.setter
    def thread(self, thread: Thread):
        """Server thread"""
        if not isinstance(thread, Thread):
            raise TypeError("Expected thread type.")
        self._thread = thread

    def start(self):
        """Start server thread"""
        self.thread = Thread(target=self.run)
        self.thread.start()
        return self.thread

    def run(self):
        """Run server logic. This is used by `.start` function"""
        return NotImplemented

    def _on_reject(self, sock: Socket):
        return NotImplemented

    def _on_accept(self, sock: Socket):
        return NotImplemented

    def stop(self):
        """Stop server thread"""
        self.thread.join()

    def _close(self, sock: Socket):
        return NotImplemented

    def _on_receive(self, sock: Socket, data: bytes, raw: bytes):
        return NotImplemented

    def _receive_data(self, conn: Socket):
        return NotImplemented
