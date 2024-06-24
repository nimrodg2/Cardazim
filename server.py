import argparse
import sys
import socket
import threading
import time

I_should_kms = False


# not good at all....
def get_msg(conn: socket.socket, addr: tuple, lock: threading.Lock) -> None:
    lock.acquire()
    data_len = conn.recv(4)
    data_len = int.from_bytes(data_len, 'little')
    # if data len is very big, maybe reading 4096 at a time is better?
    data = conn.recv(data_len)
    data = data.decode()
    print(data)
    conn.close()
    lock.release()
    if data == "kys":
        global I_should_kms
        I_should_kms = True
    return


def kms(threads):
    for t in threads:
        t.join()
    exit()


def run_server(ip: str, port: int) -> None:
    global I_should_kms
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server_lock = threading.Lock()
    threads = []
    while True:
        server.listen()
        conn, addr = server.accept()
        t1 = threading.Thread(target=get_msg, args=(conn, addr, server_lock))
        t1.start()
        threads.append(t1)
        if I_should_kms:
            kms(threads)


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
