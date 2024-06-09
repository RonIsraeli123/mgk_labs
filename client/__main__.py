import tkinter as tk
import socket
import threading

from src.config import HOST, PORT


class ClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chat Client")

        # Text view
        self.message_listbox = tk.Listbox(master, width=50, height=20)
        self.message_listbox.pack(padx=10, pady=10)

        # Input
        self.entry = tk.Entry(master, width=40)
        self.entry.pack(padx=10, pady=5)

        # Button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        # Socket connection
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

        # Receive in a different thread
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self):
        message = self.entry.get()
        if message:
            # Max 4 digits ->  1 - 9999
            message_size = '{:04d}'.format(len(message))
            # create a new message that contain a 'header' with the msg size
            message_with_size = message_size + message
            self.client_socket.send(message_with_size.encode())
            self.entry.delete(0, 'end')

    def receive_messages(self):
        while True:
            try:
                header: str = self.client_socket.recv(4).decode()
                message = self.client_socket.recv(int(header)).decode()
                self.message_listbox.insert('end', message)
                self.master.update_idletasks()  # Update the GUI immediately
            except Exception as e:
                print("Error receiving message:", e)
                break


def main():
    root = tk.Tk()
    ClientGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
