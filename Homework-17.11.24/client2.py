import socket
import protocol2

IP: str = '127.0.0.1'
SAVED_PHOTO_LOCATION: str = r'C:\Users\Oded\Pictures\Screenshots\screenshot.jpg'  # The path + filename where the


# copy of the screenshot at the client should be saved


def handle_server_response(my_socket: socket, cmd: str) -> None:
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note-special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO
    valid_protocol, server_response = protocol2.get_msg(my_socket)
    if not valid_protocol:
        print('Invalid protocol from server response')
        return None
    if cmd != 'SEND_PHOTO':
        print(f'Server has responded with:\n{server_response}')
    # (10) treat SEND_PHOTO
    else:
        send_acknowledgment(my_socket)
        receive_photo(my_socket, int(server_response))


def send_acknowledgment(my_socket: socket) -> None:
    acknowledgment: str = protocol2.ACKNOWLEDGMENT
    msg: bytes = protocol2.create_msg(acknowledgment)
    my_socket.send(msg)


def receive_photo(my_socket: socket, file_size: int) -> None:
    with open(SAVED_PHOTO_LOCATION, 'wb') as file:
        bytes_received: int = 0
        while bytes_received < file_size:
            chunk: bytes = my_socket.recv(1024)
            if not chunk:  # an empty byte string in python is considered falsely
                break
            file.write(chunk)
            bytes_received += len(chunk)


def main() -> None:
    # open socket with the server
    my_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, protocol2.PORT))
    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd: str = input("Please enter command:\n")
        cmd = fr'{cmd}'
        if protocol2.check_cmd(cmd):
            packet: bytes = protocol2.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    # close socket
    print("Closing connection")
    my_socket.close()


if __name__ == '__main__':
    main()
