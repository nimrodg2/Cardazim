import Connection
import socket


class Listener:
    def __init__(self, host, port, backlog=1000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()

    def __repr__(self):
        return "Listener(port=" + str(self.port) + ", host=" + self.host + ", backlog=" + str(self.backlog)

    def start(self):
        self.conn.bind((self.host, self.port))
        self.conn.listen()
        return

    def stop(self):
        self.conn.close()

    def accept(self):
        conn, addr = self.conn.accept()
        return connection.connection(conn)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


with Listener(5000, '127. 0.0.1') as listener:
    with listener.accept() as connection:
        pass
