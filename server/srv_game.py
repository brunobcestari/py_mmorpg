import socket
from threading import Thread

host = '127.0.0.1'
port = 5556
address = (host, port)

max_clients_allowed = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind(address)
except socket.error as e:
    print(e)

sock.listen(max_clients_allowed)
print(f"Server started at {address}")


def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    connected = True

    while connected:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected ...")
                connected = False
            else:
                print("Received: ", reply)
                print("Sending: ", reply)
            conn.sendall(str.encode(reply))
        except EOFError:
            print(f"Client socket has closed")
        except Exception as error:
            print("Error:", error)

    print("Lost connection ...")
    conn.close()


while True:
    conn, addr = sock.accept()
    print('Connection established', addr)

    Thread(target=threaded_client(conn)).start()
