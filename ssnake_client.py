from tkinter import Tk, Canvas
import random

game_on = False
WIDTH, HEIGHT = 800, 600
blocksize = 20
apple = [0,0, False, 0] # global x y of current apple
background = "#3caa3c"
snakemoves = {"Up": [0,-1], "Down": [0,1], "Left": [-1,0], "Right": [1,0]}


def Painter(coords, objecttype=1):                  # 0 - поле ; 1 - яблоко ; 2 - голова ; 3 - тело ; 4 - препятствие
    if objecttype == 1:
        c.create_oval(coords[0] * blocksize, coords[1] * blocksize, coords[0] * blocksize + blocksize,
                      coords[1] * blocksize + blocksize, width=0, fill="red", tag="apple")
    elif objecttype == 2:
        c.create_rectangle(coords[0]*blocksize, coords[1]*blocksize, coords[0]*blocksize + blocksize,
                           coords[1]*blocksize + blocksize, width=1, outline=background, fill="#f64a46", tag="head")
    elif objecttype == 3:
        c.create_rectangle(coords[0]*blocksize,coords[1]*blocksize, coords[0]*blocksize + blocksize, 
                           coords[1]*blocksize + blocksize, width=1, outline=background, fill="#6a5d4d", tag="body")
    elif objecttype == 4:
        c.create_rectangle(coords[0] * blocksize, coords[1] * blocksize, coords[0] * blocksize + blocksize,
                           coords[1] * blocksize + blocksize, width=1, outline=background, fill="#7f4870", tag="Border")
    elif objecttype == 0:
        c.create_rectangle(coords[0]*blocksize, coords[1]*blocksize, coords[0]*blocksize + blocksize,
                           coords[1]*blocksize + blocksize, width=0, fill=background)


def changevector(event):
    if player.vector[0] == -1*snakemoves[str(event.keysym)][0] or player.vector[1] == -1*snakemoves[str(event.keysym)][1]:
            pass
    else:            
        player.vector[0] = snakemoves[str(event.keysym)][0]
        player.vector[1] = snakemoves[str(event.keysym)][1]

def spawnapple():
    #надо не забыть на сервере не ставить яблоки там где есть игроки
    apple[0], apple[1] = random.randint(1,WIDTH/blocksize-1), random.randint(1,HEIGHT/blocksize-1)    
    apple[2] = True
    c.delete("apple")
    Painter(apple)


def main(): 
    if apple[2] != True: 
        spawnapple()
    if player.head[0] == apple[0] and player.head[1] == apple[1]:
        player.move_app()
        apple[2] = False
        apple[3] += 1
        c.delete("score")
        score = c.create_text(100,20,anchor="ne",text=f"Total apples: {apple[3]} \n Snake_size: {len(player.body)}", tag="score")
    else:
        player.move()
    
    root.after(150,main)


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

    def move_app(self):
        c.delete("head")
        c.delete("apple")
        
        self.body.insert(0,[self.head[0], self.head[1]])
       # self.body[0][0], self.body[0][1] = self.head[0], self.head[1]
        self.head[0], self.head[1] = self.head[0] + self.vector[0], self.head[1] + self.vector[1]

        Painter(self.head, 2)
        Painter(self.body[0], 3)


    def move(self):
        
        c.delete("head")
        c.delete("body")

        for i in range(len(self.body)-1,0,-1):
            self.body[i][0], self.body[i][1] = self.body[i-1][0], self.body[i-1][1]

        self.body[0][0], self.body[0][1] = self.head[0], self.head[1]
        self.head[0], self.head[1] = self.head[0] + self.vector[0], self.head[1] + self.vector[1]

        Painter(self.head, 2)
        for i in self.body:
            Painter(i, 3)



root = Tk()
root.title("Multiplayer snake")

c = Canvas(root, width=WIDTH, height=HEIGHT, bg=background)
score = c.create_text(100,20,anchor="ne",text=f"Total apples: {apple[3]}", tag="score")
c.grid()
player = snake()
c.focus_set()
main()
c.bind("<KeyPress>", changevector)

root.mainloop()