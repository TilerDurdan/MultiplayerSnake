#Клиент для мультиплеера
from tkinter import * #Tk, Canvas, messagebox
import random
from Multisnake_network import Network
import Multisnake_Gamefield


class SPlayer(object):
    def __init__(self, id, v):
        self.id = id
        self.vector = v


def firtsmenu():


    global conn_from_menu

    def clear():
        ip_entry.delete(0, END)
        port_entry.delete(0, END)

    def suggest():
        global conn_from_menu
        conn_from_menu = [ip_entry.get(), int(port_entry.get())]
        emenu.destroy()

    emenu = Tk()
    emenu.title("Connection menu")
    emenu.geometry("300x100")
    emenu.grid()

    ip_label = Label(text="Enter IP address:")
    port_label = Label(text="Enter port:")

    ip_label.grid(row=0,column=0,sticky="w")
    port_label.grid(row=1, column=0, sticky="w")

    ip_entry = Entry()
    port_entry = Entry()

    ip_entry.grid(row=0, column=1, padx=5, pady=5)
    port_entry.grid(row=1, column=1, padx=5, pady=5)

    ip_entry.insert(0, "127.0.0.1")
    port_entry.insert(0, "5555")

    suggest_button = Button(text="Suggest", command=suggest)
    clear_button = Button(text="Clear", command=clear)

    suggest_button.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    clear_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")

    emenu.mainloop()

    return conn_from_menu

def main():
    res = net.send([myPlayer.id, myPlayer.vector])
    c.delete("all")

    for i in res.keys():

        if i == "apples":
            for j in res["apples"]:
                drawapple(j)

        if i == my_id:
            drawhead(res[i].head, True)
            for j in res[i].body:
                drawbody(j, True)
        else:
            drawhead(res[i].head, False)
            for j in res[i].body:
                drawbody(j, False)

    root.after(200, main)


def changevector(event):
    if str(event.keysym) in SnakeMoves:
        if myPlayer.vector[0] == -1 * SnakeMoves[str(event.keysym)][0] or myPlayer.vector[1] == -1 * \
                SnakeMoves[str(event.keysym)][1]:
            pass
        else:
            myPlayer.vector[0] = SnakeMoves[str(event.keysym)][0]
            myPlayer.vector[1] = SnakeMoves[str(event.keysym)][1]


def drawhead(coords, mine):
    if mine == True:
        headcolor = "#f64a46"
    else:
        headcolor = "#000080"

    c.create_rectangle(coords[0] * BlockSize, coords[1] * BlockSize, coords[0] * BlockSize + BlockSize,
                       coords[1] * BlockSize + BlockSize, width=1, outline=background, fill=headcolor, tag="myhead")



def drawbody(coords, mine):

    if mine:
        bodycolor = "#6a5d4d"
    else:
        bodycolor = "#524b3d"
    c.create_rectangle(coords[0] * BlockSize, coords[1] * BlockSize, coords[0] * BlockSize + BlockSize,
                       coords[1] * BlockSize + BlockSize, width=1, outline=background, fill=bodycolor, tag="body")

def drawapple(coords):
    c.create_oval(coords[0] * BlockSize, coords[1] * BlockSize, coords[0] * BlockSize + BlockSize,
                  coords[1] * BlockSize + BlockSize, width=0, fill="#c92435", tag="apple")


conn_from_menu = firtsmenu()

net = Network(conn_from_menu[0], conn_from_menu[1])

p = net.getP()
print(p)#.playerslist)
ans = net.send(p)
my_id = p.id
my_vector = p.vector

'''
for i in ans.keys():
    print(ans[i].id + "\n", str(ans[i].head[0]) + " " + str(ans[i].head[1]) + "\n", str(ans[i].vector[0]) + " " + str(ans[i].vector[1]))'''



WIDTH, HEIGHT = 600, 800
BlockSize = 20
apple = []
background = "#3caa3c"
SnakeMoves = {"Up": [0, -1], "Down": [0, 1], "Left": [-1, 0], "Right": [1, 0]}
myPlayer = SPlayer(my_id, my_vector)

#         рисуем

if __name__ == '__main__':
    root = Tk()
    root.title("Multiplayer snake")
    CloseGame = False
    c = Canvas(root, width=WIDTH, height=HEIGHT, bg=background)
    #score = c.create_text(100, 20, anchor="ne", text=f"Total apples: {apple[3]}", tag="score")
    c.grid()

    c.focus_set()

    game_on = True

    main()
    c.bind("<KeyPress>", changevector)

    root.mainloop()