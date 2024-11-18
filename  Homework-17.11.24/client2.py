import socket
import protocol2

IP: str = '192.168.68.75'
SAVED_PHOTO_LOCATION: str = r'C:\Users\Oded\Pictures\Screenshots\screenshot.jpg'  # The path + filename where the
# copy of the screenshot at the client should be saved


def handle_server_response(my_socket: socket, cmd: str) -> None:
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note-special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO

    # (10) treat SEND_PHOTO


def main() -> None:
    # open socket with the server
    my_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol2.PORT))
    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd: str = input("Please enter command:\n")
        if protocol_solution.check_cmd(cmd):
            packet: bytes = protocol_solution.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()
