import socket
from client.res.network import Network

server_address = '127.0.0.1'
server_port = 1060
address = (server_address, server_port)


def recv_until(sock, suffix=False):
    message = sock.recv(2048)
    if not message:
        raise EOFError('socket closed')
    if suffix:
        while not message.endswith(suffix):
            data = sock.recv(4096)
            if not data:
                raise IOError('received {!r} then socket closed'.format(message))
            message += data
    return message.decode()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    connected = True
    while connected:
        try:
            message = input("Type your message!\n")
            b_message = str.encode(message)
            if message == "Exit":
                b_message = str.encode("Disconnecting ... ")
                connected = False
            sock.sendall(b_message)
            print(recv_until(sock))
        except Exception as error:
            print(error)
            connected = False

    sock.close()


if __name__ == '__main__':
    n = Network(server=server_address, port=server_port)
    print(n.send("Testing"))
