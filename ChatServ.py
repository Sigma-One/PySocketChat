import socket, sys, threading, time
#from multiprocessing import Queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

clients = []

name_map = {}

host = socket.gethostname()

port = 9999

server.bind((host, port))

server.listen(25)

threads = []

def log(text):
    try:
        print("LOG: " + text.strip())
    except:
        print("LOG: ", text)

def serve(sock, addr):
    try:
        client.send(("ENTER NAME: ").encode("utf8"))
        name = client.recv(1024).decode("utf8").strip()

        client_info = (name + "@" + addr[0]).strip()

        log("Client" + client_info + "ready")
    except:
        log("Name retrieving failed")

    for i in clients:
        try:
            #print(clients)
            i.send(("### " + client_info + " joined ###").encode("utf8"))

        except BrokenPipeError or ConnectionResetError:
            log("Could not send join message for" + client_info + "to" + i.getsockname()[0])

    while True:
        try:
            data = sock.recv(1024).decode("utf8")

            if data == "":
                log("Invalid data from " + client_info)
                break

            data = "<" + name + "> " + data
            log(data)
            data = data.encode("utf8")
            for i in clients:
                #print(clients)
                i.send(data)

        except:
            break

    for i in clients:
        try:
            #print(clients)
            i.send(("### " + client_info + " left ###").encode("utf8"))
        except:
            log("LOG: Could not send leave message for" + client_info + "to" + i.getsockname()[0])

    log(client_info + " hung up, closing socket")
    sock.close()
    clients.remove(sock)
    log("Cleanup for" + client_info + " done, stopping thread")
    return 0

while True:
    client, address = server.accept()
    log("Connection from " + address[0])
    #print(clients)
    clients.append(client)
    threads.append(threading.Thread(target=serve, args=(client, address)))
    threads[len(threads) - 1].start()
