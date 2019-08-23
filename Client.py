from tkinter import Tk, Canvas
import random

game_on = False
WIDTH, HEIGHT = 800, 600
blocksize = 20
background = "#3caa3c"
snakemoves = {"Up": (-1,0), "Down": (1,0), "Left": (-1,0), "Right": (1,0)}


def Painter(coords, objecttype=1):                  # 0 - поле ; 1 - яблоко ; 2 - голова ; 3 - тело ; 4 - препятствие
    if objecttype == 1:
        c.create_oval(coords[0] * blocksize, coords[1] * blocksize, coords[0] * blocksize + blocksize,
                      coords[1] * blocksize + blocksize, width=0, fill="red")
    elif objecttype == 2:
        c.create_rectangle(coords[0]*blocksize, coords[1]*blocksize, coords[0]*blocksize + blocksize,
                           coords[1]*blocksize + blocksize, width=1, outline=background, fill="#f64a46")
    elif objecttype == 3:
        c.create_rectangle(coords[0]*blocksize,coords[1]*blocksize, coords[0]*blocksize + blocksize, 
                           coords[1]*blocksize + blocksize, width=1, outline=background, fill="#6a5d4d")
    elif objecttype == 4:
        c.create_rectangle(coords[0] * blocksize, coords[1] * blocksize, coords[0] * blocksize + blocksize,
                           coords[1] * blocksize + blocksize, width=1, outline=background, fill="#7f4870")
    elif objecttype == 0:
        c.create_rectangle(coords[0]*blocksize, coords[1]*blocksize, coords[0]*blocksize + blocksize,
                           coords[1]*blocksize + blocksize, width=0, fill=background)



class snake(object):

    head = []  # координаты головы
    body = []  # координаты хвоста
    vector = []  # движение по умолчанию

    def __init__(self):
        self.head = [3, HEIGHT / (2 * blocksize)]
        self.body = [[2, HEIGHT/(2*blocksize)], [1, HEIGHT/(2*blocksize)]]
        self.vector = [snakemoves["Right"][0],snakemoves["Right"][1]]
        Painter(self.head, 2)
        Painter(self.body[1], 3)
        Painter(self.body[0], 3)

    def move(self,*args):
        #Painter([self.head[0]+self.vector[0], self.head[1]+self.vector[1]], 2)
        #Painter([self.head[0], self.head[1]], 0)
        #Painter(self.body[len(self.body) - 1], 0)

        #self.head[0] = self.head[0] + self.vector[0]
        #self.head[1] = self.head[1] + self.vector[1]

        #self.body[1][0], self.body[1][1] = self.body[0][0], self.body[0][1]
        #self.body[0][0], self.body[0][1] = self.head[0], self.head[1]

        for i in self.body:
            Painter(i, 0)

        for i in range(len(self.body)-1,1,-1):
            self.body[i][0], self.body[i][1] = self.body[i-1][0], self.body[i-1][1]
            #Painter(self.body[i], 3)

        self.body[0][0], self.body[0][1] = self.head[0], self.head[1]
        self.head[0], self.head[1] = self.head[0] + self.vector[0], self.head[1] + self.vector[1]

        c.clipboard_clear()
        Painter(self.head, 2)
        for i in self.body:
            Painter(i, 3)
    

root = Tk()
root.title("Multiplayer snake")

c = Canvas(root, width=WIDTH, height=HEIGHT, bg=background)
c.grid()
player = snake()
c.focus_set()
c.bind("<Key>", player.move)
root.mainloop()

