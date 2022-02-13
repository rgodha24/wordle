import json
from random import randint
from numpy import mean 
from tqdm import tqdm as tqdm

with open("answers.json") as answerJson:
    answers = json.load(answerJson)
    
with open("ok.json") as okJson:
    ok = json.load(okJson)
    
with open("guesses count.json") as guessesJsonFile:
    guesses = json.load(guessesJsonFile)
    print(f"current average guesses taken is {mean(guesses)}")
    
def betterIndex(list, finding):
    outputList = []
    for i, j in enumerate(list):
        if j == finding:
            outputList.append(i)
            
    return outputList

def rank(ausdhb):
    list = ausdhb.copy()
    x = []
    y = list.copy()
    popped = []
    for i in range(len(list)):
        a = max(list)
        b = list.index(a)
        
        
        appending = None
        for j, k in enumerate(betterIndex(y, a)):
            if k not in popped:
                appending = k
        x.append(appending)
        
        
        popped.append(appending)
        list.pop(b)
    # print(popped)    
    # print(list)
    return x

def getPossibleAnswers(answers, greens, yellows, greys, cantBe, triedList):
        
    possibleAnswers = []
    # checking if greens are ok
    for answerInt, answerX in enumerate(answers):
        fine = True
        for letterInt, letter in enumerate(answerX):
            if greens[letterInt] != None:
                if greens[letterInt] != letter:
                    fine = False
                    
        if fine:
            possibleAnswers.append(answerX)
    
    # checking yellows
    if len(yellows) != 0:
        popList = []
        for answerInt, answerX in enumerate(possibleAnswers):
            a = []
            for letterInt, letterX in enumerate(answerX):
                if letterX in yellows:
                    a.append(True)
            
            if len(a) != len(yellows):
                popList.append(answerInt)
                
        for bad in reversed(popList):
            try:
                possibleAnswers.pop(bad)
            except:
                print(f"pop failed LLLLLLL {bad}. on yellows")
                
    if len(greys) != 0:
        popList = [] #indexes of bad ones
        for answerInt, answerX in enumerate(possibleAnswers):
            for letterInt, letterX in enumerate(answerX):
                if letterX in greys:
                    popList.append(answerInt)
                    break
                    
        for bad in reversed(popList):
            try:
                possibleAnswers.pop(bad)
            except:
                print(f"pop failed LLLLLLL {bad}. on greys")
                    
    if len(cantBe) != 0:
        popList = []
        for answerInt, answerX in enumerate(possibleAnswers):
            for letterInt, letterX in enumerate(answerX):
                if len(cantBe[letterInt]) != 0:
                    if letterX in cantBe[letterInt]:
                        if answerInt not in popList:
                            popList.append(answerInt)
        
        # print((popList))
        for bad in reversed(popList):
            try:
                possibleAnswers.pop(bad)
            except:
                print(f"pop failed LLLLLLL {bad}. on cant bes")
                    
    if len(triedList) != 0:
        popList = []
        for answerInt, answerX in enumerate(possibleAnswers):
            if answerX in triedList:
                popList.append(answerInt)
                
        for bad in reversed(popList):
            try:
                possibleAnswers.pop(bad)
            except:
                print(f"pop failed LLLLLLL {bad}. on tried list")
            
    return possibleAnswers

def getLetterList(possibleAnswers, yellowWeight, greenWeight):
    letterList = []
    x = []
    for q in range(26):
        x.append(0)
        
    for w in range(5):
        letterList.append(x.copy())

    for j, k in enumerate(possibleAnswers):
        for letterNumber, letter in enumerate(k):
            letterList[letterNumber][ord(letter)-97] += 1
            
    # print(letterList)

    
    newLetterList = letterList.copy()
    
    
    # redoing greens with just yellow
    for i, j in enumerate(greens):
        if j != None:
            for k in range(26):
                newLetterList[i][k] = int((letterList[i][0] + letterList[i][1] + letterList[i][2] + letterList[i][3] + letterList[i][4])*yellowWeight/5) + int(letterList[i][k]*greenWeight)
    
    
                
    return newLetterList
   
def getLetterRanks(letterList):
    ranks = []
    for i in range(5):
        ranks.append(rank(letterList[i]))
        
    letterRanks = []
    for i in ranks:
        o = []
        for j in i:
            try:
                o.append(chr(j+97))
            except:
                print("one of them failed lol awef jnaow pain")
            
        letterRanks.append(o)
        
    return letterRanks
    
def getWeights(): # returns yellowWeight, greenWeight
    with open("weights.json") as weightsJson:
        x = json.load(weightsJson)

    return x["yellowWeight"], x["greenWeight"]    

