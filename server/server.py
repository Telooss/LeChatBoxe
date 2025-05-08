import socket
import threading
from .handlers import handle_client
from config.config import HOST, PORT
from database.chat_db import init_db

def start_server():
    init_db()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[✅] Chat server running at {HOST}:{PORT}...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"[+] New connection from {address}")
        thread = threading.Thread(target=handle_client, args=(client_socket, address), daemon=True)
        thread.start()

if __name__ == "__main__":
    start_server()
