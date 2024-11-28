# Imports
from socket import socket

# Fixed variables
LENGTH_FIELD_SIZE: int = 4
PORT: int = 8820
ACKNOWLEDGMENT: str = 'Ready to receive photo'


def check_cmd(data: str) -> bool:
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\\work\\file.txt is good, but DELETE alone is not
    """
    # Check for functions that should not receive parameters
    if data == 'TAKE_SCREENSHOT' or data == 'EXIT' or data == 'SEND_PHOTO':
        return True
    # Check for DIR function receiving exactly one parameter
    if len(data) >= 3 and data[:3] == 'DIR':
        if data[3] == ' ' and len(data) >= 7 and data.find(' ', 4) == -1:
            return True
    # Check for COPY function receiving exactly two parameters
    if len(data) >= 4 and data[:4] == 'COPY':
        index: int = data.find(' ', 5)
        if data[4] == ' ' and len(data) >= 22 and index != -1 and data.find(' ', index + 1) == -1:
            return True
    # Check for DELETE function receiving exactly one parameter
    if len(data) >= 6 and data[:6] == 'DELETE':
        if data[6] == ' ' and len(data) >= 13 and data.find(' ', 12) == -1:
            return True
    # Check for EXECUTE function receiving exactly one parameter
    if len(data) >= 7 and data[:7] == 'EXECUTE':
        if data[7] == ' ' and len(data) >= 13 and data.find(' ', 12) == -1:
            return True
    # (3)
    # If the tests for each function and a valid protocol meaning valid parameters fail, return False
    return False


def create_msg(data: str) -> bytes:
    """
    Create a valid protocol message, with length field
    """
    # Create the length field of the message based on the protocol of communications and add the data field
    length: str = str(len(data))
    length_full: str = length.zfill(LENGTH_FIELD_SIZE)
    msg: str = length_full + data
    # (4)
    return msg.encode()


def get_msg(my_socket: socket) -> tuple[bool, str]:
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    # Receive the length field of the message based on the protocol of communications, check if length field is
    # valid, return Error if not and receive data message if it is
    msg_length_origin: bytes = my_socket.recv(LENGTH_FIELD_SIZE)
    msg_length: str = msg_length_origin.decode()
    if not msg_length.isdigit():
        return False, 'Error'
    length: int = int(msg_length)
    msg: str = my_socket.recv(length).decode()
    # (5)
    return True, msg
