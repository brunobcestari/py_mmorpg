import socket


class Network:

    def __init__(self, server='127.0.0.1', port=5556):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addr)
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


if __name__ == '__main__':
    n = Network()
    print(n.send("Hello"))
    print(n.send("Working!!!"))
