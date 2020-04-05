import argparse
import socket
import time
from server.res.srv_treatments import move


def get_answer(request):
    time.sleep(0.0)
    str_request = request.decode()
    print("Received:", str_request)
    answer = treat_answer(str_request)
    print("Sending:", answer)
    return str.encode(str(answer))


def treat_answer(request):
    answer = eval(request)
    # do the treatment here
    new_position = answer["position"]
    new_position = move((0, 0, 0), new_position)
    answer["position"] = new_position
    return answer


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
        sock.send(b"Server: Connected!")
        handle_conversation(sock, address)


def handle_conversation(sock, address):
    reply = ""
    connected = True
    while connected:
        try:
            while True:
                handle_request(sock)

        except EOFError:
            print(f'Client socket to {address} has closed')
            connected = False
        except Exception as e:
            print(f'Client {address} error: {e}')
            connected = False

    sock.close()


def handle_request(sock):
    request = receive(sock)
    answer = get_answer(request)
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
