import socket
from _thread import *
import pickle
import threading
from multiprocessing import Process, Queue, Lock, Event, current_process
import queue
import pygame
import uuid
import  time


class Chatted(object):
    def __init__(self):
        self.list = []

    def add_msg(self, msg):
        self.list.append(msg)


def threaded_client(conn, chat_s, lock, mainq, event):

    #global chat_server

    conn.send(pickle.dumps(chat_s))
    global chat_server
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(1024))

            if not data:
                print("Disconnected")
                break
            else:
                event.wait()
                lock.acquire()
                try:
                    chat_server.add_msg(data.list[-1])
                    print(f'Trying to add {data.list[-1]} by {current_process().name}')
                finally:
                    lock.release()

                myq.put(data.list[-1])

                mainq.put('Update')
                event.wait()
                #data.add_msg(chat_s.list[-1])
                time.sleep(0.1)
                reply = chat_server

                print("Received: ", data.list)
                print("Sending : ", reply.list)


            print("CHAT \n", chat_server.list)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()
    return chat_s


server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


lock = Lock()
chat_server = Chatted()

event = threading.Event()

myq = queue.Queue()
mainq = queue.Queue()

if __name__ == '__main__':

    currentuser = 0

    while True:
        # вынес отсюда создание event, mainq, myq


        connection, addr = s.accept()
        print("Connected to:", addr)

        newconnection = threading.Thread(target=threaded_client, args=(connection, chat_server, lock, mainq, event))
    #    start_new_thread(threaded_client, (connection, chat_server, ))
        newconnection.start()
        event.set()
        if not mainq.empty():
            mainq.get()

            while not myq.empty():
                taken = myq.get()
                chat_server.add_msg(taken)
                print(taken, ' from myq')
        newconnection.join(1)

        currentuser += 1

        print('from main__ list is ', chat_server.list)
else:
    pass



