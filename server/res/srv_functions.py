import argparse
import socket
import time
from server.res.srv_treatments import treat_answer


def get_answer(request, identifier):
    time.sleep(0.0)
    str_request = request.decode()
    print("Received:", str_request)
    answer = treat_answer(str_request, identifier)
    print("Sending:", answer)
    return str.encode(str(answer))


def parse_command_line(description):
    """Analisa a linha de comando e retorna um endereco de soquete"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port (default 1060')
    args = parser.parse_args()
    address = (args.host, args.p)
    return address


def create_srv_socket(address, max_clients):
    """Constrói e retorna um soquete de escuta do servidor"""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(max_clients)
    print(f'Server started at {address}')
    return listener


def listening_clients(listener):
    while True:
        sock, address = listener.accept()
        print(f'Accepted connection from {address}')
        identifier = sock.recv(2048).decode()
        state = get_character_state(identifier)
        sock.send(str.encode(state))
        handle_conversation(sock, address, identifier)


def get_character_state(identifier):
    with open(f'{identifier}.json', 'r') as file:
        state = file.read()
        file.close()
        return state


def handle_conversation(sock, address, identifier):
    reply = ""
    connected = True
    while connected:
        try:
            while True:
                handle_request(sock, identifier)

        except EOFError:
            print(f'Client socket to {address} has closed')
            connected = False
        except Exception as e:
            print(f'Client {address} error: {e}')
            connected = False

    sock.close()


def handle_request(sock, identifier):
    request = receive(sock)
    answer = get_answer(request, identifier)
    sock.sendall(answer)


def receive(sock, suffix=False):
    message = sock.recv(2048)
    if not message:
        raise EOFError('socket closed')

    if suffix:
        while not message.endswith(suffix):
            data = sock.recv(2048)
            if not data:
                raise IOError('received {!r} then socket closed'.format(message))
            message += data
    return message
