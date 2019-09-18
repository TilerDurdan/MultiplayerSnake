from tkinter import Tk, Canvas
import random
import  socket
import sys
import snake_client_try as ClientNetwork





def Painter(coords, objecttype = 1):

    # 0 - поле ; 1 - яблоко ; 2 - голова ; 3 - тело ; 4 - препятствие/граница

    if objecttype == 1:
        c.create_oval(coords[0] * BlockSize, coords[1] * BlockSize, coords[0] * BlockSize + BlockSize,
                      coords[1] * BlockSize + BlockSize, width=0, fill="#c92435", tag="apple")
    elif objecttype == 2:
        c.create_rectangle(coords[0] * BlockSize, coords[1] * BlockSize, coords[0] * BlockSize + BlockSize,
                           coords[1] * BlockSize + BlockSize, width=1, outline=background, fill="#f64a46", tag="head")
    elif objecttype == 3:
        c.create_rectangle(coords[0] * BlockSize, coords[1] * BlockSize, coords[0] * BlockSize + BlockSize,
                           coords[1] * BlockSize + BlockSize, width=1, outline=background, fill="#6a5d4d", tag="body")
    elif objecttype == 4:
        c.create_rectangle(coords[0] * BlockSize, coords[1] * BlockSize, coords[0] * BlockSize + BlockSize,
                           coords[1] * BlockSize + BlockSize, width=1, outline=background, fill="#7f4870", tag="Border")
    elif objecttype == 0:
        c.create_rectangle(coords[0] * BlockSize, coords[1] * BlockSize, coords[0] * BlockSize + BlockSize,
                           coords[1] * BlockSize + BlockSize, width=0, fill=background)


def changevector(event):
    global CloseGame
    if str(event.keysym) in SnakeMoves:
        if player.vector[0] == -1 * SnakeMoves[str(event.keysym)][0] or player.vector[1] == -1 * \
                SnakeMoves[str(event.keysym)][1]:
            pass
        else:
            player.vector[0] = SnakeMoves[str(event.keysym)][0]
            player.vector[1] = SnakeMoves[str(event.keysym)][1]
    elif  not game_on and event.keysym == "space":
        c.delete("gameovertext")
        newgamelabel = c.create_text(400, 300, text="Press Y to play new game \nN for exit", tag="newgametext")
    elif not game_on and event.keysym == "y" or event.keysym == "Y":
        c.delete("newgametext")
    elif not game_on and event.keysym == "n" or event.keysym == "N":
        print("Close game")
        root.destroy()


def spawnapple():
    # надо не забыть на сервере не ставить яблоки там где есть игроки
    apple[0], apple[1] = random.randint(1, WIDTH / BlockSize - 1), random.randint(1, HEIGHT / BlockSize - 1)
    apple[2] = True
    c.delete("apple")
    Painter(apple)

def checkoutstep():

    nextx, nexty = player.head[0], player.head[1]

    if 0 <= nextx <= WIDTH/BlockSize and 0 <= nexty <= HEIGHT/BlockSize:
        pass
    else:
        return False
    # на первом шаге проверки проверяем не наступим ли мы за границы и если что отсекаем сразу

    #на втором будем смотреть на самоедство
    for b in player.body:
        if nextx == b[0] and nexty == b[1]:
            return  False
    # на третьем шаге мы добавим наступление на хвосты других игроков
    # или в случае выхода логики в сервер - на список всех змеек

    return True


def main():

    global game_on

    if game_on:
        if not apple[2]:
            spawnapple()
        if player.head[0] == apple[0] and player.head[1] == apple[1]:
            player.move_app()
            apple[2] = False
            apple[3] += 1
            c.delete("score")
            score = c.create_text(120, 20, anchor="ne", text=f"Total apples: {apple[3]} \n "
                                  f"Snake_size: {len(player.body)}", tag="score")
        else:
            player.move()

        root.after(150, main)
    else:
        gameover = c.create_text(400, 300,  text="GAME OVER \nPress Space for new game", tag="gameovertext")
        player.dead_snake()


class snake(object):
    head = []  # координаты головы
    NickName = "UnnamedPlayer"
    HeadColor = "#f64a46"
    body = []  # координаты хвоста
    vector = []  # движение по умолчанию

    def __init__(self):
        self.head = [3, HEIGHT / (2 * BlockSize)]
        self.body = [[2, HEIGHT / (2 * BlockSize)], [1, HEIGHT / (2 * BlockSize)]]
        self.vector = [SnakeMoves["Right"][0], SnakeMoves["Right"][1]]
        Painter(self.head, 2)
        Painter(self.body[1], 3)
        Painter(self.body[0], 3)

    def move_app(self):
    # анимация движения  если съели яблоко

        global  game_on
        c.delete("head")
        c.delete("apple")

        self.body.insert(0, [self.head[0], self.head[1]])
        self.head[0], self.head[1] = self.head[0] + self.vector[0], self.head[1] + self.vector[1]

        Painter(self.head, 2)
        Painter(self.body[0], 3)

        if not(checkoutstep()):
            game_on = False

    def move(self):
    # анимация движения без яблока

        global game_on

        c.delete("head")
        c.delete("body")

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0], self.body[i][1] = self.body[i - 1][0], self.body[i - 1][1]

        self.body[0][0], self.body[0][1] = self.head[0], self.head[1]
        self.head[0], self.head[1] = self.head[0] + self.vector[0], self.head[1] + self.vector[1]

        Painter(self.head, 2)
        for i in self.body:
            Painter(i, 3)

        if not(checkoutstep()):
            game_on = False


    def dead_snake(self):

        c.delete("head")
        c.delete("body")
        Painter(self.body[0])


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


def connect_game():
    net = Network()
    return net



game_on = False
WIDTH, HEIGHT = 800, 600
BlockSize = 20
apple = [0, 0, False, 0]  # global x y of current apple T/F is for existing on board, last is for counter
background = "#3caa3c"
SnakeMoves = {"Up": [0, -1], "Down": [0, 1], "Left": [-1, 0], "Right": [1, 0]}

if __name__ == '__main__':
    root = Tk()
    root.title("Multiplayer snake")
    CloseGame = False
    c = Canvas(root, width=WIDTH, height=HEIGHT, bg=background)
    score = c.create_text(100, 20, anchor="ne", text=f"Total apples: {apple[3]}", tag="score")
    c.grid()
    player = snake()
    c.focus_set()

    game_on = True

    # создаём подключение
#    n = connect_game()
#    connection = n.getP()

    # запускаем мэйн

    main()
    c.bind("<KeyPress>", changevector)

    root.mainloop()

    # https://jenyay.net/Programming/Argparse