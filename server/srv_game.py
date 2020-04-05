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


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


pos = [(0, 0), (100, 100)]


def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    connected = True
    while connected:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                connected = False
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except EOFError:
            print(f"Client socket has closed")
        except Exception as error:
            print("Error:", error)

    print("Lost connection ...")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = sock.accept()
    print('Connection established', addr)

    Thread(target=threaded_client(conn, currentPlayer)).start()
    currentPlayer += 1
