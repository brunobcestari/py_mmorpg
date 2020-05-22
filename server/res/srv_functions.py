import socket
import time
from server.res.srv_treatments import treat_answer
from _thread import start_new_thread


class Server:

    def __init__(self, host, port, max_clients):
        self.connected = 0
        self.chars = dict()
        self.host = host
        self.port = port
        self.address = (host, port)
        self.listener = self.create_srv_socket(max_clients)

    def create_srv_socket(self, max_clients):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(self.address)
        listener.listen(max_clients)
        print(f'Server started at {self.address}')
        return listener

    def listening_clients(self):
        while True:
            sock, address = self.listener.accept()
            print(f'Accepted connection from {address}')
            self.connected += 1
            print(self.connected)
            print(self.chars)
            start_new_thread(self.handle_conversation, (sock, address))

    def handle_conversation(self, sock, address):
        identifier = sock.recv(2048).decode()
        state = get_character_state(identifier)
        self.chars.update({address: identifier})
        sock.send(str.encode(state))

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

        self.connected -= 1
        del self.chars[address]
        sock.close()


def get_answer(request, identifier):
    time.sleep(0.0)
    str_request = request.decode()
    answer = treat_answer(str_request, identifier)
    return str.encode(str(answer))


def get_character_state(identifier):
    with open(f'{identifier}.json', 'r') as file:
        state = file.read()
        file.close()
        return state


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
