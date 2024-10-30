import socket
from threading import Thread

QUEUE_SIZE = 10
BUFFER_SIZE = 1024
IP = '0.0.0.0'
PORT = 8080
ENCODED = '393a02a8b46c706c42e3aa9795cc73ca'
LATEST_R = 0
CRANGE = 5000

found = False


def handle_connection(client_socket, client_address):
    """
    Handle_connection function:
    handles each client's connection in a separate thread.
    contains the logic for the server/client communication protocol, according to client's choice.
    Infinite loop until client closes program.
    """
    global ENCODED
    global LATEST_R
    global CRANGE
    global found
    try:
        client_socket.send(ENCODED.encode())
        c_count = int(client_socket.recv(BUFFER_SIZE).decode())
        erange = LATEST_R + (CRANGE * c_count)
        drange = str(LATEST_R + 1) + '-' + str(erange)
        client_socket.send(drange.encode())
        for i in range(0, c_count + 1):
            response = client_socket.recv(BUFFER_SIZE).decode()
            response = response[:len(response) - 1]
            if response == 'Y':
                decoded_message = client_socket.recv(BUFFER_SIZE).decode()
                print('Original message found - ' + decoded_message)
                found = True
    except (socket.error, ValueError) as err:
        print('Received exception - ' + str(err))
    finally:
        client_socket.close()


def main():
    """
    starts the server, starting thread for each client
    on an infinite loop.
    """
    global found
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)
        while not found:
            client_socket, client_address = server_socket.accept()
            thread = Thread(target=handle_connection, args=(client_socket, client_address))
            thread.start()
    except socket.error as err:
        print('Received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
