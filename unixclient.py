"""Test Client"""
from time import sleep
from socket_wrapper.client import UNIXClient as Client

client = Client("server.sock")

client.start()

client.send("Hello, World!")

sleep(1)

print(client.block_read())

client.send("Hello, World!!")

print(client.block_read())

client.stop()
