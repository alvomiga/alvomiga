import random
import time

global startTime

def isWin(): 
    if exists("1460466965057.png"):
        return True
    else:
        return False

def clearBet():
    click("1460466979161.png")
    
    
def getBetLevel(stepBet):
    if stepBet == 0:
        return 1
    elif stepBet == 1:
        return 2
    elif stepBet == 2:
        return 4
    elif stepBet == 3:
        return 8
    elif stepBet == 4:
        return 16
    #elif stepBet == 5:
        #return 32

#place bet on a opposite style after defined row
def placeBet(style, stepBet):
    
    if style == 'odd':
        for i in range (getBetLevel(stepBet)):
            Region(691,565,76,78).click()
    
    elif style == 'even':
        for i in range (getBetLevel(stepBet)):
            Region(924,722,88,77).click()

    elif style == 'high':
        for i in range (getBetLevel(stepBet)):
            Region(605,529,91,64).click()
            
    elif style == 'low':
        for i in range (getBetLevel(stepBet)):
            Region(1030,790,72,63).click()
            
    Region(729,828,79,84).click()
    time.sleep(1)

def doFreeSpin():
    Region(729,828,79,84).click()
    time.sleep(1)
    
def doFreeSpinAndGetText():
    Region(717,828,95,90).click()
    time.sleep(1)
    return Region(429,813,87,27).text()
            
def checkStyleFromSpin(style, textFromSpin):
    textFromSpin = textFromSpin.lower()
    
    if style == 'odd':
        expectedText = ['odd']
    elif style == 'even':
        expectedText = ['even', 'evan']
    elif style == 'low':
        expectedText = ['low', 'law']
    elif style == 'high':
        expectedText = ['high']  

    counter = 0
    for i in expectedText:
        if i in textFromSpin:
            counter += 1

    return counter

def waitForRow(expectedInRow, maxToleranceTime, startTime):
    
    evenInRow = 0
    oddInRow = 0
    lowInRow = 0
    highInRow = 0
    
    counter = 0
    
    while evenInRow != expectedInRow and oddInRow != expectedInRow and lowInRow != expectedInRow and highInRow != expectedInRow:
        
        textFromSpin = doFreeSpinAndGetText()
        print startTime
        print time.time() - startTime
        
        if isElapsedTimeInTolerance(maxToleranceTime, time.time() - startTime) == False:
            closeAndStartRoulette()
            startTime = time.time()
            textFromSpin = doFreeSpinAndGetText()
        
        if checkStyleFromSpin('even', textFromSpin) == 1:
            evenInRow += 1
        elif checkStyleFromSpin('even', textFromSpin) == 0:
            evenInRow = 0
            
        if checkStyleFromSpin('odd', textFromSpin) == 1:
            oddInRow += 1
        elif checkStyleFromSpin('odd', textFromSpin) == 0:
            oddInRow = 0

        if checkStyleFromSpin('low', textFromSpin) == 1:
            lowInRow += 1
        elif checkStyleFromSpin('low', textFromSpin) == 0:
            lowInRow = 0

        if checkStyleFromSpin('high', textFromSpin) == 1:
            highInRow += 1
        elif checkStyleFromSpin('high', textFromSpin) == 0:
            highInRow = 0

        counter += 1

    stylesResult = {'even' : evenInRow, 'odd' : oddInRow, 'low' : lowInRow, 'high' : highInRow} 
    return max(stylesResult, key=stylesResult.get)

def closeAndStartRoulette():
    Region(1621,182,14,19).click()
    time.sleep(1)
    Region(304,502,167,108).click()
    time.sleep(1)
    Region(685,624,607,34).click()
    time.sleep(15)

def isElapsedTimeInTolerance(maxToleranceTime, elapsedTime):
    if elapsedTime > maxToleranceTime:
        return False
    else:
        return True

def runWaitForRowStrategy(numberInRow):        
    betLevel = 0
    numberOfWinGames = 0
    numberOfLoseGames = 0
    balance = 544
    maxToleranceTime = 1080

    startTime = time.time()
    style = waitForRow(numberInRow, maxToleranceTime, startTime)
    
    while balance > 424 and numberOfLoseGames < 2:
        if betLevel < 5:
            
            placeBet(style, betLevel)
            
            if isWin() == False:
                betLevel = betLevel + 1
            else:
                clearBet()
                betLevel = 0
                numberOfWinGames = numberOfWinGames + 1
                balance += 2
                print "number of win games: ", numberOfWinGames, "balance: ", balance, "style: ", style
                style = waitForRow(numberInRow, maxToleranceTime, startTime)
        else:
            betLevel = 0
            numberOfLoseGames = numberOfLoseGames + 1
            balance -= 62
            print "number of lose games", numberOfLoseGames, "balance: ", balance, "style: ", style
            style = waitForRow(numberInRow, maxToleranceTime, startTime)

runWaitForRowStrategy(8)
