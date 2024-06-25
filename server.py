import argparse
import sys
from card import Card
from card_manager import CardManager
import os
import socket
import threading
import time

import Connection
import listener

# not good at all....
"""def get_msg(conn: socket.socket, addr: tuple, lock: threading.Lock) -> None:
    lock.acquire()
    data_len = conn.recv(4)
    a = data_len
    data_len = int.from_bytes(data_len, 'little')
    # if data len is very big, maybe reading 4096 at a time is better?
    data = conn.recv(data_len)
    a += data
    data = data.decode()
    print(data)
    conn.send(a)
    conn.close()
    lock.release()
    exit()
    return


def run_server(ip: str, port: int) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server_lock = threading.Lock()
    while True:
        server.listen()
        conn, addr = server.accept()
        t1 = threading.Thread(target=get_msg, args=(conn, addr, server_lock))
        t1.start()"""


def run_server(ip: str, port: int, path: str) -> None:
    with listener.Listener(ip, port) as server:
        while True:
            with server.accept() as connection:
                new_data = connection.receive_message()
                new_card = Card.deserialize(new_data)
                print("Received card")
                cm = CardManager()
                cm.save(new_card, path)
                saved_path = os.path.join(path, CardManager.generate_identifier(new_card))
                print("Saved card to path " + saved_path)


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('path', type=str,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port, args.path)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
