import socket
import threading
import socket
from _thread import *
import pickle
import threading
from multiprocessing import Process, Queue, Lock, Event, current_process
import queue
import time
import Multisnake_Gamefield


def threaded_client(conn, maing, curplayer, lock, mainq, event):

    global maingame
    #для теста, добавляю в вызов curentplayer и пробую его вместо maingame.playerslist отправить
    conn.send(pickle.dumps(curplayer))
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
                    '''chat_server.add_msg(data.list[-1])
                    print(f'Trying to add {data.list[-1]} by {current_process().name}')'''
                finally:
                    lock.release()

                '''myq.put(data.list[-1])'''

                mainq.put('Update')
                event.wait()


                reply = maingame.playerslist

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except error as e:
            print(e)
            #break

    print("Lost connection")
    conn.close()
    return maingame


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


# записали локальный адрес в список
whereami = get_ip()
# пишем где мы
print(f"Server started at {whereami[0]}:{whereami[1]}")

server = "127.0.0.1"#str(whereami[0])
port = 5555#whereami[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# стартанули сервер
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

# слушаем, ждём
s.listen()
print("Waiting for a connection, Server Started")

# служебные штуки для очередей и событий
lock = Lock()
maingame = Multisnake_Gamefield.GameField()


event = threading.Event()

myq = queue.Queue()
mainq = queue.Queue()

# начало работы


if __name__ == '__main__':

    while True:

        connection, addr = s.accept()
        print("Connected to:", addr)
        pl = Multisnake_Gamefield.Player(maingame)
        for i in range(30):
            print(maingame.gamematrix[i], end="\n")
        newconnection = threading.Thread(target=threaded_client, args=(connection, maingame, pl, lock, mainq, event))

        newconnection.start()
        event.set()
        if not mainq.empty():
            mainq.get()


            # вот тут из очереди надо будет гонять обновление карты относительно действий игроков из очереди
            while not myq.empty():
                taken = myq.get()
                chat_server.add_msg(taken)
                print(taken, ' from myq')
        newconnection.join(1)
