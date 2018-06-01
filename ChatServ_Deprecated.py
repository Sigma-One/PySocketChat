import socket
import sys
import threading
import json


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

clients = []

name_map = {}

host = socket.gethostname()

port = int(input("Please enter port to host on >> "))

server.bind((host, port))

server.listen(25)

threads = []

def log(text):
  try:
  print("LOG: " + text.strip())
  except:
  print("LOG: ", text)

def serve(sock, addr):
  # Set default client info
  client_info = {}
  client_info["ADDRESS"] = addr[0]
  client_info["NAME"] = "<Anonymous> "

  msg = {}
  msg["MSG"] = client_info["NAME"] + " @ " + client_info["ADDRESS"] + " joined"
  for i in clients:
  i.send(json.dumps(msg).encode("utf8"))

  # Main client loop
  while True:
    try:
    data = json.loads(sock.recv(1024))

    # Check message type
    if "MSG" in data.keys():
    # Message is message, send it forward
    data["MSG"] = client_info["NAME"] + data["MSG"]
    for i in clients:
    i.send(json.dumps(data).encode("utf8"))

    elif "NAME" in data.keys():
    # Message is name, set it as client name
    # Send info to clients
    msg = {}
    msg["MSG"] = client_info["NAME"] + " @ " + client_info["ADDRESS"] + " set their name to <" + data["NAME"] + ">"

    for i in clients:
    i.send(json.dumps(msg).encode("utf8"))

    # Set name
    client_info["NAME"] = "<" + data["NAME"] + "> "

    elif "QUIT" in data.keys():
    # Message is quit, disconnect client
    break
    except:
      print("Something Horrible Happened, disconnecting user")
      break


  # Disconnect and clean up
  log(client_info["NAME"] + "@ " + client_info["ADDRESS"] + " hung up, closing socket")
  print(clients)
  clients.remove(sock)
  print(clients)
  sock.close()
  del sock

while True:
  client, address = server.accept()
  log("Connection from " + address[0])
  clients.append(client)
  threads.append(threading.Thread(target=serve, args=(client, address)))
  threads[len(threads) - 1].start()
