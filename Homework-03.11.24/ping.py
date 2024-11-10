import platform  # For getting the operating system name
import subprocess  # For executing a shell command
import sys


def ping(host) -> bool:
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python ping.py <hostname>')
        sys.exit(1)
    else:
        hostname: str = sys.argv[1]
        result: bool = ping(hostname)
        if result:
            print(f'{hostname} is working well')
        else:
            print(f'{hostname} has not responded')


if __name__ == '__main__':
    main()
    sys.exit(0)
