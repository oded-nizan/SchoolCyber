import socket
import protocol2
import glob
import os
import subprocess
import shutil
import pyautogui

IP: str = '192.168.68.75'
PHOTO_PATH: str = r'C:\Users\Oded\Pictures\Screenshots\screenshot.jpg'  # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd: str) -> tuple[bool, str, list[str]]:
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first
    valid_cmd_protocol: bool = protocol2.check_cmd(cmd)
    if not valid_cmd_protocol:
        return False, cmd, []
    index: int = cmd.find(' ')
    stripped_cmd: str = cmd[:index]
    params: list[str] = []
    next_index: int
    while index < len(cmd) - 1:
        end_loop: bool = False
        next_index = cmd[index + 1:].find(' ')
        if next_index == -1:
            end_loop = True
            param: str = cmd[index + 1:]
        else:
            param: str = cmd[index + 1:next_index]
        params.append(param)
        index = next_index
        if end_loop:
            break
    # Then make sure the params are valid
    for param in params:
        if not (stripped_cmd == 'DIR' and os.path.isdir(param)) or (stripped_cmd != 'DIR' and os.path.isfile(param)):
            return False, stripped_cmd, params
    # (6)

    return True, stripped_cmd, params


def handle_client_request(command: str, params: list[str]) -> str:
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    response: str
    match command:
        case 'DIR':
            response = command_dir(params[0])
        case 'DELETE':
            response = command_delete(params[0])
        case 'COPY':
            response = command_copy(params[0], params[1])
        case 'EXECUTE':
            response = command_execute(params[0])
        case 'TAKE_SCREENSHOT':
            response = command_take_screenshot()
        case 'SEND_PHOTO':
            response = command_send_photo()
        case _:
            response = f'Something went wrong while attempting to execute command: {command}'
    # (7)
    return response


def command_dir(param: str) -> str:
    path: str = fr'{param}\*.*'
    dir_list: list[str] = glob.glob(path)
    return ''.join(x + '\n' for x in dir_list)


def command_delete(param: str) -> str:
    path: str = fr'{param}'
    os.remove(path)
    return f'Something went wrong while attempting to delete file: {param}' if os.path.isfile(path) else 'OK'


def command_copy(param1: str, param2: str) -> str:
    path1: str = fr'{param1}'
    path2: str = fr'{param2}'
    shutil.copy(path1, path2)
    return 'OK' if os.path.isfile(
        path2) else f'Something went wrong while attempting to coppy file: {param1} to file: {param2}'


def command_execute(param: str) -> str:
    path: str = fr'{param}'
    subprocess.call(path)
    return 'OK'


def command_take_screenshot() -> str:
    image = pyautogui.screenshot()
    image.save(PHOTO_PATH)
    return 'OK' if os.path.isfile(
        PHOTO_PATH) else f'Something went wrong while attempting to take a screenshot and save it to: {PHOTO_PATH}'


def command_send_photo() -> str:
    return ''


def main():
    # open socket with client
    server_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol2.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    # (1)

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol2.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                # (6)
                # prepare a response using "handle_client_request"
                response = handle_client_request(cmd, params)
                # add length field using "create_msg"
                msg: bytes = protocol2.create_msg(response)
                # send to client
                client_socket.send(msg)
                if command == 'SEND_FILE':
                    # Send the data itself to the client
                    pass
                    # (9)

                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response: str = 'Bad command or parameters'
                # add length field using "create_msg"
                msg: bytes = protocol2.create_msg(response)
                # send to client
                client_socket.send(msg)

        else:
            # prepare proper error to client
            response: str = 'Packet not according to protocol'
            # add length field using "create_msg"
            msg: bytes = protocol2.create_msg(response)
            # send to client
            client_socket.send(msg)

            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
