#!/usr/bin/python3
import utility
import cv2
import PIL
import numpy
import os

###init stuff
relSymbolsPath = "../images/symbols"
absSymbolsPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),relSymbolsPath)
cardSymbols = ['0','1','2','3','4','5','6','7','8','9','J','Q','K','A','10','symbol']
###
###cv2 image

def dist(sample,extract,bstDist):
    ans = 0
    for lin in range(0,len(sample)):
        for col in range(0,len(sample[lin])):
            ans = ans + abs(int(sample[lin][col][0]) - int(extract[lin][col][0]))
            if ans >= bstDist:
                return bstDist + 1; 
    return ans

def getCards(image):
    cards = []

    thresh = cv2.inRange(image,(109,109,109),(255,255,255))
    thresh_rgb = cv2.cvtColor(thresh,cv2.COLOR_GRAY2RGB)
    contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    digits_contours = []

    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if 5 <= w and w <= 25 and 15 <= h and h <= 25:
            digits_contours.append(c)

    extracts = []
    for c in digits_contours:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = numpy.int0(box)
        center,size,theta = rect
        center,size = tuple(map(int,center)),tuple(map(int,size))
        if theta < 0 and 90 + theta < -theta:
            theta = 90 + theta
        M = cv2.getRotationMatrix2D( center, theta, 1)
        extract = cv2.warpAffine(thresh_rgb, M, (int(1.4 * image.shape[0]),int(1.4 * image.shape[1])))
        extract = cv2.getRectSubPix(extract, size, center);
        extract = cv2.resize(extract,(30,30))
        extracts.append(extract)
    
    for x in range(0,len(extracts)):
        extract = extracts[x]
        bstDist = 1e9
        bstSymbol = -1
        for symbol in cardSymbols:
            sampleFilePath = os.path.join(absSymbolsPath,str(symbol))
            for filename in os.listdir(sampleFilePath):
                if not (filename.endswith(".png")):
                    continue
                filepath = os.path.join(sampleFilePath,filename)
                sample = cv2.imread(filepath,cv2.IMREAD_COLOR)
                tmpDist = dist(sample,extract,bstDist)
                if(tmpDist < bstDist):
                    bstDist = tmpDist;
                    bstSymbol = symbol
        if bstSymbol == 'symbol':
            continue
        elif bstSymbol == "0":#0's and 1's usually come together, and I think that 0 is more reliable
            cards.append('10')
        elif bstSymbol != "1":
            cards.append(bstSymbol) 


    return cards;
            
