import socket
import threading


class Connection:

    def __init__(self, connection: socket.socket):
        self.con = connection
        self.lock = threading.Lock()

    def send_message(self, message: bytes):
        self.con.send(len(message).to_bytes(4, 'little') + message)

    def receive_message(self):
        data_len = self.con.recv(4)
        data_len = int.from_bytes(data_len, 'little')
        data = self.con.recv(data_len)
        data = data.decode()
        return data

    @classmethod
    def connect(cls, host, port):
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_con = Connection(new_sock)
        new_con.host = host
        new_con.port = port
        new_con.con.connect((host, port))
        return new_con

    def close(self):
        self.con.close()

    def __repr__(self):
        return "<Connection: " + self.host + " " + str(self.port) + ">"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


"""with Connection.connect('127.0.0.1', 5000) as connection:
    print(connection)
    connection.send_message(b'hello')
    connection.receive_message()
"""