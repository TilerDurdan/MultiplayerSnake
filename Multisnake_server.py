import socket
import threading
import socket
from _thread import *
import pickle
import threading
from multiprocessing import Process, Queue, Lock, Event, current_process
import queue
import time


def threaded_client(conn, chat_s, lock, mainq, event):
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
                    '''chat_server.add_msg(data.list[-1])
                    print(f'Trying to add {data.list[-1]} by {current_process().name}')'''
                finally:
                    lock.release()

                '''myq.put(data.list[-1])

                mainq.put('Update')'''
                event.wait()

                #time.sleep(0.1)
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

server = str(whereami[0])
port = whereami[1]

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
maingame = gamefield()

event = threading.Event()

myq = queue.Queue()
mainq = queue.Queue()

# начало работы


if __name__ == '__main__':

    currentuser = 0



    while True:

        connection, addr = s.accept()
        print("Connected to:", addr)

        newconnection = threading.Thread(target=threaded_client, args=(connection, snake_server, lock, mainq, event))

        newconnection.start()
        event.set()
        if not mainq.empty():
            mainq.get()

            """
                def newplayer(self, data):

        id =  str(uuid.uuid4())[:5]
        set_id = False
        Nick = data[6:]



        while not set_id:
            if id not in self.idlist:
                self.idlist.append([id, Nick, start_pos])
                set_id = True
            else:
                id = str(uuid.uuid4())[:5]

        start_pos = self.gen_start(id)
        return id
            """

            # вот тут из очереди надо будет гонять обновление карты относительно действий игроков из очереди
            while not myq.empty():
                taken = myq.get()
                chat_server.add_msg(taken)
                print(taken, ' from myq')
        newconnection.join(1)
