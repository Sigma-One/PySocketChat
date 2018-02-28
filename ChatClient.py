import socket
import threading
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 9999

client.connect((host, port))

def get_input():
    while True:
        message = input()
        client.send(message.encode("utf8"))

def write_messages():
    global cache_file
    while True:
            sys.stdout.write(client.recv(1024).decode("utf8") + "\n")

sys.stdout.write(client.recv(1024).decode("utf8"))
client.send(input().encode("utf8"))

sender = threading.Thread(target=get_input)
sender.start()

receiver = threading.Thread(target=write_messages)
receiver.start()
