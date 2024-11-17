import socket


def main() -> None:
    my_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    my_socket.connect(('127.0.0.1', 8820))

    my_socket.send('Hello'.encode())
    data: str = my_socket.recv(1024).decode()
    print(f'The server sent the following data: {data}')

    my_socket.send('Who is your favorite student'.encode())
    data_2: str = my_socket.recv(1024).decode()
    print(f'The server sent the following data: {data_2}')

    my_socket.close()


if __name__ == '__main__':
    main()
