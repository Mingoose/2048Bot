import random
import PySimpleGUI as sg


def move(direction,game,score):
    temp = [[],[],[],[]]
    for i in range(4):
        for j in range(4):
            temp[i].append(0)
    if direction == "up":
        j = 0
        while j < 4:
            i = 0
            while i < 4:
                if game[i][j] == 0:
                    i += 1
                elif i < 3 and game[i][j] == game[i+1][j]:
                    temp[vertIndex(temp,j)][j] = game[i][j]*2
                    score += game[i][j]*2
                    i += 2
                elif i < 2 and game[i][j] == game[i+2][j] and game[i+1][j] == 0 :
                    temp[vertIndex(temp,j)][j] = game[i][j]*2
                    score += game[i][j]*2
                    i += 3
                elif i < 1 and game[i][j] == game[i+3][j] and game[i+1][j] == 0 and game[i+2][j] == 0:
                    temp[vertIndex(temp,j)][j] = game[i][j]*2
                    score += game[i][j]*2
                    i += 4
                else:
                    temp[vertIndex(temp,j)][j] = game[i][j]
                    i += 1
            j += 1
        game = temp
                            
    elif direction == "left":
        i = 0
        while i < 4:
            j = 0
            while j < 4:
                if game[i][j] == 0:
                    j += 1
                elif j < 3 and game[i][j] == game[i][j+1]:
                    temp[i][temp[i].index(0)] = game[i][j]*2
                    score += game[i][j]*2
                    j += 2
                elif j < 2 and game[i][j] == game[i][j+2] and game[i][j+1] == 0 :
                    temp[i][temp[i].index(0)] = game[i][j]*2
                    score += game[i][j]*2
                    j += 3
                elif j < 1 and game[i][j] == game[i][j+3] and game[i][j+1] == 0 and game[i][j+2] == 0:
                    temp[i][temp[i].index(0)] = game[i][j]*2
                    score += game[i][j]*2
                    j += 4
                else:
                    temp[i][temp[i].index(0)] = game[i][j]
                    j += 1
            i += 1
        game = temp
    elif direction == "right":
        i = 3
        while i > -1:
            j = 3
            while j > -1:
                if game[i][j] == 0:
                    j -= 1
                elif j > 0 and game[i][j] == game[i][j-1]:
                    temp[i][negHorIndex(temp,i)] = game[i][j]*2
                    score += game[i][j]*2
                    j -= 2
                elif j > 1 and game[i][j] == game[i][j-2] and game[i][j-1] == 0 :
                    temp[i][negHorIndex(temp,i)] = game[i][j]*2
                    score += game[i][j]*2
                    j -= 3
                elif j > 2 and game[i][j] == game[i][j-3] and game[i][j-1] == 0 and game[i][j-2] == 0:
                    temp[i][negHorIndex(temp,i)] = game[i][j]*2
                    score += game[i][j]*2
                    j -= 4
                else:
                    temp[i][negHorIndex(temp,i)] = game[i][j]
                    j -= 1
            i -= 1
        game = temp
    elif direction == "down":
        j = 3
        while j > -1:
            i = 3
            while i > -1:
                if game[i][j] == 0:
                    i -= 1
                    continue
                elif i != 0 and game[i][j] == game[i-1][j]:
                    temp[negVertIndex(temp,j)][j] = game[i][j]*2
                    score += game[i][j]*2
                    i -= 2
                elif i > 1 and game[i][j] == game[i-2][j] and game[i-1][j] == 0 :
                    temp[negVertIndex(temp,j)][j] = game[i][j]*2
                    score += game[i][j]*2
                    i -= 3
                elif i > 2 and game[i][j] == game[i-3][j] and game[i-1][j] == 0 and game[i-2][j] == 0:
                    temp[negVertIndex(temp,j)][j] = game[i][j]*2
                    score += game[i][j]*2
                    i -= 4
                else:
                    temp[negVertIndex(temp,j)][j] = game[i][j]
                    i -= 1
            j -= 1
        game = temp
    return score,game
def vertIndex(ar,index):
    if ar[0][index] == 0:
        return 0
    if ar[1][index] == 0:
        return 1
    if ar[2][index] == 0:
        return 2
    if ar[3][index] == 0:
        return 3

def negVertIndex(ar,index):
    if ar[3][index] == 0:
        return 3
    if ar[2][index] == 0:
        return 2
    if ar[1][index] == 0:
        return 1
    if ar[0][index] == 0:
        return 0
def negHorIndex(ar,index):
    if ar[index][3] == 0:
        return 3
    if ar[index][2] == 0:
        return 2
    if ar[index][1] == 0:
        return 1
    if ar[index][0] == 0:
        return 0

def addRandom(game):
    zeros = []
    for i in range(len(game)):
        for j in range(len(game[i])):
            if game[i][j] == 0:
                zeros.append((i,j))
    if len(zeros) == 0:
        print("game over")
        return game
    else:
        index = random.choice(zeros)
        game[index[0]][index[1]] = 1
        return game
def getColor(num):
    if num == "":
        return "#9F9F9F"
    else:
        decimal = 32 + 200/(1+2**(-int(num)))
        h = hex(int(decimal))
        return "#9F9F" + h[2:]
def init():
    game = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    i = random.randint(0,3)
    j = random.randint(0,3)
    game[i][j] = 1
    return game
def play():
    score = 0
    game = init()
    sg.theme("light green 6")
    layout = []
    font = ("Arial",30)
    for i in range(len(game)):
        add = []
        for j in range(len(game[i])):
            if game[i][j] == 0:
                name = ""
            else:
                name = str(game[i][j])
            
            add.append(sg.Button(name, size = (3,3),key = (i,j),font = font,disabled = True,button_color = ("white", getColor(name)) ))
        layout.append(add)

    window = sg.Window("2048",layout, return_keyboard_events = True)

    while True:
        event, value = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        newGame = game
        print(score)
        if(event == "w"):
            score,newGame = move("up",game,score)
        elif(event == "a"):
            score,newGame = move("left",game,score)
        elif(event == "s"):
            score,newGame = move("down",game,score)
        elif(event == "d"):
            score,newGame = move("right",game,score)
        if game != newGame:
            game = addRandom(newGame)
        for i in range(len(game)):
            for j in range(len(game[i])):
                if game[i][j] == 0:
                    name = ""
                else:
                    name = str(game[i][j])
                window[(i,j)].update(name)
                window[(i,j)].update(button_color = ("white",getColor(name)))

