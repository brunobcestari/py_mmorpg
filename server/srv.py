from res.srv_functions import *
import argparse

host = '127.0.0.1'
port = 1060
max_clients_allowed = 2


def parse_command_line(description):
    """ Para iniciar o servidor atraves da linha de comando: Analisa a linha de comando e retorna um endereco de
    soquete """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port (default 1060')
    args = parser.parse_args()
    return args.host, args.p


if __name__ == '__main__':

    # host, port = parse_command_line("Used for executing by terminal command")
    srv = Server(host, port, max_clients_allowed)
    srv.listening_clients()
