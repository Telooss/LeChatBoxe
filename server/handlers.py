from .utils import broadcast, shutdown_server
from .commands import handle_command
from database.chat_db import login_user, register_user, save_message
from cryptography.fernet import Fernet
import uuid
from config.config import ADMIN_USERNAME

clients = []
usernames = {}
fernet_keys = {}
access_password = str(uuid.uuid4())

print(f"[🔐] Server access password: {access_password}")

def handle_client(client_socket, address):
    global access_password

    if client_socket not in clients:
        clients.append(client_socket)

    try:
        access_attempt = client_socket.recv(1024).decode().strip()
        if access_attempt != access_password:
            client_socket.send(b"Access denied. Invalid server password.\n")
            client_socket.close()
            return

        session_key = Fernet.generate_key()
        fernet = Fernet(session_key)
        fernet_keys[client_socket] = fernet
        client_socket.send(session_key)

        client_socket.send(fernet.encrypt(
            b"Welcome to the chat server!\n1 - Login\n2 - Register\nEnter your choice: "))
        choice = fernet.decrypt(client_socket.recv(2048)).decode()

        client_socket.send(fernet.encrypt(b"Enter your username: "))
        username = fernet.decrypt(client_socket.recv(2048)).decode()

        client_socket.send(fernet.encrypt(b"Enter your password: "))
        password = fernet.decrypt(client_socket.recv(2048)).decode()

        if choice == "2":
            if register_user(username, password):
                client_socket.send(fernet.encrypt(b"Registration successful.\n"))
            else:
                client_socket.send(fernet.encrypt(b"Username already exists.\n"))
                client_socket.close()
                return
        elif choice == "1":
            if login_user(username, password):
                client_socket.send(fernet.encrypt(b"Login successful.\n"))
            else:
                client_socket.send(fernet.encrypt(b"Invalid credentials.\n"))
                client_socket.close()
                return
        else:
            client_socket.send(fernet.encrypt(b"Invalid choice.\n"))
            client_socket.close()
            return

        usernames[client_socket] = username
        broadcast(f"Server: {username} has joined the chat.", client_socket, fernet_keys, clients)

        while True:
            encrypted_msg = client_socket.recv(2048)
            if not encrypted_msg:
                break

            message = fernet.decrypt(encrypted_msg).decode().strip()

            if message.startswith("/"):
                handle_command(message, client_socket, usernames, clients, fernet_keys, access_password)
                continue

            if message.lower() == "exit":
                break

            save_message(username, message)
            broadcast(f"[{username}] {message}", client_socket, fernet_keys, clients)

    except Exception as e:
        print(f"[-] Exception {address}: {e}")

    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        usernames.pop(client_socket, None)
        fernet_keys.pop(client_socket, None)
        client_socket.close()
        broadcast(f"Server: {username} has left the chat.", client_socket, fernet_keys, clients)
