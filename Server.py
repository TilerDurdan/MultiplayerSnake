import socketserver
import random


# игровое поле 0 - пусто 1 - яблоко id - игрок (-1)*id голова игрока
GameField = [[0 for i in range(40)] for j in range(30)]



class Apple(object):

    x,y = 0, 0

    def __init__(self):

        set_apple = False

        while not set_apple:
            xcoor = random.randint(0,40)
            ycoor = random.randint(0,40)

            if GameField[xcoor][ycoor] == 0:
                self.x = xcoor
                self.y = ycoor
                set_apple = True
            else:
                xcoor = random.randint(0, 40)
                ycoor = random.randint(0, 40)

