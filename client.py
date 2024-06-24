import argparse
import sys
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


def send_data(server_ip, server_port, data):
    with Connection.Connection.connect(server_ip, server_port) as connection:
        connection.send_message(data.encode())


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('data', type=str,
                        help='the data')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
