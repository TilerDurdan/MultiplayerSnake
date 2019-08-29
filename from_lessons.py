import socketserver


# переопределение метода из базового класса
class EchoTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip()
        print(f"Address : {self.client_address[0]} Port: {self.client_address[1]}")
        print(f"Data: {data.decode()}")
        data1 = data.decode()[::-1]
        self.request.sendall(data1.encode())


if __name__ == '__main__':
    with socketserver.TCPServer(('', 8888), EchoTCPHandler) as server:
        server.serve_forever()

# Client
"""
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('',8888))

sock.send(b'Text message')
result = sock.recv(1024)
print('Response: ', result)
sock.close()
"""
