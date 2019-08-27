import  socket
import threading
import uuid

# MAKE SHORT ID
# str(uuid.uuid4())[:5]
# short_id for head might be -1*id


GameField = [[0 for i in range(40)] for j in range(30)]

for j in range(len(GameField)):
    for i in range(len(GameField[j])):
        print(GameField[j][i],end="\t")
    print("\n")
