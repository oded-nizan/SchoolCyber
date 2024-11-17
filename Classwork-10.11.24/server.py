import socket


def main() -> None:
    server_socket: socket = socket.socket()

    server_socket.bind(('0.0.0.0', 8820))
    server_socket.listen()
    print('The server is up and running')

    (client_socket, client_address) = server_socket.accept()
    print('Client connected')

    data: str = client_socket.recv(1024).decode()
    print(f'Client has sent: {data}')

    reply: str = 'Hello'
    client_socket.send(reply.encode())

    data_2: str = client_socket.recv(1024).decode()
    print(f'Client has sent: {data_2}')

    reply: str = 'Roe'
    client_socket.send(reply.encode())

    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()