import socket
from threading import Thread

MY_HOST = '127.0.0.1'
MY_PORT = 8888

CLIENT_STORE = []


def handle_client(sock, addr):
    try:
        # add socket to list of clients
        CLIENT_STORE.append(sock)
        print(f"# of clients: {len(CLIENT_STORE)}")

        while True:
            # receive and handle client messages
            req: str = sock.recv(1024).decode()

            print(f"client said: {req}")

            if req.__eq__('close'):
                sock.send('closed'.encode())
                break

            if req.__eq__('knock'):
                sock.send('you should get a token at this point.'.encode())



            # send an empty response to get back to message prompt and let client know nothing happened
            # sock.send(" ".encode())
    except Exception as e:
        print(f"error when handling client: {e}")
    finally:
        # remove from store before disconnect
        [CLIENT_STORE.pop(i) for i, c in enumerate(CLIENT_STORE) if c.getpeername() == sock.getpeername()]

        sock.close()
        print(f"connection to client {addr[0]}:{addr[1]} closed")


def the_server():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # bind the socket to host/port
        serv.bind((MY_HOST, MY_PORT))
        # listen for incoming connections
        serv.listen(3)
        print(f"listening on {MY_HOST}:{MY_PORT}")

        while True:
            # accept client connection
            cli_sock, addr = serv.accept()
            print(f"accepted connection from {addr[0]}:{addr[1]}")

            # start a new thread to handle the client
            t = Thread(target=handle_client, args=(cli_sock, addr))
            t.start()
    except Exception as e:
        print(f"error: {e}")
    finally:
        serv.close()


def main():
    the_server()


if __name__ == "__main__":
    main()
