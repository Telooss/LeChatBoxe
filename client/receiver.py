def receive_messages(client_socket, fernet, username):
    while True:
        try:
            encrypted = client_socket.recv(2048)
            if encrypted:
                message = fernet.decrypt(encrypted).decode()
                if message.startswith("[KICK]"):
                    print(f"\n{message.replace('[KICK] ', '')}")
                    print("Disconnected by admin.")
                    client_socket.close()
                    break
                elif message.startswith("Server shutting down."):
                    print("\nServer shutting down.")
                    client_socket.close()
                    break
                print(f"\n{message}")
                print(f"{username}: ", end="", flush=True)
            else:
                break
        except:
            break