def fixDoubleLetters(word):
    wordList = list(word)
    output = 0
    for i, j in enumerate(wordList):
        if wordList.index(j) != i:
            output += .1
            
    return output

greens = [None, None, None, None, None]
yellows = []
greys = []
cantBe = []
guesses = 0
for i in range(5):
    cantBe.append([])
triedList = []
yellowWeight, greenWeight = getWeights()

while True:
   
    # possible answers is a list of all of all of the wordle answers that are possibly left, taking into account
    # greens, yellows, greys, cantBe (letters that were yellow, so cant be in that spot again), and all of the words already tried
    possibleAnswers = getPossibleAnswers(answers, greens, yellows, greys, cantBe, triedList)

    # letterList is a count of the frequency of a letter in the possible answer list. it also allows for a weighting of yellows and greens. 
    letterList = getLetterList(possibleAnswers, yellowWeight, greenWeight)

    # letter ranks is letterList, but instead of letterList[0][0] being the amount of A's in the first letter, 
    # letter ranks[0][0] is the most common first letter. 
    letterRanks = getLetterRanks(letterList)
            
        
    print(f"currently there are {len(possibleAnswers)} possible answers. finding the best one now")
    if len(possibleAnswers)>5: 

        added = [0,0,0,0,0]
        bestWord = ''
        tryWord = ""
        bestAdded = 1000
        for aaa in tqdm(range(5)):
            for bbb in range(5):
                for ccc in range(5):
                    for ddd in range(5):
                        for eee in range(5):
                            added = [aaa, bbb, ccc, ddd, eee]
                            tryWord = ''
                            tryAdded = sum(added)
                            
                            for k in range(5):
                                tryWord += letterRanks[k][added[k]]
                                
                            tryAdded += fixDoubleLetters(tryWord)
                            if tryAdded < bestAdded:
                                if tryWord in ok:
                                    if tryAdded < bestAdded:
                                        bestWord = tryWord
                                        bestAdded = tryAdded
                                        # print("found a better word!")
                                        # print(bestAdded)

        if len(bestWord) != 0:
            print(f"try {bestWord}!")
        elif len(possibleAnswers) != 0 and len(bestWord) == 0:
            print("pain it failed")
            bestWord = possibleAnswers[randint(0, len(possibleAnswers))]
            print(f"{bestWord} is a random one it failed tho lol sry")
            print(greens, yellows, greys, cantBe, triedList)
            
        else:
            print("pain it failed")
            print(greens, yellows, greys, cantBe, triedList)
            break
            
        
    else: 
        best = 100
        bestWord = ''
        for i in tqdm(possibleAnswers):
            rankInt = 0
            
            for j, k in enumerate(i):
                rankInt += letterRanks[j].index(k)
                
            if rankInt < best:
                bestWord = i
                best = rankInt
                
        if len(bestWord) != 0:
            print(f"try {bestWord}!")
        else:
            print("pain it failed")
            print(greens, yellows, greys, cantBe, triedList)
            break
    
    guesses += 1
    
    if input("was this word right? y/n: ") == "y":
        with open("guesses count.json", "r") as guessesJsonFile:
            guessesJson = json.load(guessesJsonFile)
            guessesJson.append(guesses)
        with open("guesses count.json", "w") as guessesJsonFile:
            json.dump(guessesJson, guessesJsonFile)
        break
    
    else:
        print("enter what wordle gave you back.")
        triedList.append(bestWord)
        
        answerInput = []
        for letter in bestWord:
            answerInput.append(input(f"for {letter} what color was it? 0 for green, 1 for yellow, 2 for grey: ").strip())
            
        for answerInt, answerX in enumerate(answerInput):
            if answerX == "0":
                greens[answerInt] = bestWord[answerInt]
                if bestWord[answerInt] in yellows:
                    yellows.pop(yellows.index(bestWord[answerInt]))
                    
                if bestWord[answerInt] in greys:
                    greys.pop(greys.index(bestWord[answerInt]))
                    print(f"popped {bestWord[answerInt]} out of greys")
            
            elif answerX == "1":
                cantBe[answerInt].append(bestWord[answerInt])
                if bestWord[answerInt] not in yellows:
                    yellows.append(bestWord[answerInt])
                    
                if bestWord[answerInt] in greys:
                    cantBe[greys.index(bestWord[answerInt])].append(bestWord[answerInt])
                    greys.pop(greys.index(bestWord[answerInt]))
                    print(f"popped {bestWord[answerInt]} out of yellowsn")
                    
            elif answerX == "2":
                if bestWord[answerInt] not in greens and bestWord[answerInt] not in yellows and bestWord[answerInt] not in greys:
                    greys.append(bestWord[answerInt])
                    
            else:
                print("youre stupid you borked it dumbass")
                    
        # print(greens, yellows, greys, cantBe, triedList)