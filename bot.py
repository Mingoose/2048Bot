#idea: each generation 30 ppl
#take best 3 of each generation
#modify a number by some factor, 50/generation
#16 inputs
#4 * 4 + 8 * 3 + 2 * 4
#16 + 24 + 8 = 48
#3 layers of 16
#4 outputs
import math
import random
import game as game
import PySimpleGUI as sg
import time
import copy
weightsLayer1 = []
nodes1 = [] #16
weightsLayer2 = []
nodes2 = [] #16
weightsLayer3 = []
nodes3 = [] #16
weightsLayer4 = []
outputs = [] # 0 = up, 1 = left, 2 = down, 3 = right
class Bot:
    def __init__(self):
        self.weightsLayer1 = []
        self.nodes1 = [] #16
        self.weightsLayer2 = []
        self.nodes2 = [] #16
        self.weightsLayer3 = []
        self.nodes3 = [] #16
        self.weightsLayer4 = []
        for i in range(16):
            w1 = []
            w2 = []
            w3 = []
            self.nodes1.append(random.uniform(-2048,2048))
            self.nodes2.append(random.uniform(-2048,2048))
            self.nodes3.append(random.uniform(-2048,2048))
            for j in range(16):
                w1.append(random.uniform(-1,1))
                w2.append(random.uniform(-1,1))
                w3.append(random.uniform(-1,1))
            self.weightsLayer1.append(w1)
            self.weightsLayer2.append(w2)
            self.weightsLayer3.append(w3)
        for i in range(4):
            w4 = []
            for j in range(16):
                w4.append(random.uniform(-1,1))
            self.weightsLayer4.append(w4)
    def getColor(self,num):
        if num == "":
            return "#9F9F9F"
        else:
            decimal = 32 + 200/(1+2**(-int(num)))
            h = hex(int(decimal))
            return "#9F9F" + h[2:]
    def run(self,display):
        score = 0
        inputs = game.init()
        if display:
            sg.theme("light green 6")
            layout = []
            font = ("Arial",20)
            for i in range(len(inputs)):
                add = []
                for j in range(len(inputs[i])):
                    if inputs[i][j] == 0:
                        name = ""
                    else:
                        name = str(inputs[i][j])
                
                    add.append(sg.Button(name, size = (3,3),key = (i,j),font = font,disabled = True,button_color = ("white", self.getColor(name)) ))
                layout.append(add)
            window = sg.Window("2048",layout, return_keyboard_events = True)
            event, value = window.read()
        while True:
            moves = self.calculate(inputs)
            moves = [["up",moves[0]],["left",moves[1]],["down",moves[2]],["right",moves[3]]]
            moves.sort(key = lambda x: x[1])
            moved = False
            for move in moves:
                s,g = game.move(move[0],inputs,score)
                if g != inputs:
                    score = s
                    inputs = game.addRandom(g)
                    moved = True
                    break
            if display:

                if event == sg.WINDOW_CLOSED:
                    break
                for i in range(len(inputs)):
                    for j in range(len(inputs[i])):
                        if inputs[i][j] == 0:
                            name = ""
                        else:
                            name = str(inputs[i][j])
                        window[(i,j)].update(name)
                        window[(i,j)].update(button_color = ("white",self.getColor(name)))
                window.refresh()
            if moved == False:
                break
        return score
    def calculate(self,inputs): #given a game state, return the move that we should make
        #get state
        oneDInputs = []
        outputs = [0,0,0,0]
        for i in inputs:
            for j in i:
                oneDInputs.append(j)
        for i in range(len(self.nodes1)):
            for j in range(len(self.weightsLayer1[i])):
                self.nodes1[i] += self.weightsLayer1[i][j] * oneDInputs[j]
            self.nodes1[i] = self.sigmoid(self.nodes1[i])
        for i in range(len(self.nodes2)):
            for j in range(len(self.weightsLayer2[i])):
                self.nodes2[i] += self.weightsLayer2[i][j] * self.nodes1[j]
            self.nodes2[i] = self.sigmoid(self.nodes2[i])
        for i in range(len(self.nodes3)):
            for j in range(len(self.weightsLayer3[i])):
                self.nodes3[i] += self.weightsLayer3[i][j] * self.nodes2[j]
            self.nodes3[i] = self.sigmoid(self.nodes3[i])
        for i in range(len(outputs)):
            for j in range(len(self.weightsLayer4[i])):
                outputs[i] += self.weightsLayer4[i][j] * self.nodes3[j]
            outputs[i] = self.sigmoid(outputs[i])
        return outputs
                        #figure out the valid move stuff
        return game(move) # get score from game
    def sigmoid(self,num):
        try:
            return 1/(1+math.exp(-num))
        except:
            return 0
    def mutate(self,gen,total): #given the generation and total number of bots you want to create and bot to mutate, return list of old bot and mutated bots
        out = [self]
        for i in range(total):
            factor = .5/gen**(1/10)
            bot2 = copy.deepcopy(self)
            for j in range(len(bot2.nodes1)):
                bot2.nodes1[j] = self.findNew(-2048,2048,factor,bot2.nodes1[j])
                bot2.nodes2[j] = self.findNew(-2048,2048,factor,bot2.nodes2[j])
                bot2.nodes3[j] = self.findNew(-2048,2048,factor,bot2.nodes3[j])
            for j in range(len(bot2.weightsLayer1)):
                for k in range(len(bot2.weightsLayer1[j])):
                    bot2.weightsLayer1[j][k] = self.findNew(-1,1,factor,bot2.weightsLayer1[j][k])
                    bot2.weightsLayer2[j][k] = self.findNew(-1,1,factor,bot2.weightsLayer2[j][k])
                    bot2.weightsLayer3[j][k] = self.findNew(-1,1,factor,bot2.weightsLayer3[j][k])
            for j in range(len(bot2.weightsLayer4)):
                for k in range(len(bot2.weightsLayer4[j])):
                    bot2.weightsLayer4[j][k] = self.findNew(-1,1,factor,bot2.weightsLayer4[j][k])
            out.append(bot2)
        return out
    def findNew(self, lower, upper, factor, value):
        lower = max(lower,value - factor*value)
        upper = min(upper,value + factor*value)
        return random.uniform(lower,upper)
            
        
#bot1 = Bot()
#bot1.run(True)
        
