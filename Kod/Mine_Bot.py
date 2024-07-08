# -*- coding: utf-8 -*-
import pyautogui
import os
import pygetwindow
import time
import numpy

# 0 = beginner | 1 = intermediate | 2 = expert
gamemode = 1

def startSweeper():
    os.getcwd()
    os.startfile(os.getcwd() + "\MinesweeperX.exe")
    time.sleep(1)
    y = pygetwindow.getWindowsWithTitle("Minesweeper X")[0]
    time.sleep(1)
    y.moveTo(0, 0)

if(gamemode == 0):
    startSweeper()
    xCount = 8
    yCount = 8
    bombCount = 10
    pyautogui.click(35,40)
    pyautogui.click(70,90)
    time.sleep(0.1)
elif(gamemode == 1):
    startSweeper()
    xCount = 16
    yCount = 16
    bombCount = 40
    pyautogui.click(35,40)
    pyautogui.click(70,110)
    time.sleep(0.1)
elif(gamemode == 2):
    startSweeper()
    xCount = 16
    yCount = 30
    bombCount = 99
    pyautogui.click(35,40)
    pyautogui.click(70,130)
    time.sleep(0.1)
    
xStart = 22
yStart = 109
squareSize = 16
gameFinished = False
gameWon = False
deathCounter = 0
winCounter = 0
bombsFound = 0
limit = bombCount/(xCount*yCount)
doneLimit = False

blocks = numpy.zeros([xCount,yCount], dtype = int)
bombPercentage = numpy.zeros([xCount,yCount], dtype = float)
finished = numpy.zeros([xCount,yCount], dtype = bool)
checkedNines = numpy.zeros([xCount,yCount], dtype = bool)

def minesweeper(): 
    global gameFinished, blocks, bombPercentage, finished, checkedNines, deathCounter, winCounter, gameWon, bombsFound, limit, doneLimit
    while((winCounter + deathCounter) < 50):
        blocks[0,0] = click(0,0)
        if(blocks[0,0] == 9):
            checkNines()
        while True:
            if(gameFinished == True):
                break
            goThroughNumbers()
            clickLowestPercentage()
            pass
        if(not gameWon):
            if(yCount == 8):
                pyautogui.click(72, 74)
            elif(yCount == 16):
                pyautogui.click(136, 74)
            elif(yCount == 30):
                pyautogui.click(248, 74)
            deathCounter += 1
            
            
        elif (gameWon):
            if(yCount == 8):
                pyautogui.click(72, 74)
            elif(yCount == 16):
                pyautogui.click(136, 74)
            elif(yCount == 30):
                pyautogui.click(248, 74) 
            winCounter += 1
        
        blocks = numpy.zeros([xCount,yCount], dtype = int)
        bombPercentage = numpy.zeros([xCount,yCount], dtype = float)
        finished = numpy.zeros([xCount,yCount], dtype = bool)
        checkedNines = numpy.zeros([xCount,yCount], dtype = bool)
        
        print("Game " + str(winCounter+deathCounter))
        if(deathCounter == 0):
            print(1)
        else:    
            print(str(((float)(winCounter/(winCounter+deathCounter))) * 100) + "%")
        gameFinished = False
        gameWon = False
        bombsFound = 0
        limit = bombCount/(xCount*yCount)
        doneLimit = False
        time.sleep(0.1)

    
def click(y,x):
    pyautogui.click(xStart+squareSize*x,yStart+squareSize*y)
    r,g,b = pyautogui.pixel(xStart+squareSize*x,yStart+squareSize*y)
    
    checkIfDeadOrWin(xCount)
    
    if r == 0 and g == 0 and b == 255:
        return 1
    elif r == 0 and g == 128 and b == 0:
        return 2
    elif r == 255 and g == 0 and b == 0:
        return 3
    elif r == 0 and g == 0 and b == 128:
        return 4
    elif r == 128 and g == 0 and b == 0:
        return 5
    elif r == 0 and g == 128 and b == 128:
        return 6
    elif r == 0 and g == 0 and b == 0:
        return 7
    elif r == 128 and g == 128 and b == 128:
        return 8
    elif r == 192:
        checkNines()
        return 9

