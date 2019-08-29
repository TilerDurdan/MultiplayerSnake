import socketserver
from Class_Library import *
import pickle

"""def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP"""







class EchoTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip()
        print(f"Address : {self.client_address[0]}:{self.client_address[1]}")
        print(f"Data: {data.decode()}")
        if str(data).startswith("Login:"):
            msg = GF.newplayer(data.decode())
        else:
            msg = "Turn taken"

        self.request.sendall(msg.encode())


if __name__ == '__main__':
    with socketserver.TCPServer(('', 8888), EchoTCPHandler) as server:
        GF = GameField(40, 30)
        server.serve_forever()
