import socket

from org.odds.web.the_server import MY_HOST, MY_PORT


def run_client():
    # create a socket
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    cli.connect((MY_HOST, MY_PORT))

    try:
        # get input message from user and send to the server
        msg = input("enter message: ")

        while True:
            cli.send(msg.encode()[:1024])

            # receive message from server
            res = cli.recv(1024)
            res = res.decode()

            '''
            if server sent us "closed" in the payload, we break out of
            this loop and close the socket
            '''
            if res.__eq__('closed'):
                break

            print(f"{res}")

            # get input message from user and send to the server
            msg = input("enter message: ")
    except Exception as e:
        print(f"error: {e}")
    finally:
        # close the client socket (connection to the server)
        cli.close()
        print(f"connection closed")


def main():
    run_client()


if __name__ == "__main__":
    main()
