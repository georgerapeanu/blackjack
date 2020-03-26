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

def dist(sample,extract):
    ans = 0
    for lin in range(0,len(sample)):
        for col in range(0,len(sample[lin])):
            ans = ans + abs(int(sample[lin][col][0]) - int(extract[lin][col][0]))
    return ans

def getCards(image):
    cards = {}

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
        print("new extract")
        cv2.imshow('extract',extract)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        bstsym = -1
        bst = 1e9
        for symbol in cardSymbols:
            print("symbols is " + str(symbol))
            sampleFilePath = os.path.join(absSymbolsPath,str(symbol))
            bstdist = 1e9
            for filename in os.listdir(sampleFilePath):
                if not (filename.endswith(".png")):
                    continue
                filepath = os.path.join(sampleFilePath,filename)
                sample = cv2.imread(filepath,cv2.IMREAD_COLOR)
                tmpdist = dist(sample,extract)
                if(bstdist > tmpdist):
                    bstdist = tmpdist
            print("bstdist is " + str(bstdist))
            if(bstdist < bst):
                bst = bstdist;
                bstsym = symbol
        print("i think its a " + str(bstsym) + " with dst " + str(bst))
        print("save file ?")
        if(str(input()) == "y"):
            print("what was it?")
            ans = str(input())
            print("ok so it was a " + str(ans))
            sampleFilePath = os.path.join(absSymbolsPath,str(ans))
            savePath = os.path.join(sampleFilePath,(str(len(os.listdir(sampleFilePath))) + ".png"))
            print("save as " + savePath)
            cv2.imwrite(savePath,extract)
                

#compare them with each thing
