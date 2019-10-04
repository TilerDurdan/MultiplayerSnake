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

class Splayer(object):
    id = ''
    vector = []

def threaded_client(conn, maing, curplayer, lock, mainq, event):

    global maingame
    #для теста, добавляю в вызов curentplayer и пробую его вместо maingame.playerslist отправить
    conn.send(pickle.dumps(curplayer))
    cur_id = curplayer.id
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



                mainq.put('Update')
                event.wait()
                if type(data) != type(curplayer):
                    maingame.playerslist[cur_id].vector[0] = data[1][0]
                    maingame.playerslist[cur_id].vector[1] = data[1][1]
                    if not deadlycollision(maingame, cur_id):
                        moveplayer(maingame, cur_id)
                        for i in maingame.apples:
                            if i[0] == maingame.playerslist[cur_id].head[0] and i[1] == \
                                    maingame.playerslist[cur_id].head[1]:
                                maingame.delapple(i[0],i[1])
                                maingame.spawnapple()
                                maingame.updateapples()
                                extendplayer(maingame,cur_id)
                    else:
                        playerdead(maingame, cur_id)



                reply = maingame.playerslist

                print("Received: ", data)
                print("Sending : ", reply, maingame.playerslist[cur_id].vector)

            conn.sendall(pickle.dumps(reply))
        except error as e:
            print(e)
            maingame.playerslist.pop(cur_id)
            break
        except EOFError:
            print('NO DATA! Player close window')
            maingame.playerslist.pop(cur_id)
            break

    print("Lost connection")
    conn.close()
    return maingame

def playerdead(game, pid):
    pass


def deadlycollision(game, pid):

    newx = game.playerslist[pid].head[0] + game.playerslist[pid].vector[0]
    newy = game.playerslist[pid].head[1] + game.playerslist[pid].vector[1]

    if newx < 0 or newx > (game.width / game.blocksize) -1:
        return True

    if newy < 0 or newy > (game.height / game.blocksize) -1:
        return True

    if game.gamematrix[newy][newx] == 0 or game.gamematrix[newy][newx] == "@":
        pass
    else:
        return True

    return False

def extendplayer(game, pid):

    #вставили голову в тело на 0 позицию, переписали матрицу

    game.playerslist[pid].body.insert(0, [game.playerslist[pid].head[0], game.playerslist[pid].head[1]])
    game.gamematrix[game.playerslist[pid].head[1]][game.playerslist[pid].head[0]] = pid

    # двинули голову , переписали матрицу
    game.playerslist[pid].head[0], game.playerslist[pid].head[1] = game.playerslist[pid].head[0] + game.playerslist[pid].vector[0], game.playerslist[pid].head[1] + game.playerslist[pid].vector[1]

    game.gamematrix[game.playerslist[pid].head[1]][game.playerslist[pid].head[0]] = "-" + pid




def moveplayer(game, pid):

    game.gamematrix[game.playerslist[pid].body[len(game.playerslist[pid].body) - 1][1]][game.playerslist[pid].body[len(game.playerslist[pid].body) - 1][0]] = 0

    for i in range(len(game.playerslist[pid].body) - 1,0,-1):
        game.playerslist[pid].body[i][0], game.playerslist[pid].body[i][1] = game.playerslist[pid].body[i - 1][0], game.playerslist[pid].body[i - 1][1]

    game.playerslist[pid].body[0][0],game.playerslist[pid].body[0][1] = game.playerslist[pid].head[0],game.playerslist[pid].head[1]
    game.playerslist[pid].head[0],game.playerslist[pid].head[1] = game.playerslist[pid].head[0] + game.playerslist[pid].vector[0],game.playerslist[pid].head[1] + game.playerslist[pid].vector[1]

    # не забыть поменять матрицу
    game.gamematrix[game.playerslist[pid].head[1]][game.playerslist[pid].head[0]] = "-" + pid
    game.gamematrix[game.playerslist[pid].body[0][1]][game.playerslist[pid].body[0][0]] = pid


def fixmatrix(game):
    for i in range(40):
        for j in range(30):
            if game.gamematrix[j][i] == "-" or game.gamematrix[j][i] == "":
                game.gamematrix[j][i] = 0


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
maingame.spawnapple()
maingame.updateapples()
fixmatrix(maingame)
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
