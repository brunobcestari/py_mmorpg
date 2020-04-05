from server.res.srv_functions import *

host = '127.0.0.1'
port = 1060
max_clients_allowed = 2


if __name__ == '__main__':

    # address = parse_command_line("Used for executing by terminal")
    address = (host, port)
    listener = create_srv_socket(address, max_clients_allowed)
    listening_clients(listener)
