import select

from src.config.config import HOST, PORT
from src.utils.soket_handle import create_server_socket, accept_new_connection
from src.utils.client_handle import handle_client_message


# Activate server
def main():
    server_socket = create_server_socket(HOST, PORT)
    # can storage in db
    clients = []

    while True:
        # Handle multiple messages in some async way
        readable, _, _ = select.select([server_socket] + clients, [], [])

        for sock in readable:
            if sock == server_socket:
                accept_new_connection(server_socket, clients)
            else:
                try:
                    # Receive the fixed-length header
                    header: str = sock.recv(4).decode()  # Assuming the header length is 4 bytes

                    if header:
                        message = sock.recv(int(header)).decode()
                        handle_client_message(message, clients, sock)
                    else:
                        print(f"Client {sock.getpeername()} disconnected.")
                        sock.close()
                        clients.remove(sock)
                except ConnectionResetError as e:
                    print("Connection reset by peer:", e)
                    sock.close()
                    clients.remove(sock)


if __name__ == "__main__":
    main()
