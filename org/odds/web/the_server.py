import socket
import time
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from threading import Thread

from pgpy import PGPUID, PGPKey
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, CompressionAlgorithm, SymmetricKeyAlgorithm

from org.odds.util import crc32

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8888
BUF_LEN = 1024


class ClientHandle:
    def __init__(self, cid: str, sock: socket.socket, addr: tuple):
        self.id = cid
        self.socket = sock
        self.address = addr


class PGPStuff:
    KEY_USAGE = {KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage}
    HASH_FLAGS = [HashAlgorithm.SHA256, HashAlgorithm.SHA512]
    CIPHER_FLAGS = [SymmetricKeyAlgorithm.AES256]
    COMPRESSION_FLAGS = [
        CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2,
        CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed
    ]

    @staticmethod
    def gen_key(id, email="", comment=""):
        key = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
        uid = PGPUID.new(id, email=email, comment=comment)
        key.add_uid(
            uid, usage=PGPStuff.KEY_USAGE,
            hashes=PGPStuff.HASH_FLAGS,
            ciphers=PGPStuff.CIPHER_FLAGS,
            compression=PGPStuff.COMPRESSION_FLAGS
        )

        return key


class TheServer:
    def __init__(self, host: str, port: int = 8888):
        self.host_spec: tuple = (host, port)
        self.connections: list[ClientHandle] = []

        self.executor = ThreadPoolExecutor(max_workers=1)

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
            # self.connections.append(ClientHandle(cid, sock, addr))

            while True:
                # receive and print client messages
                req = sock.recv(BUF_LEN)
                print(f"client: {req.decode()}\n")

                '''
                process input from clients after this line.
                basically the client has to send commands that
                meet the protocol of the server (e.g. client sends 
                `quit`, and the server will confirm with `DISCONNECT`,
                `DISCONNECT` triggers the client to disconnect
                '''
                res = "<< "
                if req.decode().__eq__('quit'):
                    res = 'disconnect'.upper()
                    # sock.send('disconnect'.upper().encode())

                if req.decode().startswith('hash'):
                    cmd = req.decode().split(' ')
                    if len(cmd) >= 2:
                        res = 'sha256'.upper() + " " + sha256(' '.join(cmd[1:]).encode()).hexdigest()
                    else:
                        res = 'noop'.upper()

                if req.decode().startswith('gen'):
                    cmd = req.decode().split(' ')
                    if len(cmd) >= 4:
                        id = cmd[1].strip()
                        email = cmd[2].strip()
                        comment = ' '.join(cmd[3:]).strip()
                        # generate keys
                        futr = self.executor.submit(PGPStuff.gen_key, id, email=email, comment=comment)
                        key: PGPKey = futr.result()
                        res = f'key {' '.join(key.fingerprint[i: i + 4] for i in range(0, len(key.fingerprint), 4))}'.upper()

                # convert and send response to client
                sock.send(res.encode())
        except Exception as e:
            # print(f"client {addr[0]}:{addr[1]} handling error {e}")
            sock.close()
        finally:
            print(f"connection to {addr[0]}:{addr[1]} closed")
            sock.close()


def the_server():
    server = TheServer('127.0.0.1')


def main():
    the_server()


if __name__ == "__main__":
    main()
