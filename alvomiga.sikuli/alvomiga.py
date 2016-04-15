from java.awt import Robot
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
            Region(681,514,62,73).click()
    
    elif style == 'even':
        for i in range (getBetLevel(stepBet)):
            Region(960,685,64,73).click()

    elif style == 'high':
        for i in range (getBetLevel(stepBet)):
            Region(599,466,64,69).click()
            
    elif style == 'low':
        for i in range (getBetLevel(stepBet)):
            Region(1055,751,74,76).click()

    elif style == 'red':
        for i in range (getBetLevel(stepBet)):
            Region(859,636,66,53).click()
            
    elif style == 'black':
        for i in range (getBetLevel(stepBet)):
            Region(769,581,63,50).click()
            
    Region(705,799,109,108).click()
    time.sleep(1)
            
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
    elif style == 'red':
        expectedText = ['red']  
    elif style == 'black':
        expectedText = ['black']  
        
    counter = 0
    for i in expectedText:
        if i in textFromSpin:
            counter += 1

    return counter

def checkTextAndColorFromSpin():
    Region(717,828,95,90).click()
    time.sleep(1)
    textFromSpin = Region(435,754,73,24).text()
    colorRegion = find("1460730720660.png")
    colorPattern = colorRegion.getTopLeft().offset(5,5)
    robot = Robot()
    colorRobot = robot.getPixelColor(colorPattern.x, colorPattern.y)
    color = ( colorRobot.getRed())
    if color == 173:
        colorRed = 'red'
        textFromSpin = textFromSpin + colorRed
        return textFromSpin
    elif color == 31:
        colorBlack = 'black'
        textFromSpin = textFromSpin + colorBlack
        return textFromSpin
    else: 
        return textFromSpin
    
def waitForRow(expectedInRow, maxToleranceTime, startTime):
    
    evenInRow = 0
    oddInRow = 0
    lowInRow = 0
    highInRow = 0
    redInRow = 0
    blackInRow = 0
    
    counter = 0
    
    while evenInRow != expectedInRow and oddInRow != expectedInRow and lowInRow != expectedInRow and highInRow != expectedInRow and redInRow != expectedInRow and blackInRow != expectedInRow:
        
        textAndColorFromSpin = checkTextAndColorFromSpin()

        if isElapsedTimeInTolerance(maxToleranceTime, time.time() - startTime) == False:
            closeAndStartRoulette()
            startTime = time.time()
            textAndColorFromSpin = checkTextAndColorFromSpin()
        
        if checkStyleFromSpin('even', textAndColorFromSpin) == 1:
            evenInRow += 1
        elif checkStyleFromSpin('even', textAndColorFromSpin) == 0:
            evenInRow = 0
            
        if checkStyleFromSpin('odd', textAndColorFromSpin) == 1:
            oddInRow += 1
        elif checkStyleFromSpin('odd', textAndColorFromSpin) == 0:
            oddInRow = 0

        if checkStyleFromSpin('low', textAndColorFromSpin) == 1:
            lowInRow += 1
        elif checkStyleFromSpin('low', textAndColorFromSpin) == 0:
            lowInRow = 0

        if checkStyleFromSpin('high', textAndColorFromSpin) == 1:
            highInRow += 1
        elif checkStyleFromSpin('high', textAndColorFromSpin) == 0:
            highInRow = 0

        if checkStyleFromSpin('red', textAndColorFromSpin) == 1:
            redInRow += 1
        elif checkStyleFromSpin('red', textAndColorFromSpin) == 0:
            redInRow = 0

        if checkStyleFromSpin('black', textAndColorFromSpin) == 1:
            blackInRow += 1
        elif checkStyleFromSpin('black', textAndColorFromSpin) == 0:
            blackInRow = 0
            
        counter += 1
    
    stylesResult = {'even' : evenInRow, 'odd' : oddInRow, 'low' : lowInRow, 'high' : highInRow, 'red' : redInRow, 'black' : blackInRow} 
    print stylesResult
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
