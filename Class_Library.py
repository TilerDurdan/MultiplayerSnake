import random
import uuid

class Snake(object):
    Head = []  # координаты головы
    NickName = "UnnamedPlayer"
    HeadColor = "#f64a46"
    Body = []  # координаты хвоста
    Vector = []  # движение по умолчанию
    SnakeMoves = {"Up": [0, -1], "Down": [0, 1], "Left": [-1, 0], "Right": [1, 0]}
    Snake_Game = True

    def __init__(self):
        self.head = [3, HEIGHT / (2 * BlockSize)]
        self.body = [[2, HEIGHT / (2 * BlockSize)], [1, HEIGHT / (2 * BlockSize)]]
        self.vector = [self.SnakeMoves["Right"][0], self.SnakeMoves["Right"][1]]
        Painter(self.head, 2)
        Painter(self.body[1], 3)
        Painter(self.body[0], 3)

    def move_app(self):
    # анимация движения  если съели яблоко

        c.delete("head")
        c.delete("apple")

        self.body.insert(0, [self.head[0], self.head[1]])
        self.head[0], self.head[1] = self.head[0] + self.vector[0], self.head[1] + self.vector[1]

        Painter(self.head, 2)
        Painter(self.body[0], 3)

        if not(checkoutstep()):
            self.Snake_Game = False

    def move(self):
    # анимация движения без яблока

        c.delete("head")
        c.delete("body")

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0], self.body[i][1] = self.body[i - 1][0], self.body[i - 1][1]

        self.body[0][0], self.body[0][1] = self.head[0], self.head[1]
        self.head[0], self.head[1] = self.head[0] + self.vector[0], self.head[1] + self.vector[1]

        Painter(self.head, 2)
        for i in self.body:
            Painter(i, 3)

        if not(self.checkoutstep()):
            self.Snake_Game = False

    def checkoutstep(self):

        nextx, nexty = self.head[0], self.head[1]

        if 0 <= nextx <= WIDTH / BlockSize and 0 <= nexty <= HEIGHT / BlockSize:
            pass
        else:
            return False
        # на первом шаге проверки проверяем не наступим ли мы за границы и если что отсекаем сразу

        # на втором будем смотреть на самоедство
        for b in self.body:
            if nextx == b[0] and nexty == b[1]:
                return False
        # на третьем шаге мы добавим наступление на хвосты других игроков
        # или в случае выхода логики в сервер - на список всех змеек

        return True

    def changevector(self, event):
        if str(event.keysym) in self.SnakeMoves:
            if self.vector[0] == -1 * self.SnakeMoves[str(event.keysym)][0] or self.vector[1] == -1 * \
                    self.SnakeMoves[str(event.keysym)][1]:
                pass
            else:
                self.vector[0] = self.SnakeMoves[str(event.keysym)][0]
                self.vector[1] = self.SnakeMoves[str(event.keysym)][1]
        else:
            pass


class GameField(object):

    game = []
    playerslist = []
    idlist = []
    start_positions = []
    height = 30
    width = 40

    def __init__(self, w, h):

        self.game = [[0 for i in range(w)] for j in range(h)]
        self.height, self.width = h, w

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

    def gen_start(self,id):
        pos = random.randint(0, 2*self.height)
        selected = False
        while not selected:
            if pos not in self.start_positions:
                self.start_positions.append([id, pos])
            else:
                pos = random.randint(0, 2*self.height)
        return pos

