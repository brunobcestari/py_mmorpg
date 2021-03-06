import socket


class Network:

    def __init__(self, identifier, server='localhost', port=1060):
        self.identifier = identifier
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.state = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.send(str.encode(self.identifier))
            return self.client.recv(2048).decode()
        except Exception as error:
            print(f"Error while connecting to {self.addr}")
            print(error)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as error:
            print(error)

