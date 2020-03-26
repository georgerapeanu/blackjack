#!/usr/bin/python3
import utility
import cv2
import PIL
import numpy
import os

def getCards(image):
    cards = {}

    thresh = cv2.inRange(image,(109,109,109),(255,255,255))
    thresh_rgb = cv2.cvtColor(thresh,cv2.COLOR_GRAY2RGB)
    contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    processed_image = numpy.array(image)

    digits_contours = []

    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
#        cv2.rectangle(image,(x,y),(x + w,y + h),(0,255,0),1)
        if 5 <= w and w <= 25 and 15 <= h and h <= 25:
            digits_contours.append(c)

    cv2.drawContours(image,contours,-1,(0,255,0),1)

    extracts = []
    for c in digits_contours:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect);
        box = numpy.int0(box)
        center,size,theta = rect
        center,size = tuple(map(int,center)),tuple(map(int,size))
        print(rect)
        if theta < 0 and 90 + theta < -theta:
            theta = 90 + theta
        M = cv2.getRotationMatrix2D( center, theta, 1)
        extract = cv2.warpAffine(thresh_rgb, M, (int(1.4 * image.shape[0]),int(1.4 * image.shape[1])))
        extract = cv2.getRectSubPix(extract, size, center);
        extract = cv2.resize(extract,(30,30))
        extracts.append(extract)
        cv2.drawContours(processed_image, [box], 0, (0,255,0), 1)
    
    final_image = numpy.hstack((image,thresh_rgb,processed_image))
    
    cv2.imshow('final',final_image)
    cv2.waitKey()
    #cv2.imwrite(filename + "_mask.png",final_image)
    
    final_extracts = numpy.hstack(tuple(extracts))
    
    cv2.imshow('symbols',final_extracts)
    cv2.waitKey()
    #cv2.imwrite(im + "_symbols.png",final_extracts)

#    for x in range(0,len(extracts)):
#        cv2.imshow("symbol.png",extracts[x])
#        cv2.waitKey()
