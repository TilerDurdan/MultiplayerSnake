import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
        Port = s.getsockname()[1]
    except:
        IP = '127.0.0.1'
        Port = 5555
    finally:
        s.close()
    return [IP, Port]

