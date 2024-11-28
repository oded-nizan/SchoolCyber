# Imports
import socket
from communications_protocol import PORT, ACKNOWLEDGMENT, check_cmd, get_msg, create_msg
from glob import glob
from os.path import isfile, isdir, getsize
from os import remove
from subprocess import call
from shutil import copy
from pyautogui import screenshot

# Fixed variables
IP: str = '0.0.0.0'
PHOTO_PATH: str = r'C:\Users\Oded\Pictures\Screenshots\screenshot.png'  # The path + filename where the screenshot at
# the server should be saved


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
    valid_cmd_protocol: bool = check_cmd(cmd)
    index: int = cmd.find(' ')  # Get the index of the first appearance of the space character
    # If there are no spaces in the command that means there are no parameters therefore we'll check if there should
    # be any
    if index == -1:
        # All commands that should not have any parameters
        no_params: bool = cmd == 'TAKE_SCREENSHOT' or cmd == 'EXIT' or cmd == 'SEND_PHOTO'
        if not valid_cmd_protocol or not no_params:
            return False, cmd, []
        if no_params:
            return True, cmd, []
    params: list[str] = []  # Initialize the parameter's list
    stripped_cmd: str = cmd[:index]  # Get the command word itself out of the command text
    # Check if the command is associated with needing exactly one parameter
    if stripped_cmd == 'DIR' or stripped_cmd == 'EXECUTE' or stripped_cmd == 'DELETE':
        params.append(cmd[index + 1:])
        # Check the validity of the parameters for each command
        if (stripped_cmd == 'DIR' and isdir(params[0])) or stripped_cmd == 'EXECUTE' or isfile(
                params[0]):
            return True, stripped_cmd, params
        else:
            return False, stripped_cmd, params
    # In case the program hasn't exited the command is COPY, which requires exactly two parameters
    second_index: int = cmd.find(' ', index + 1)  # Get the index of the second appearance of the space character
    if second_index == -1:
        return False, stripped_cmd, params  # If there isn't another space there are not two parameters
    # Note: In the protocol function we check for the exact number of parameters but assuming a certain level of
    # black box we will make more checks here
    # Append the parameters to the list
    params.append(cmd[index + 1: second_index])
    params.append(cmd[second_index + 1:])
    # Check the validity of the parameters
    if not isfile(params[0]) or not isfile(params[0]):
        print(params)
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
    # Using a match-case structure with a separate function returning the response for each command
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
        case 'EXIT':
            response = 'Exiting communication...'
        case _:
            response = f'Something went wrong while attempting to execute command: {command}'
    # (7)
    return response


def command_dir(param: str) -> str:
    # Get the raw path for the directory and then get the list required and return it
    path: str = fr'{param}\*.*'
    dir_list: list[str] = glob(path)
    return ''.join(x + '\n' for x in dir_list)


def command_delete(param: str) -> str:
    # Get the raw path for the file and remove it, then return a response based on the remaining existence of the file
    path: str = fr'{param}'
    remove(path)
    return f'Something went wrong while attempting to delete file: {param}' if isfile(path) else 'OK'


def command_copy(param1: str, param2: str) -> str:
    # Get the raw path for the files, copy the first to the second and return a response based on the existence of
    # the second file
    path1: str = fr'{param1}'
    path2: str = fr'{param2}'
    copy(path1, path2)
    return 'OK' if isfile(
        path2) else f'Something went wrong while attempting to copy file: {param1} to file: {param2}'


def command_execute(param: str) -> str:
    # Get the raw path and attempt to call the program with try-catch. If we fail, return appropriate response
    path: str = fr'{param}'
    try:
        call(path)
    except Exception as e:
        return f'Something went wrong while attempting to execute: {path}\nException is {e}'
    return 'OK'


def command_take_screenshot() -> str:
    # Take a screenshot, save it and return response based on its existence as a file
    image = screenshot()
    image.save(PHOTO_PATH)
    return 'OK' if isfile(
        PHOTO_PATH) else f'Something went wrong while attempting to take a screenshot and save it to: {PHOTO_PATH}'


def command_send_photo() -> str:
    # Get the length of the file and return it for the initial server response
    photo_length: int = getsize(PHOTO_PATH)
    return str(photo_length)


def send_photo(client_socket: socket) -> None:
    # Send the full photo after receiving acknowledgment
    # receive acknowledgment
    valid, msg = get_msg(client_socket)
    if valid and msg == ACKNOWLEDGMENT:
        # Send the data itself to the client
        with open(PHOTO_PATH, 'rb') as f:
            client_socket.sendfile(f)
    else:
        client_socket.send(create_msg('Something went wrong'))


def main():
    # open socket with client
    server_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    connection_msg: bytes = create_msg('Server is connected')
    client_socket.send(connection_msg)

    # (1)

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                # (6)
                # prepare a response using "handle_client_request"
                response: str = handle_client_request(command, params)
                # add length field using "create_msg"
                msg: bytes = create_msg(response)
                # send to client
                client_socket.send(msg)
                if command == 'SEND_PHOTO':
                    send_photo(client_socket)
                    # (9)

                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response: str = 'Bad command or parameters'
                # add length field using "create_msg"
                msg: bytes = create_msg(response)
                # send to client
                client_socket.send(msg)

        else:
            # prepare proper error to client
            response: str = 'Packet not according to protocol'
            # add length field using "create_msg"
            msg: bytes = create_msg(response)
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
