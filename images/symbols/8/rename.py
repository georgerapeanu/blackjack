#!/usr/bin/python3
import numpy
import os

a = 1

for filename in os.listdir("./"):
    if (filename.endswith(".py")):
        continue
    os.rename(filename,str(a) + ".png");
    a = int(a) + 1
    
