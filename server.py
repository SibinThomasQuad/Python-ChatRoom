import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 55555

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# List to hold client connections
clients = []
nicknames = []


# Broadcast messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handle individual client connections
def handle(client):
    while True:
        try:
            # Broadcast received messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Handle client disconnections
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            break


# Accept client connections and start handling them
def receive():
    while True:
        client, address = server_socket.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        # Start handling the client in a separate thread
        client_thread = threading.Thread(target=handle, args=(client,))
        client_thread.start()


print('Server running...')
receive()
