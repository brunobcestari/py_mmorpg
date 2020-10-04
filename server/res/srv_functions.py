import socket
import time
from .srv_treatments import treat_answer
from _thread import start_new_thread
from pymongo import MongoClient


class Server:

    def __init__(self, host, port, max_clients, database_host='localhost', database_port=27017):
        self.connected = 0
        self.chars = dict()
        self.host = host
        self.port = port
        self.address = (host, port)
        self.listener = self.create_srv_socket(max_clients)

        self.mongo_db = MongoClient(database_host, database_port)["mmorpg_db"]
        self.characters_db = self.connect_collection()

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
            start_new_thread(self.handle_conversation, (sock, address))
            self.connected += 1
            print("Players connected:", self.connected)

    def handle_conversation(self, sock, address):
        identifier = sock.recv(2048).decode()
        state = self.get_character_state(identifier)
        self.chars.update({address: identifier})
        print(self.chars)
        sock.send(str(state).encode())

        connected = True
        while connected:
            try:
                while True:
                    self.handle_request(sock, state)

            except EOFError as e:
                print(f'Client socket to {address} has closed')
                connected = False
            except Exception as e:
                print(f'Client {address} error: {e}')
                connected = False

        self.connected -= 1
        del self.chars[address]
        sock.close()

    def handle_request(self, sock, actual_state):
        request = receive(sock)
        answer = get_answer(request, actual_state)

        #updating mongodb
        query = {"ID":answer.get("ID")}
        new_values = {"$set": answer}
        self.characters_db.update_one(query, new_values)
        sock.sendall(str.encode(str(answer)))

    def connect_collection(self):

        if 'characters' in self.mongo_db.list_collection_names():
            return self.mongo_db['characters']
        else:
            self.mongo_db.create_collection('characters')
            return self.mongo_db['characters']

    def get_character_state(self, identifier):
        character = self.characters_db.find_one({"ID": identifier})
        if not character:
            print("NEW CHARACTER!!!!", identifier)
            character = {'ID': identifier,
                         'name': identifier,
                         'position': [0, 0, 0],
                         'health': 100,
                         'mana': 100,
                         'stamina': 100}
            self.characters_db.insert_one(character)
        return character


def get_answer(request, actual_state):
    time.sleep(0.0)
    str_request = request.decode()
    answer = treat_answer(str_request, actual_state)
    return answer


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
