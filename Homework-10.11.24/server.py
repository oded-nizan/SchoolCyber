import socket
import protocol
import datetime
import random


def create_server_rsp(cmd: str) -> str:
    """Based on the command, create a proper response"""
    response: str
    match cmd:
        case 'TIME':
            current_time = datetime.datetime.now()
            response = current_time.strftime("%a %b %d %H:%M:%S %Y")
        case 'NAME':
            response = 'Oded'
        case 'RAND':
            response = str(random.randint(1, 10))
        case _:
            response = 'Invalid command'
    return response


def main() -> None:
    server_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            print(f"Received {cmd}")
            # 2. Check if the command is valid
            valid: bool = protocol.check_cmd(cmd)
            if valid:
                if cmd == 'EXIT':
                    break
                # 3. If valid command - create response
                response: str = create_server_rsp(cmd)
            else:
                response: str = "Invalid command"
        else:
            response: str = "Invalid protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        # Handle EXIT command, no need to respond to the client
        if cmd == 'Exit':
            break
        # Send response to the client
        server_response: str = protocol.create_msg(response)
        client_socket.send(server_response.encode())

    print("Closing\n")
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
