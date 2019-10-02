import random
import uuid


class GameField(object):

    snakeMoves = {"Up": [0, -1], "Down": [0, 1], "Left": [-1, 0], "Right": [1, 0]}
    width = 800
    height = 600
    blocksize = 20
    playerslist = {}
    gamematrix = [[0 for i in range(40)] for j in range(30)]

    def __init__(self):

        #self.gamematrix = [[0 for i in range(40)] for j in range(30)]
        #self.playerslist = {}
        pass


class Player:

        id = ""

    # список игроков 
        def __init__(self, gamefield.playlist):

            self.head = []
            self.body = []
            self.vector = []
            self.id = self.newplayer(GameField.playerslist)

        def newplayer(self, playerslist):

            pid = str(uuid.uuid4())[:5]
            set_id = False

            while not set_id:
                if pid not in playerslist.keys():

                    set_id = True
                else:
                    pid = str(uuid.uuid4())[:5]

                self.spawnpos(GameField.gamematrix)

            self.spawnpos(GameField.gamematrix)
            playerslist[pid] = self
            return pid

        def spawnpos(self, matrix):

            x = random.randint(3, GameField.height / GameField.blocksize - 3)
            y = random.randint(3, GameField.width / GameField.blocksize - 4)
            if x > GameField.height / 2:
                k = -1
            else:
                k = 1

            free = False
            while not free:
                if matrix[x][y] == 0 and matrix[x-1*k][y] == 0 and matrix[x-2*k][y] == 0:
                    self.head = [x, y]
                    matrix[x][y] = "-" + self.id
                    self.body.append([x-1*k, y])
                    self.body.append([x-2*k, y])
                    matrix[x - 1 * k][y], matrix[x - 2 * k][y] = self.id, self.id
                    self.vector = [k, 0]
                    free = True
                else:
                    x = random.randint(GameField.height / GameField.blocksize)
                    y = random.randint(3, GameField.width / GameField.blocksize - 4)
                    if x > GameField.height / 2:
                        k = -1
                    else:
                        k = 1
