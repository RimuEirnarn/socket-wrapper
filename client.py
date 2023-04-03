"""Test Client"""
from time import sleep
from socket_wrapper.client import Client

client = Client("127.0.0.1", 2000)

client.start()

client.send("Hello, World!")

sleep(1)

print(client.block_read())

client.send("Hello, World!!")

print(client.block_read())

client.stop()
