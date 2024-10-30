import socket
from threading import Thread

QUEUE_SIZE = 10
BUFFER_SIZE = 1024
IP = '0.0.0.0'
PORT = 8080
ENCODED = 'dc36fecdcd65b2b2f0e12567f26167f4'
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
        LATEST_R = erange
        client_socket.send(drange.encode())
        for i in range(0, c_count + 1):
            response = ''
            while '#' not in response:
                response_part = client_socket.recv(BUFFER_SIZE).decode()
                response += response_part
            response = response[:len(response) - 1]
            if response == 'Y':
                decoded_message = ''
                while '#' not in decoded_message:
                    decoded_part = client_socket.recv(BUFFER_SIZE).decode()
                    decoded_message += decoded_part
                print('Original message found - ' + decoded_message[:len(decoded_message) - 1])
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
