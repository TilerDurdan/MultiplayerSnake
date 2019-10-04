import random
import uuid


class GameField(object):

    snakeMoves = {"Up": [0, -1], "Down": [0, 1], "Left": [-1, 0], "Right": [1, 0]}
    width = 800
    height = 600
    blocksize = 20
    playerslist = {}
    gamematrix = [[0 for i in range(40)] for j in range(30)]
    apples = []

    def __init__(self):

        #self.gamematrix = [[0 for i in range(40)] for j in range(30)]
        #self.playerslist = {}
        pass

    def spawnapple(self):

        canspawn = False
        while not canspawn:
            ax = random.randint(0,40)
            ay = random.randint(0,30)
            if self.gamematrix[ay][ax] == 0:
                self.apples.append([ax, ay])
                canspawn = True

    def delapple(self, x, y):
        for i in self.apples:
            if i[0] == y and i[1] == x:
                self.apples.remove([x, y])


    def updateapples(self):
        self.playerslist["apple"] = []

        for i in self.apples:
            self.playerslist["apple"].append(i)

class Player:

        id = ""

    # список игроков 
        def __init__(self, gf):

            self.head = []
            self.body = []
            self.vector = []
            self.id = self.newplayer(gf)
            self.spawnpos(gf.gamematrix)

        def newplayer(self, gf):

            pid = str(uuid.uuid4())[:5]
            set_id = False

            while not set_id:
                if pid not in gf.playerslist.keys():

                    set_id = True
                else:
                    pid = str(uuid.uuid4())[:5]

            #self.spawnpos(gf.gamematrix)

            gf.playerslist[pid] = self
            return pid

        def spawnpos(self, matrix):



            #y and x перепутал

            free = False
            while not free:
                y = random.randint(3,GameField.height / GameField.blocksize - 3)
                x = random.randint(3,GameField.width / GameField.blocksize - 4)
                if x > GameField.height / (2 * GameField.blocksize):
                    k = -1
                else:
                    k = 1

                if matrix[x][y] == 0 and matrix[x-1*k][y] == 0 and matrix[x-2*k][y] == 0:
                    self.head = [x, y]
                    matrix[x][y] = "-" + self.id
                    self.body.append([x-1*k, y])
                    self.body.append([x-2*k, y])
                    matrix[x - 1 * k][y] = self.id
                    matrix[x - 2 * k][y] = self.id
                    self.vector = [k, 0]
                    free = True

            pass