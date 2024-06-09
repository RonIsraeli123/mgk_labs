from src.utils.socket_handle import broadcast
from src.utils.openai_handle import process_with_openai


# Handle client messages
def handle_client_message(message: str, clients: list, sender):
    try:
        # End socket
        if message.lower() == "quit":
            sender.send("Goodbye!".encode())
            sender.close()
            clients.remove(sender)
        # Send a message to specific user
        elif message.startswith("@"):
            ip_name, message_body = message.split(" ", 1)
            ip_name = ip_name[1:]  # Remove "@" prefix
            # Extract the specific user socket
            target_client = next((client for client in clients if client.getpeername()[0] == ip_name), None)
            if target_client:
                target_client[0].send(f"[Direct Message] FROM [{sender.getpeername()[0]}] {message_body}".encode())
            else:
                sender.send(f"{ip_name} not exist!!".encode())
        # Send a broadcast to every user
        elif message.lower().startswith("@broadcast"):
            # Broadcast message to all clients
            broadcast_message = message[11:]  # Remove "@broadcast" prefix
            broadcast(broadcast_message, clients, sender)
        else:
            try:
                # Process message using OpenAI's model
                response = process_with_openai(message)
                message_size = '{:04d}'.format(len(response))
                # Create a new message that contain a 'header' with the msg size
                message_with_size = message_size + response
                sender.send(message_with_size.encode())
            except:
                response = "open api fail to process your message"
                sender.send(response.encode())
    except:
        sender.send("server error".encode())
