"""Universal utilities"""
from binascii import Error as BinasciiError
from base64 import b64decode
from socket import socket as Socket


def validate_data(data: bytes):
    """Validate if data is base64 blob, return empty bytes if invalid. Return decoded if valid."""
    try:
        return b64decode(data)
    except BinasciiError:
        return b""


def _read(conn: Socket):
    data = conn.recv(1024)
    if not data:
        return b""
    while not data.endswith(b"\r\n"):
        more_data = conn.recv(1024)
        if not more_data:
            break
        data += more_data
    return data