def checkWholeBoard():
    for x in range(0, xCount):
        for y in range(0, yCount): 
            if(blocks[y,x] == 0):
                blocks[y,x] = checkPixel(x,y)
            pass
        pass

def checkPixel(x,y):
    r,g,b = pyautogui.pixel(xStart+squareSize*x, yStart+squareSize*y)

    if r == 0 and g == 0 and b == 255:
        return 1
    elif r == 0 and g == 128 and b == 0:
        return 2
    elif r == 255 and g == 0 and b == 0:
        return 3
    elif r == 0 and g == 0 and b == 128:
        return 4
    elif r == 128 and g == 0 and b == 0:
        return 5
    elif r == 0 and g == 128 and b == 128:
        return 6
    elif r == 0 and g == 0 and b == 0:
        return 7
    elif r == 128 and g == 128 and b == 128:
        return 8
    elif r == 192 and g == 192 and b == 192:
        r,g,b = pyautogui.pixel(xStart+squareSize*x-7, yStart+squareSize*y-7)
        if r == 255 and g == 255 and b == 255:
            return 0
        else:
            return 9    
    
def checkNines():
    rerun = False
    for x in range(0, xCount):
        for y in range(0, yCount): 
            if(blocks[x,y] == 9):
                if(checkedNines[x,y] == False):
                    for xk in range(0, 3):
                        for yk in range(0, 3):
                            try:
                                if (x + xk - 1) >= 0 and (x + xk - 1) < xCount and (y + yk - 1) >= 0 and (x + xk - 1) < yCount:
                                    if blocks[x + xk - 1, y + yk - 1] == 0:
                                        pixelNum = checkPixel(y + yk - 1,x + xk - 1)
                                        blocks[x + xk - 1, y + yk - 1] = pixelNum
                                        if pixelNum == 9:
                                            rerun = True
                            except:
                                pass
                            pass
                        pass
                    checkedNines[x,y] = True
            pass
        pass
    if rerun:
        checkNines()
        

def findEmptyAroundSquare(x,y):
    counterSquares = counterBombs = 0
    if(blocks[x,y] != 0 and blocks[x,y] != -1 and blocks[x,y] != 9):
        for xk in range(0, 3):
            for yk in range(0, 3):
                try:
                    if (x + xk - 1) >= 0 and (x + xk - 1) < xCount and (y + yk - 1) >= 0 and (x + xk - 1) < yCount:
                        if blocks[x + xk - 1, y + yk - 1] == -1:
                            counterSquares += 1
                            counterBombs += 1
                        elif blocks[x + xk - 1, y + yk - 1] == 0:
                            counterSquares += 1
                except:
                    pass
                pass
            pass
    return counterSquares, counterBombs

def goThroughNumbers():
    
    for x in range(0, xCount):
        for y in range(0, yCount): 
            if(blocks[x,y] != 0 and blocks[x,y] != -1 and blocks[x,y] != 9):
                
                if(finished[x,y] == True):
                    pass
                
                emptyAround,bombsAround = findEmptyAroundSquare(x, y)
                
                if(blocks[x,y] == bombsAround):
                    finished[x,y] = True

                chance = (((blocks[x,y]-bombsAround) / blocks[x,y])/emptyAround) * blocks[x,y]
             
                for xk in range(0, 3):
                    for yk in range(0, 3):
                        try:
                            if (x + xk - 1) >= 0 and (x + xk - 1) < xCount and (y + yk - 1) >= 0 and (x + xk - 1) < yCount:
                                if blocks[x + xk - 1, y + yk - 1] == 0:
                                    if(blocks[x,y] == emptyAround):
                                        blocks[x + xk - 1, y + yk - 1] = -1
                                        bombPercentage[x + xk - 1, y + yk - 1] = 1
                                        global bombsFound
                                        bombsFound += 1
                                    elif(chance != 0):
                                        if(round(chance,2) > bombPercentage[x + xk - 1, y + yk - 1]):
                                            bombPercentage[x + xk - 1, y + yk - 1] = round(chance,2)
                                    else:
                                        bombPercentage[x + xk - 1, y + yk - 1] = 0
                                        clickNum = click(x + xk - 1, y + yk - 1)
                                        blocks[x + xk - 1, y + yk - 1] = clickNum
                                        if clickNum == 9:
                                            checkNines()
                                        goThroughNumbers()
                        except:
                            pass       
                        pass
                    pass
            pass
        pass


