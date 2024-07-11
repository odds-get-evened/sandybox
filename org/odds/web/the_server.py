import socket
import time
from hashlib import sha256
from threading import Thread

from org.odds.util import crc32

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8888
BUF_LEN = 1024


class ClientHandle:
    def __init__(self, cid: str, sock: socket.socket, addr: tuple):
        self.id = cid
        self.socket = sock
        self.address = addr


class TheServer:
    def __init__(self, host: str, port: int = 8888):
        self.host_spec: tuple = (host, port)
        self.connections: list[ClientHandle] = []

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.serv:
            self.serv.bind(self.host_spec)
            self.serv.listen(5)
            print(f"listening on {self.host_spec[0]}:{self.host_spec[1]}")

            while True:
                # accept client connections
                cli_sock, addr = self.serv.accept()
                print(f"connection from {addr[0]}:{addr[1]}")

                clid = crc32(str(addr[0] + str(addr[1]) + str(time.time())).encode()).decode()

                # start a new thread for each client
                Thread(target=self.handle_client, args=(clid, cli_sock, addr)).start()

    def handle_client(self, cid: str, sock: socket.socket, addr: tuple):
        try:
            self.connections.append(ClientHandle(cid, sock, addr))

            while True:
                # receive and print client messages
                req = sock.recv(BUF_LEN)
                print(f"client: {req.decode()}")

                '''
                process input from clients after this line.
                basically the client has to send commands that
                meet the protocol of the server (e.g. client sends 
                `quit`, and the server will confirm with `DISCONNECT`,
                `DISCONNECT` triggers the client to disconnect
                '''
                res = ""
                if req.decode().__eq__('quit'):
                    res = 'disconnect'.upper()
                    # sock.send('disconnect'.upper().encode())

                if req.decode().startswith('hash'):
                    cmd = req.decode().split(' ')
                    if len(cmd) >= 2:
                        res = 'SHA256'.upper() + " " + sha256(' '.join(cmd[1:]).encode()).hexdigest()

                # convert and send response to client
                sock.send(("server <<: " + res).encode())
        except Exception as e:
            print(f"client {addr[0]}:{addr[1]} handling error {e}")
        finally:
            sock.close()
            print(f"connection to {addr[0]}:{addr[1]} closed")


def the_server():
    server = TheServer('127.0.0.1')


def main():
    the_server()


if __name__ == "__main__":
    main()
