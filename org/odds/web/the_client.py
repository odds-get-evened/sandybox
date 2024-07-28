import socket

from org.odds.web.the_server import DEFAULT_HOST, DEFAULT_PORT, BUF_LEN


class TheClient:
    def __init__(self, host: str, port: int):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            self.sock.connect((host, port))

            while True:
                # input message and send to server
                req = input(">> ")
                self.sock.send(req.strip().encode()[:BUF_LEN])

                # receive message from server
                res = self.sock.recv(1024)
                print(f"{res.decode()}")

                if res.decode().__eq__('DISCONNECT'):
                    print("disconnected from server")
                    break

                if res.decode().startswith('SHA256'):
                    continue


def the_client(host: str, port: int):
    client = TheClient(host, port)


def main():
    the_client(DEFAULT_HOST, DEFAULT_PORT)


if __name__ == "__main__":
    main()
