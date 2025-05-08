import uuid
from config.config import ADMIN_USERNAME
from .utils import broadcast, shutdown_server

def handle_command(msg, client_socket, usernames, clients, fernet_keys, access_password):
    cmd = msg.strip().split()
    username = usernames.get(client_socket, "")

    if cmd[0].lower() == "/users":
        connected = ", ".join(usernames.values())
        client_socket.send(
            fernet_keys[client_socket].encrypt(f"Connected users: {connected}".encode())
        )

    elif cmd[0].lower() == "/regen" and username == ADMIN_USERNAME:
        access_password = str(uuid.uuid4())
        broadcast(
            f"🔁 New access password: {access_password}",
            None,
            fernet_keys,
            clients
        )

    elif cmd[0].lower() == "/stop" and username == ADMIN_USERNAME:
        client_socket.send(
            fernet_keys[client_socket].encrypt(b"Server: Shutdown initiated.")
        )
        shutdown_server(client_socket, clients)

    elif cmd[0].lower() == "/kick" and username == ADMIN_USERNAME:
        if len(cmd) < 2:
            client_socket.send(
                fernet_keys[client_socket].encrypt(b"Usage: /kick <username>")
            )
            return

        target_name = cmd[1].strip().lower()

        target_socket = next(
            (sock for sock, uname in usernames.items() if uname.lower() == target_name),
            None
        )

        if target_socket:
            target_socket.send(
                fernet_keys[target_socket].encrypt(b"[KICK] You were kicked by admin.")
            )
            target_socket.close()
            if target_socket in clients:
                clients.remove(target_socket)
            usernames.pop(target_socket, None)
            fernet_keys.pop(target_socket, None)
            broadcast(
                f"Server: {cmd[1]} was kicked by the admin.",
                None,
                fernet_keys,
                clients
            )
        else:
            client_socket.send(
                fernet_keys[client_socket].encrypt(b"User not found.")
            )

    else:
        client_socket.send(
            fernet_keys[client_socket].encrypt(b"Unknown or unauthorized command.")
        )
