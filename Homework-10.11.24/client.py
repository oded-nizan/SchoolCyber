import socket
import protocol


def main() -> None:
    my_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input: str = input("Enter command\n")
        # Check if user entered a valid command as defined in protocol
        valid_cmd: bool = protocol.check_cmd(user_input)
        # If the command is valid:
        if valid_cmd:
            # 1. Add length field
            cmd_length: str = str(len(user_input))
            full_cmd_length: str = cmd_length.zfill(protocol.LENGTH_FIELD_SIZE)
            user_cmd: str = full_cmd_length + user_input
            # 2. Send it to the server
            my_socket.send(user_cmd.encode())
            # 3. If command is EXIT, break from while loop
            if user_input == 'EXIT':
                break
            # 4. Get server's response
            response_length: int = int(my_socket.recv(protocol.LENGTH_FIELD_SIZE).decode())
            server_response: str = my_socket.recv(response_length).decode()
            # 5. If server's response is valid, print it
            if len(server_response) > 0:
                print(server_response)
            else:
                print("Response not valid\n")
        else:
            print("Not a valid command")

    print("Closing\n")
    my_socket.close()


if __name__ == "__main__":
    main()
