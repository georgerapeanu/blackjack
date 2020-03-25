import os
import time
import pyscreenshot as imageGrab
from autopilot.input import Mouse

### config and init stuff

mouse = Mouse.create()

playButton = (345, 450)

newGameButton = (369, 451)
lastGameButton = (441, 450)

settingsButton = (402, 450)
settingsBackButton = (208, 246)

firstDeckOption = (374, 293)
deckOptionDelta = (45,0)

deckCounts = [1,2,4,6,8]
deckPositions = []
for i in range(0,len(deckCounts)):
    deckPositions.append((firstDeckOption[0] + deckOptionDelta[0] * i,firstDeckOption[1] + deckOptionDelta[1] * i))


dealer17Option = (370, 338)
insuranceOption = (379, 382)
autoAdviceOption = (364, 439)
autoLastBetOption = (373, 486)

betValues = [1,10,100,500]
betPositions = [(210, 399), (208, 463), (255, 503), (307, 513)]

dealButton = (335, 437)
hitButton = (334, 440)
standButton = (523, 439)
doubleButton = (240, 276)
insureButton = (470, 422)
splitButton = (387, 425)

mainHand = (256,300,393,406)
sideHand = (399,487,517,570)
dealerHand = (440,294,583,423)
gameBox = (192,170,613,576)

centerButton = (406,376)

closeAddButton = (576, 203)

waitTime = 0.3

### end of config and init
    
def screenGrab():
    im = imageGrab.grab()
    return im

def gameGrab():
    im = imageGrab.grab(gameBox)
    return im

def mainHandGrab():
    im = imageGrab.grab(mainHand)
    return im

def sideHandGrab():
    im = imageGrab.grab(sideHand)
    return im

def dealerHandGrab():
    im = imageGrab.grab(dealerHand)
    return im

def getCursorPosition():
    return (mouse.x,mouse.y)

def moveCursor(p):
    mouse.move(p[0],p[1])

def mouseClick():
    mouse.click()

def clickButton(p):
    moveCursor(p)
    mouseClick()
    time.sleep(waitTime)

def playNewGame():
    clickButton(playButton)
    clickButton(newGameButton)
    print("Started new game")

def playLastGame():
    clickButton(playButton)
    clickButton(lastGameButton)
    print("Continues last game")

def mainMenuSettings():
    clickButton(settingsButton)
    print("Opened settings")

def backSettings():
    clickButton(settingsBackButton)
    print("closed settings")

def selectDeckCount(x):
    for i in range(0,len(deckCounts)):
        if(deckCounts[i] == x):
            mainMenuSettings()
            clickButton(deckPositions[i]);
            backSettings();
            print("selected " + str(x) + " decks")
            x = int(x)
            return ;
    print("invalid bet option")

def toggleDealer17Option():
    mainMenuSettings()
    clickButton(dealer17Option)
    backSettings()
    print("toggled dealer 17 option")

def toggleInsuranceOption():
    mainMenuSettings()
    clickButton(insuranceOption)
    backSettings()
    print("toggled insurance option")

def toggleAutoAdviceOption():
    mainMenuSettings()
    clickButton(autoAdviceOption)
    backSettings()
    print("toggled auto advice option")

def toggleAutoLastBetOption():
    mainMenuSettings()
    clickButton(autoLastBetOption)
    backSettings()
    print("toggled auto last bet option");

def bet(X):
    tmp_X = int(X);
    for i in range(len(betValues) - 1,-1,-1):
        while X >= betValues[i]:
            clickButton(betPositions[i])
            X -= betValues[i]
    print("betted " + str(tmp_X))

def hit():
    clickButton(hitButton)
    print("hit")

def stand():
    clickButton(standButton)
    print("standed")

def split():
    clickButton(splitButton)
    print("splited")

def insure():
    clickButton(insureButton)
    print("insured")

def double():
    clickButton(doubleButton)
    print("doubled")

def deal():
    clickButton(dealButton)
    print("dealt cards")

def continueGame():
    clickButton(centerButton)
    print("continued")

def closeAdd():
    clickButton(closeAddButton)
    print("closed the add")
