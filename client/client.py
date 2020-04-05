import socket

server_address = '127.0.0.1'
server_port = 1060
address = (server_address, server_port)


def recv_until(sock, suffix):
    message = sock.recv(4096)
    if not message:
        raise EOFError('socket closed')
    while not message.endswith(suffix):
        data = sock.recv(4096)
        if not data:
            raise IOError('received {!r} then socket closed'.format(message))
        message += data
    return message.decode()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    message = input("Type your message!")
    message += '?'
    b_message = str.encode(message)

    sock.sendall(b_message)
    print(recv_until(sock, b'.'))
    sock.close()


if __name__ == '__main__':
    main()
