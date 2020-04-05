import argparse
import socket
import time


def get_answer(request):
    time.sleep(0.0)
    str_request = request.decode()
    answer = str_request + ' OK.'
    return str.encode(answer)


def parse_command_line(description):
    """Analisa a linha de comando e retorna um endereco de soquete"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port (default 1060')
    args = parser.parse_args()
    address = (args.host, args.p)
    return address


def get_address(host, port):
    address = (host, port)
    return address


def create_srv_socket(address):
    """Constrói e retorna um soquete de escuta do servidor"""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print(f'Server started at {address}')
    return listener


def accept_connections_forever(listener):
    while True:
        sock, address = listener.accept()
        print(f'Accepted connection from {address}')
        handle_conversation(sock, address)


def handle_conversation(sock, address):
    try:
        while True:
            handle_request(sock)
    except EOFError:
        print(f'Client socket to {address} has closed')
    except Exception as e:
        print(f'Client {address} error: {e}')
    finally:
        sock.close()


def handle_request(sock):
    aphorism = recv_until(sock, b'?')
    answer = get_answer(aphorism)
    sock.sendall(answer)


def recv_until(sock, suffix):
    message = sock.recv(4096)
    if not message:
        raise EOFError('socket closed')
    while not message.endswith(suffix):
        data = sock.recv(4096)
        if not data:
            raise IOError('received {!r} then socket closed'.format(message))
        message += data
    return message
