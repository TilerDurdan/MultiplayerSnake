import  socket
import threading
import uuid
import time

# MAKE SHORT ID
# str(uuid.uuid4())[:5]
# short_id for head might be -1*id


GameField = [[0 for i in range(40)] for j in range(30)]

for j in range(len(GameField)):
    for i in range(len(GameField[j])):
        print(GameField[j][i],end="\t")
    print("\n")

# список ServerPlayer'ов состав [id,ip:port, Имя, очки, координаты тушки и головы, цвет головы?, статус игры]
PlayersList = []
idlist = []

class ServerPlayer(self):

    def __init__(self):
        pid = CreateId() # создаем короткий и уникальный id
        ingame = True    # игрок не выбыл
        PlayerScore = 0  # набранные очки
        pass
    
    def PlayerConnected(self):
        pass
    
    def PlacePlayers(self):
    # ёлочкой сверху-вниз слева-направо по нисходящей
    # если позиция больше середины (считай правая) то переориентировать змеюку и поставить ей вектор
        pass

    def CreateId(self):
        set_id = False

        while not set_id:
            newid = str(uuid.uuid4)[:5]
            if newid not in idlist:
                set_id = True
                idlist.append(newid)
               
        # тут же прописываем игроку его id
        return newid
    
    def MovePlayer(self):
        pass
    

class GlobalTimer(self):

    CountDown = 100  # если не ошибся то в секундах
    def __init__(self):
        GameContinue = True
        pass
    
    def NewRound(self):
        if self.CountDown > 0:
            self.CountDown -= 1
        else:
            self.GameContinue = False
            StopGame()

class Apple(self):
# а почему бы не сделать класс под яблочко, которое будет определять сколько ему жить и где находиться
# после того как время пришло яблоко можно убрать с поля или превратить в "плохое яблоко ещё на 5-10 секунд"
# за съедание плохого яблока можно снижать очки и отбрасывать кусок хвоста

    TimeToLive = time.time() + 10
    ApplePosition = [] # XY of apple

    def __init__(self):
        pass
        

# 
# закончили с классами
# начинаем всякие служебные функции
#

def StartGame():
    pass

def StopGame():
    pass

def isHead(XYpos):
    # определяем по координатам клетки голова или нет
    if GameField[XYpos[0]][XYpos[1]] in idlist and GameField[XYpos[0]][XYpos[1]][0] == "-":
        return True
    else:
        return False


    