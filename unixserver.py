"""Server test"""
from socket_wrapper.server import UNIXServer as Server

server = Server("server.sock")

server.run()
