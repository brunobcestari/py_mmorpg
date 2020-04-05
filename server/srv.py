from server.res.srv_functions import *

host = '127.0.0.1'
port = 1060

if __name__ == '__main__':

    address = get_address(host=host, port=port)
    listener = create_srv_socket(address)
    accept_connections_forever(listener)