def clickLowestPercentage():
    global limit, doneLimit
    lowestX = lowestY = -1
    lowestNum = 1
    goThroughNumbers()
    for x in range(0, xCount):
        for y in range(0, yCount):
            if bombPercentage[x,y] > 0 and bombPercentage[x,y] < lowestNum:
                lowestNum = bombPercentage[x,y]
                lowestX = x
                lowestY = y
            pass
        pass
    if(not doneLimit):
        emptyCount = 0
        for x in range(0, xCount):
            for y in range(0, yCount):
                if blocks[x,y] == 0:
                    emptyCount += 1
                pass
            pass
        if(emptyCount != 0):
            limit = (bombCount-bombsFound)/emptyCount
    
    if(blocks[lowestX,lowestY] == 0 and lowestNum < limit):
        clickNum = click(lowestX,lowestY)
        blocks[lowestX,lowestY] = clickNum
        if clickNum == 9:
            checkNines()
        bombPercentage[lowestX,lowestY] = 0
        
    elif(lowestNum == 1):
        done = False
        for x in range(0, xCount):
            for y in range(0, yCount):
                if blocks[x,y] == 0:
                    done = True
                    blocks[x,y] = click(y, x)
                if(done): 
                    break
                pass
            if(done): 
                break
            pass
        if(not done):
            click(yCount-1, xCount-1)
            for x in range(0, xCount):
                for y in range(0, yCount):
                    if(blocks[x,y] == 0):
                        blocks[x,y] = click(x,y)
                    pass
                pass
        
    elif(limit == 0.5 and lowestNum == 0.5):
        for x in range(0, xCount):
            for y in range(0, yCount):
                if blocks[x,y] == 0:
                    clickNum = click(x,y)
                    blocks[x,y] = clickNum
                    if clickNum == 9:
                        checkNines()
                    bombPercentage[x,y] = 0
                pass
            pass
        
    elif(lowestNum >= limit):
        for x in range(0, xCount):
            for y in range(0, yCount):
                if(blocks[x,y] == 0 and bombPercentage[x,y] == 0):
                    clickNum = click(x,y)
                    blocks[x,y] = clickNum
                    if clickNum == 9:
                        checkNines()
                    bombPercentage[x,y] = 0
                    doneLimit = True
                if(doneLimit): 
                    break
                pass
            if(doneLimit): 
                break
            pass
        if(doneLimit):
            limit += 0.05
        
    else:
        bombPercentage[lowestX,lowestY] = 0
        checkIfDeadOrWin(xCount)
        if(gameFinished == False):
            clickLowestPercentage()

def checkIfDeadOrWin(xCount):
    global gameFinished, gameWon
    if(yCount == 8):
        r,g,b = pyautogui.pixel(80, 76)
    elif(yCount == 16):
        r,g,b = pyautogui.pixel(142, 76)
    elif(yCount == 30):
        r,g,b = pyautogui.pixel(255, 76)
    if(yCount == 8):
        r1,g1,b1 = pyautogui.pixel(72, 74)
    elif(yCount == 16):
        r1,g1,b1 = pyautogui.pixel(136, 74)
    elif(yCount == 30):
        r1,g1,b1 = pyautogui.pixel(248, 74)
    if r == 0:
        gameFinished = True
    if r1 == 0:
        gameFinished = True
        gameWon = True
        
 
minesweeper()