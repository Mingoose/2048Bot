import bot
def main():
    bots = []
    for i in range(30):
        bots.append(bot.Bot())
    generation = 1
    while generation < 100:
        scores = []
        for b in bots: 
            scores.append(b.run(False))
        bestThree = sorted(zip(scores,bots), key = lambda x : x[0], reverse = True)[:3]
        bots = []
        for b in bestThree:
            bots += b[1].mutate(generation,9)
        print(max(scores))
        generation += 1
    bots[0].run(True)

            
main()
