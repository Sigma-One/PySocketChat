import socket
import threading
import sys
import tkinter

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 9999

client.connect((host, port))

root = tkinter.Tk()
frame = tkinter.Frame(root, bg="azure")
frame.grid(sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

message_box = tkinter.Text(root, wrap=tkinter.WORD)
message_box.grid(row=0, column=0, sticky="nsew")

def get_input():
    while True:
        message = input()
        client.send(message.encode("utf8"))

def write_messages():
    while True:
        message_received = client.recv(1024).decode("utf8")
        sys.stdout.write(message_received + "\n")
        message_box.insert("end", message_received + "\n")

sys.stdout.write(client.recv(1024).decode("utf8"))
client.send(input().encode("utf8"))

sender = threading.Thread(target=get_input)
sender.start()

receiver = threading.Thread(target=write_messages)
receiver.start()

root.mainloop()
