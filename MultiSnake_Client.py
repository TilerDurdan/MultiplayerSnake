#Клиент для мультиплеера
from tkinter import * #Tk, Canvas, messagebox
import random
from Multisnake_network import Network
import Multisnake_Gamefield


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
    pass


conn_from_menu = firtsmenu()

net = Network(conn_from_menu[0], conn_from_menu[1])

p = net.getP()
print(p)#.playerslist)
ans = net.send(p)
my_id = p.id
print(my_id)
'''
for i in ans.keys():
    print(ans[i].id + "\n", str(ans[i].head[0]) + " " + str(ans[i].head[1]) + "\n", str(ans[i].vector[0]) + " " + str(ans[i].vector[1]))'''



WIDTH, HEIGHT = 800, 600
BlockSize = 20
apple = []
background = "#3caa3c"
SnakeMoves = {"Up": [0, -1], "Down": [0, 1], "Left": [-1, 0], "Right": [1, 0]}

#         рисуем

if __name__ == '__main__':
    root = Tk()
    root.title("Multiplayer snake")
    CloseGame = False
    c = Canvas(root, width=WIDTH, height=HEIGHT, bg=background)
    score = c.create_text(100, 20, anchor="ne", text=f"Total apples: {apple[3]}", tag="score")
    c.grid()

    c.focus_set()

    game_on = True

    main()
    c.bind("<KeyPress>", changevector)

    root.mainloop()