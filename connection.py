import socket
import threading


class Connection:

    def __init__(self, connection: socket.socket):
        self.threads = None
        self.con = connection
        self.I_should_kms = False
        self.lock = threading.Lock()

    def send_message(self, message: bytes):
        self.con.connect((self.ip, self.port))
        self.con.send(len(message).to_bytes(4, 'little') + message)

    def get_msg(self, conn) -> None:
        self.lock.acquire()
        data_len = conn.recv(4)
        data_len = int.from_bytes(data_len, 'little')
        data = conn.recv(data_len)
        if len(data) != data_len:
            raise Exception
        data = data.decode()
        print(data)
        conn.close()
        self.lock.release()
        if data == "kys":
            self.I_should_kms = True
        return

    def receive_message(self):
        self.con.bind((self.ip, self.port))
        self.threads = []
        while True:
            self.con.listen()
            conn, addr = self.con.accept()
            t1 = threading.Thread(target=self.get_msg, args=(conn))
            t1.start()
            self.threads.append(t1)
            if self.I_should_kms:
                for t in self.threads:
                    t.join()
                exit()

    @classmethod
    def connect(cls, host, port):
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_con = Connection(new_sock)
        new_con.ip = host
        new_con.port = port
        return new_con

    def close(self):
        self.con.close()

    def __repr__(self):
        return '<Connection from ' + str(self.ip) + ':' + str(self.port) + ' to ' + str(self.ipt) + ':' + str(
            self.portt) + '>'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# WHAT

# in repr, there are "two" ip's and ports, but we only recieve one in connect

# why does innit not take self? is this a mistake?

# why does it recieve a socket? is this socket already connnected to anything? probably not so why? and when is it made if we
# make a new connection with "connect" ?? Do we call it in connect? then what is the use of puting anything inside innit?????

# should connect bind like a server or connect like a client? both are probably wrong so what does it do that isn't just
# taking some variables??? if nothing, why aren't we using innit????????

# are we inheriting from socket? no way right????? this would have been stated....

with Connection.connect('127.0.0.1', 8000) as connection:
    print(type(connection))
    connection.send_message(b'hello')
