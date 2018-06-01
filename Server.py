#############    #######    #######
     #     #    #          #     #
    #     #    #          #          #####  #####  #####  #   #  #####  #####
   ##################    #          #      #      #   #   #  #  #      #   #
  #                #    #          #####  #####  #####    # #  #####  #####
 #                #    #     #        #  #      #  #      ##  #      #  #
#          ##################    #####  #####  #    #     #  #####  #    #

# Crappy ASCII Art ^^
# PySocketChat(PSC) Server ~ SigmaOne ~ 2018

# !important
# If you are just some regular person wanting to run a server and add custom features (Commands, etc.), don't touch this!
# Use Custom.py for your custom features instead!
# However, if you know python and want to help this thing progress, go on ahead with this code!

import socket
import threading
import json
import time

from Logger import Logger

client_list = []

try:
  # Create a TCP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

except socket.error, err_msg:
    Logger.log("Socket creation failure", 2)
    Logger.log("ERR_NO: " + str(err_msg[0]), 2)
    Logger.log("ERR_MSG: " + err_msg[1], 2)
    exit(1);

Logger.log("Socket created succesfully")

# Ask user for server port
port = int(input("Port to host server on: "))
host = socket.gethostname()

try:
  # bind socket to host and port
  Logger.log("Binding socket to port " + str(port) + " on host " + host, 0)
  sock.bind((host, port))
  sock.listen(25)

except socket.error, err_msg:
  Logger.log("Bind failed", 2)
  Logger.log("ERR_NO: " + str(err_msg[0]), 2)
  Logger.log("ERR_MSG: " + err_msg[1], 2)
  exit(1)

Logger.log("Binding succesful")

def send_message(client, msg_type, msg):
  """
  Sends a message of a specified type to a single client
  Params:
    - client (socketobject): The client socket to send the message to
    - msg_type (string):     The type of the message, i.e. "TMSG" for a regular text message
    - msg (string):          The actual message body
  """

  final_msg = {}
  final_msg[msg_type] = msg
  client.send(json.dumps(final_msg))

def mainloop(client, addr):
  """
  Handles receiving messages from a specific client and processing them
  e.g. Client0 send message "Hello, World!" of type "MSG", mainloop detects the type and decides that this will be forwarded to everyone
  Params:
    - client (array): Array containing the client socketobject on index 0, and the client info dictionary on index 1
    - addr (tuple): Tuple containing the client IP address on index 0, and some integer which I do not understand on index 1
  """

  while True:
    try:
      # Receive and load data from users
      raw_data = json.loads(client[0].recv(1024))
      data = [raw_data.keys()[0], raw_data[raw_data.keys()[0]]]

      Logger.log("Received data from " + addr[0], 0)

      # Process message per type
      if data[0] == "QUIT":
        # User has quit in a controlled manner, server cleans up details
        Logger.log(addr[0] + " disconnected correctly")
        client_list.remove(client)
        break

      elif data[0] == "SINF":
        # User wants to set info about themself
        # TODO: Only allow predetermined info types to avoid flooding the server memory

        Logger.log("Setting info value " + data[1][0] + " for " + addr[0] + " to " + data[1][1])
        for i in client_list:
          send_message(i[0], "TMSG", time.strftime("<%H:%M:%S> ") + client[1]["NAME"] + " changed their " + data[1][0].lower() + " to " + data[1][1])

        client[1][data[1][0]] = data[1][1]

      elif data[0] == "TMSG":
        # User has sent a normal text-based message, server adds timestamp and username and forwards message to everyone
        Logger.log("Adding details and forwarding message to all clients", 0)
        for i in client_list:
          send_message(i[0], "TMSG", time.strftime("<%H:%M:%S> ") + client[1]["NAME"] + ": " + data[1])

    except ValueError, TypeError:
      # User disconnects unexpectedly, this cleans up the mess they caused
      Logger.log(addr[0] + " broke connection", 1)
      client_list.remove(client)
      break


while True:
  # Handles giving each client a thread running the main loop
  client, address = sock.accept()

  # Set default user info
  client = [client, {"NAME" : "Anon"}]

  Logger.log("Connection from " + address[0])
  print(address)
  client_list.append(client)
  print(client_list)

  # Create and start thread
  thread = threading.Thread(target=mainloop, args=(client, address))
  thread.start()
