import socket
import threading

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1234))
server.listen()


clients = []
usernames = {}

# Broadcast messages to all clients
def broadcast(message, sender_client=None):
    for client in clients:
        # if client != sender_client:
        try:
            client.send(message)
        except:
            client.close()
            remove_client(client)

# Handle messages from clients
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, client)
        except:
            remove_client(client)
            break

def remove_client(client):
    if client in clients:
        clients.remove(client)
    if client in usernames:
        username = usernames.pop(client)
        broadcast(f'{username} has left the chat!'.encode('utf-8'))

# Receive connections from clients
def receive_connections():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('USERNAME'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames[client] = username
        clients.append(client)

        print(f'Username of the client is {username}')
        broadcast(f'{username} has joined the chat!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print('Server is listening...')
receive_connections()