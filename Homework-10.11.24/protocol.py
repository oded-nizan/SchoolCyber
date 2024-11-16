LENGTH_FIELD_SIZE: int = 2
PORT: int = 8820


def check_cmd(data: str) -> bool:
    """Check if the command is defined in the protocol (e.g. RAND, NAME, TIME, EXIT)"""
    if data == 'TIME' or data == 'NAME' or data == 'RAND' or data == 'EXIT':
        return True
    return False


def create_msg(data: str) -> str:
    """Create a valid protocol message, with length field"""
    length: str = str(len(data))
    length_full: str = length.zfill(LENGTH_FIELD_SIZE)
    return length_full + data


def get_msg(client_socket) -> (bool, str):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    data_length: str = client_socket.recv(LENGTH_FIELD_SIZE).decode()
    if not data_length.isdigit():
        return False, 'Error'
    length: int = int(data_length)
    data: str = client_socket.recv(length).decode()
    return True, data
