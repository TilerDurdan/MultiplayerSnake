import socket
import pickle
import pygame
import Client


class Chatted(object):
    def __init__(self):
        self.list = []

    def add_msg(self, msg):
        self.list.append(msg)


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(1024))
        except socket.error as e:
            print("Houston! We have problem ", e)


def main():
    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        chat.add_msg(str(input()))
        p2 = n.send(chat)

        print("send ", chat.list)
        print("Recieved ", p2.list)


chat = Chatted()
main()
