def broadcast(message, sender_socket, fernet_keys, clients):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(fernet_keys[client].encrypt(message.encode()))
            except:
                client.close()
                clients.remove(client)

def shutdown_server(server_socket, clients):
    print("[⛔] Server shutting down...")
    for client in clients:
        try:
            client.send(b"Server shutting down.")
            client.close()
        except:
            pass
    server_socket.close()
