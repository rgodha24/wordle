import json
from random import randint, choice
from numpy import mean, round_ 
from tqdm import tqdm as tqdm
import time

with open("answers.json") as answerJson:
    answers = json.load(answerJson)
    
with open("ok.json") as okJson:
    ok = json.load(okJson)
    
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

def checkWord(correctAnswer, word, ):
    if correctAnswer == word:
        return True
    
    else:
        wordLength = len(word)
        answerLetters = list(correctAnswer)
        output = ["2",'2','2','2','2']
        
        for i in range(wordLength -1, -1, -1): # (let i = wordLength - 1; i >= 0; i--) 
            if word[i] == correctAnswer[i]:
                output[i] = '0'
                answerLetters.pop(i)

        for i in range(wordLength): # (let i = 0; i < wordLength; i++) {
            if word[i] in answerLetters and output[i] != 0:
                output[i] = '1'
                answerLetters.pop(answerLetters.index(word[i]))
                
        return output

benchmarkList = []

loopNumber = int(input("how many loops do you want?"))

yellowWeight = 1
greenWeight = 50

for wordleAnswerInt in tqdm(range(loopNumber),):
    greens = [None, None, None, None, None]
    wordleAnswer = choice(answers)
    yellows = []
    greys = []
    cantBe = []
    guesses = 0
    for i in range(5):
        cantBe.append([])
    triedList = []
    
    
    
    while True:
        
        
        #finding the best word to put in
        # ranking the letters (copied from best starting word)


        # checking if greens are ok
        possibleAnswers = []
        for answerInt, answerX in enumerate(answers):
            fine = True
            for letterInt, letter in enumerate(answerX):
                if greens[letterInt] != None:
                    if greens[letterInt] != letter:
                        fine = False
                        
            if fine:
                possibleAnswers.append(answerX)
                
        # print(len(possibleAnswers))
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

            # print(len(possibleAnswers))
            
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
                    # print(len(possibleAnswers))
            
            # print(len(possibleAnswers))
            
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
        
        for i in range(5):
            for k in range(26):
                newLetterList[i][k] = int(int((letterList[0][k] + letterList[1][k] + letterList[2][k] + letterList[3][k] +letterList[4][k]) * yellowWeight/5) + letterList[i][k] * greenWeight)
            
        
        # redoing greens with just yellow
        for i, j in enumerate(greens):
            if j != None:
                for k in range(26):
                    newLetterList[i][k] = letterList[0][k] + letterList[1][k] + letterList[2][k] + letterList[3][k] + letterList[4][k] 
        
        
                    
        letterList = newLetterList.copy()

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

        # letter ranks is now a rank of the best letter for each part of the word. 
        # now we have to generate the best word to put in next with this list.
            
        if len(possibleAnswers)>5: 

            added = [0,0,0,0,0]
            bestWord = ''
            tryWord = ""
            bestAdded = 1000
            start = time.time()
            for i in (range(int(min(len(possibleAnswers)*4000, 100000)))):
                tryWord = ''
                for i in range(len(added)):
                    added[i] = randint(0,4)
                tryAdded = sum(added)    
                
                
                
                if tryAdded < bestAdded:
                    for i in range(5):
                        tryWord += letterRanks[i][added[i]]
                    if tryWord in ok:
                        if tryAdded < bestAdded:
                            bestWord = tryWord
                            bestAdded = tryAdded
                            # print("found a better word!")
                            # print(bestAdded)

            if len(bestWord) != 0:
                pass
            elif len(possibleAnswers) != 0 and len(bestWord) == 0:
                # print("pain it failed")
                bestWord = possibleAnswers[randint(0, len(possibleAnswers)-1)]
                # print(f"{bestWord} is a random one it failed tho lol sry")
                # print(greens, yellows, greys, cantBe, triedList)
                
            else:
                # print("pain it failed")
                # print(greens, yellows, greys, cantBe, triedList)
                break
            
        
        else: 
            best = 100
            bestWord = ''
            for i in (possibleAnswers):
                rankInt = 0
                
                for j, k in enumerate(i):
                    rankInt += letterRanks[j].index(k)
                    
                if rankInt < best:
                    bestWord = i
                    best = rankInt
                    
            if len(bestWord) != 0:
                pass
            else:
                # print("pain it failed")
                # print(greens, yellows, greys, cantBe, triedList)
                break
            
        guesses += 1
        
        damn = checkWord(wordleAnswer, bestWord)

        
        if damn == True:
            # print(f"got it in {guesses} guesses. average is {mean(benchmarkList)}")
            benchmarkList.append(guesses)
            break
        
        
        else:
            # print("enter what wordle gave you back.")
            triedList.append(bestWord)
            
            answerInput = damn
                
            for answerInt, answerX in enumerate(answerInput):
                if answerX == "0":
                    greens[answerInt] = bestWord[answerInt]
                    if bestWord[answerInt] in yellows:
                        yellows.pop(yellows.index(bestWord[answerInt]))
                        
                    if bestWord[answerInt] in greys:
                        greys.pop(greys.index(bestWord[answerInt]))
                        # print(f"popped {bestWord[answerInt]} out of greys")
                
                elif answerX == "1":
                    cantBe[answerInt].append(bestWord[answerInt])
                    if bestWord[answerInt] not in yellows:
                        yellows.append(bestWord[answerInt])
                        
                    if bestWord[answerInt] in greys:
                        cantBe[greys.index(bestWord[answerInt])].append(bestWord[answerInt])
                        greys.pop(greys.index(bestWord[answerInt]))
                        # print(f"popped {bestWord[answerInt]} out of yellowsn")
                        
                elif answerX == "2":
                    if bestWord[answerInt] not in greens and bestWord[answerInt] not in yellows and bestWord[answerInt] not in greys:
                        greys.append(bestWord[answerInt])
                        
                else:
                    print("youre stupid you borked it dumbass")
                        
            # print(greens, yellows, greys, cantBe, triedList)
            
print(f"{round(mean(benchmarkList), 3)} is the average number of guesses it takes with a random input of {loopNumber} answers")