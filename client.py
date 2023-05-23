import socket
import threading

# Client configuration
HOST = '127.0.0.1'  # Localhost
PORT = 55555

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Prompt the user for a nickname
nickname = input('Enter your nickname: ')

# Send the nickname to the server
client_socket.send(nickname.encode('ascii'))


# Handle receiving messages from the server
def receive():
    while True:
        try:
            # Receive messages from the server
            message = client_socket.recv(1024).decode('ascii')
            if message == 'NICK':
                client_socket.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Handle disconnections
            print('An error occurred while receiving messages.')
            client_socket.close()
            break


# Handle sending messages to the server
def send():
    while True:
        message = input()
        client_socket.send(message.encode('ascii'))


# Start the receiving and sending threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
