import socket


# Create a socket
def create_server_socket(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    return server_socket


# Accept new connection
def accept_new_connection(server_socket, clients):
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f"New connection from {client_address}")


# Broadcast message to all clients except the sender
def broadcast(message, clients, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)
