import socket

def check_port_exists(port, host="127.0.0.1"):
    try:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.close()
        return False
    except socket.error:
        return True