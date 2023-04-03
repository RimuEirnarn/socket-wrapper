"""Server test"""
from socket_wrapper.server import Server

server = Server("127.0.0.1", 2000)

server.run()
