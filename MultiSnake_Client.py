#Клиент для мультиплеера
from tkinter import * #Tk, Canvas, messagebox
import random
import Multisnake_network



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


conn_from_menu = ['', '']

print(firtsmenu())
