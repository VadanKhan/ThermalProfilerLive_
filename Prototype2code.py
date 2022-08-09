# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import numpy as np
import matplotlib as plt
import math as m
from scipy.optimize import fsolve
import csv
import time

ser = serial.Serial('/dev/ttyACM0',115200)

#getting current timestamp
localtime = time.localtime()
strttime = time.strftime("%d-%I:%M:%S", localtime)
print(strttime)

#FILENAME EDIT HERE:
#if want to create new file then put strttime as first part
#if appending previous then input timestamp and following name
filename = strttime + ", VK first tests"
print(filename)

#FORMAT TYPE HERE (.csv or .txt)
form = ".txt"


#creating initial array, IF APPENDING PREVIOUS THEN COMMENTIFY ALL THIS
empt = np.array([0])
try:
    np.savetxt(filename + form, empt, delimiter = ',')
except Exception:
    print("error: saving initial file")

try:
    ini = np.zeros([2, 12])
    with open(filename + form, 'w') as f:
        csv.writer(f, delimiter = ',').writerows(ini)
except Exception:
    print("error: adding zeros to initial file")


while True:
    print("----------")
    read_serial=ser.readline()
    print(type(read_serial))
    print(read_serial)
   
    #change to string and eliminate \r\n
    strraw = read_serial.decode()
    strraw = strraw.rstrip()
    print(type(strraw))
    print(strraw)
   
    #splitting into list, using commas
    strraw = strraw.split(",")
    print(type(strraw))
    print(strraw)
       
    #converting to float code
   
    try:
        a = float(strraw[0])
        b = float(strraw[1])
        c = float(strraw[2])
        d = float(strraw[3])
        e = float(strraw[4])
        f = float(strraw[5])
        g = float(strraw[6])
        h = float(strraw[7])
    except Exception:
        print("error: float")
        pass
   
    #put in array
    try:
        raw = np.array([a, b, c, d, e, f, g, h])
        print(type(raw))
        print(raw)
    except Exception:
        print("error: array")
        pass
   
    #python numerical solving
    try:
        A = 34.197
        B = 28.383
        C = 26.245
        a = 1
        b = 2
        c = 3
        v = 1
       
        def eqs(x):
            k = x[0]
            Tc = x[1]
            Th = x[2]
            f = Tc + (Th - Tc)*m.exp(-k*(a/v)) - A
            g = Tc + (Th - Tc)*m.exp(-k*(b/v)) - B
            h = Tc + (Th - Tc)*m.exp(-k*(c/v)) - C
            return [f, g, h]
        guess = [1, 25, 70]
        solution = fsolve(eqs, guess)
        print("trial values solution [k, T_c, T_h]: ", solution)
    except Exception:
        print("error: numerical solving")
        pass
   
    34.197
    28.383
    26.245
   
    #calculating delta
    try:
        delta = solution[2] - raw[6]
        print("delta: ", delta)
        deltaarr = np.array([])
        deltaarr = np.append(deltaarr, delta)
        print(deltaarr)
    except Exception:
        print("error: calculating delta")
        pass
   
    #saving data to same file
    try:
        res = np.append(raw, solution)
        res = np.append(res, deltaarr)
        print(np.shape(res))
        print("results: ", res)
        out = np.genfromtxt(filename + form, dtype='float', delimiter = ',', skip_header=0)
        print(type(out))
        print("out: ", out)
        b = np.append(out, [res], axis=0)
        print("b: ", b)
    except Exception:
        print("error: array appending")
        pass
       
    try:
        with open(filename + form, 'w') as f:
            csv.writer(f, delimiter = ',').writerows(b)
    except Exception:
        print("error: array save")
        pass
   
   
    print("----------")
