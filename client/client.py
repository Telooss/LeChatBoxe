import socket
import threading
from cryptography.fernet import Fernet
from .receiver import receive_messages
from config.config import HOST, PORT

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Connexion sécurisée au serveur
    access_password = input("Enter server access password: ")
    client_socket.send(access_password.encode())

    # Réception clé Fernet
    fernet_key = client_socket.recv(1024)
    fernet = Fernet(fernet_key)

    # Authentification (login/register)
    encrypted = client_socket.recv(1024)
    print(fernet.decrypt(encrypted).decode(), end="")
    choice = input()
    client_socket.send(fernet.encrypt(choice.encode()))

    encrypted = client_socket.recv(1024)
    print(fernet.decrypt(encrypted).decode(), end="")
    username = input()
    client_socket.send(fernet.encrypt(username.encode()))

    encrypted = client_socket.recv(1024)
    print(fernet.decrypt(encrypted).decode(), end="")
    password = input()
    client_socket.send(fernet.encrypt(password.encode()))

    encrypted = client_socket.recv(1024)
    response = fernet.decrypt(encrypted).decode()
    print(response)
    if "successful" not in response:
        client_socket.close()
        return

    threading.Thread(target=receive_messages, args=(client_socket, fernet, username), daemon=True).start()

    while True:
        message = input(f"{username}: ")
        client_socket.send(fernet.encrypt(message.encode()))
        if message.lower() == "exit":
            break

    client_socket.close()

if __name__ == "__main__":
    main()
