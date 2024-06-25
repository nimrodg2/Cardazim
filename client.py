import argparse
import sys
from card import Card
import socket
import time

import Connection
import listener

###########################################################
####################### YOUR CODE #########################
###########################################################


"""def send_data(server_ip, server_port, data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    msg = data.encode()
    client.send(len(msg).to_bytes(4, 'little') + msg)
    client.close()
    return"""


def send_data(server_ip, server_port, new_card: Card):
    new_card.image.encrypt(new_card.solution)
    data = new_card.serialize()
    with Connection.Connection.connect(server_ip, server_port) as connection:
        connection.send_message(data)


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('name', type=str,
                        help='the data')
    parser.add_argument('creator', type=str,
                        help='the data')
    parser.add_argument('riddle', type=str,
                        help='the data')
    parser.add_argument('solution', type=str,
                        help='the data')
    parser.add_argument('path', type=str,
                        help='the data')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        new_Card = Card.create_from_path(args.name, args.creator, args.path, args.riddle, args.solution)
        send_data(args.server_ip, args.server_port, new_Card)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
