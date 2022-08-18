import serial
import numpy as np
import matplotlib as plt
import math as m
from scipy.optimize import fsolve
import csv
import time

try:
    ser = serial.Serial('/dev/ttyACM0',115200)
except Exception:
    print("serial didnt work")
    pass

#getting current timestamp
localtime = time.localtime()
strttime = time.strftime("%d-%I:%M:%S", localtime)
print(strttime)

inx = 0
#%%
#FILENAME EDIT HERE:
#if want to create new file then put strttime as first part
#if appending previous then input timestamp and following name
filename = strttime + ", VK second tests"
print(filename)
filenameavg = filename + "avg"

#FORMAT TYPE HERE (.csv or .txt)
form = ".txt"

#EXPERIMENT CONDITIONS HERE
a = 0.15
b = 0.3
c = 0.45
d = 0.6
e = 0.75
f = 0.88
v = 10/60
#position of validation sensor temperature from arduino code
valdpos = 12

#INPUT DEFAULT GUESS HERE, Th = guess1, Tc = guess2, k = guess3
guess1 = 50
guess2 = 25
guess3 = 0.01
solution = np.array([guess1, guess2, guess3])
mastguess = np.array([guess1, guess2, guess3])

#INPUT MAXIMUM AND MINIMUM PREDICTION TEMPERATURES YOU ARE WILLING TO ACCEPT, AND MAXIMUM JUMP IN TEMPERATURE
lbnd = 20
upbnd = 70
maxjump = 5
#%%
#creating initial array, IF APPENDING PREVIOUS THEN COMMENTIFY ALL THIS
empt = np.empty(0)
results = np.empty(0)

try:
    np.savetxt(filename + form, empt, delimiter = ',')
except Exception:
    print("error: saving initial file")

try:
    np.savetxt(filenameavg + form, empt, delimiter = ',')
except Exception:
    print("error: saving initial avg file")

reset = False
#%%
while True: 
    print("----------")
    try: 
        read_serial=ser.readline()
        #print(type(read_serial))
        #print(read_serial)
        
        #change to string and eliminate \r\n
        strraw = read_serial.decode()
        strraw = strraw.rstrip()
        #print(type(strraw))
        #print(strraw)
        
        #splitting into list, using commas
        strraw = strraw.split(",")
        #print(type(strraw))
        #print(strraw)
    except Exception:
        print("couldn't read")
        pass
#%%
    #converting to float code
    
    try:
        raw = np.asarray(strraw, dtype = np.float64, order ='C')
        #print(type(raw))
        #print(raw)
    except Exception:
        print("error: array floatifying")
        pass
    
    #choose which temp indicates what
    try:
        A = raw[0]
        B = raw[1]
        C = raw[2]
        D = raw[3]
        E = raw[4]
        F = raw[5]
        print("A, B, C:", A, B, C)
    except Exception:
        print("error: assign temp points")
        pass
    
    #resetting crazy Tc and k values
    '''
    if solution[1] > 50 or solution[1] < 0:
        solution[1] = float(guess2)
        
    if solution[2] > 10 or solution[2] < 10:
        solution[2] = float(guess3)
    '''
#%%
    #attempt 1    
    try:
        def eqs(x):
            Th = x[0]
            Tc = x[1]
            k = x[2]
            
            f = Tc + (Th - Tc)*np.exp(-k*(a/v)) - A
            g = Tc + (Th - Tc)*np.exp(-k*(b/v)) - B
            h = Tc + (Th - Tc)*np.exp(-k*(c/v)) - C
            
            return [f, g, h]
        guess = solution
        #print(type(guess))
        solution = fsolve(eqs, guess)
        print("trial values solution [T_h, T_c, k]: ", solution)
        err = True
    except Exception:
        print("error: numerical solving 1")
        err = True
        pass
    
#%%
    #attempt 2, guess from previous for Th, but fixed guesses for Tc & k
    if err == True:
        try:
            def eqs(x):
                Th = x[0]
                Tc = x[1]
                k = x[2]
                f = Tc + (Th - Tc)*np.exp(-k*(a/v)) - A
                g = Tc + (Th - Tc)*np.exp(-k*(b/v)) - B
                h = Tc + (Th - Tc)*np.exp(-k*(c/v)) - C
                
                return [f, g, h]
            guess = np.array([solution[0], guess2, guess3])
            #print(type(guess))
            solution = fsolve(eqs, guess)
            print("trial values try2 solution [T_h, T_c, k]: ", solution)
            err = False
        except Exception:
            print("error: numerical solving 2")
            err = True
            pass
    else:
        pass
#%%
    #solving attempt 3, with all fixed guess values
    if err == True:
        try:
            def eqs(x):
                Th = x[0]
                Tc = x[1]
                k = x[2]
                f = Tc + (Th - Tc)*np.exp(-k*(a/v)) - A
                g = Tc + (Th - Tc)*np.exp(-k*(b/v)) - B
                h = Tc + (Th - Tc)*np.exp(-k*(c/v)) - C
                
                return [f, g, h]
            guess = np.array([guess1, guess2, guess3])
            print(type(guess))
            solution = fsolve(eqs, guess)
            print("trial values try3 solution [T_h, T_c, k]: ", solution)
            err = False
        except Exception:
            print("error: numerical solving 3")
            err = True
            pass    
    else:
        pass
#%%
    #note previous files    
    try:    
        out = np.genfromtxt(filename + form, dtype='float', delimiter = ',', skip_header=0)
        #print(type(out))
        # print("out: ", out)
        if np.shape(out) == (0,):
            print("empty txt detected")
            out = np.empty((2,len(res)))
        else:
            print("non empty txt detected")
        #print(np.shape(out))
        #print(type(np.shape(out)))
    except Exception:
        print("error: fetching solution array")
        pass
#%%
    #check for change from previous temperature
    inx1 = inx - 1
    if inx > 0:
        try:
            change = solution[0] - results[inx1,7]
            if abs(change)>maxjump and abs(change)<1000 and results[inx1,1]>lbnd and results[inx1,1]<upbnd:
                redjump = True
            if abs(change)>maxjump and abs(change)<1000 and results[inx1,1]>lbnd and results[inx1,1]<upbnd:
                redjump = False
            print("change: ", change)
            while abs(change)>maxjump and abs(change)<1000 and results[inx1,1]>lbnd and results[inx1,1]<upbnd:
                if change > 0:
                    solution[0] -= 1
                    change = solution[0] - results[inx1,7]
                    print("change: ", change)
                if change < 0:
                    solution[0] += 1
                    change = solution[0] - results[inx1,7]
                    print("change: ", change)
            if redjump == True:
                print("Reduced Jump Th:", solution[0])
        except Exception:
            print("error: reducing jump")
            pass
    else:
        pass
#%%
    #anomalous final check, if so reset values
    if (solution[0]<lbnd or solution[0]>upbnd):
        print("Unable to find reasonable solution")
        inx1 = inx - 1
        try:
            #print(np.shape(results))
            solution[0] = results[inx1,7]
        except Exception:
            print("error previousing")
            solution = mastguess
        #print(type(solution))
        print("reset solution: ", solution)
        #reset = True
    else:
        pass
#%%
#if reset == False:
    #calculating delta
    try:
        delta = solution[0] - raw[valdpos]
        print("delta: ", delta)
        deltaarr = np.array([])
        deltaarr = np.append(deltaarr, delta)
        #print(deltaarr)
    except Exception:
        print("error: calculating delta")
        pass
    
    #creating solution line to append
    try:
        res = np.array([A, B, C, D, E, F, raw[valdpos]])
        res = np.append(res, solution)
        res = np.append(res, deltaarr)
        #print(np.shape(res))
        print("Results: Tval, Th, Tc, k, delta", res)
    except Exception:
        print("error: forming solution line")
        pass
#else:
    #res = solution
    
    try:
        results = np.append(out, [res], axis=0)
        #print(results)
        np.savetxt(filename + form, results, delimiter = ',')
    except Exception:
        print("error: appendation")
        pass
    
#%%
    #AVERAGING CODE
    
    #Averaging over last 3 values
    try:
        inx1 = inx - 1
        inx2 = inx - 2
        if inx == 0 or inx == 1:
            avgposs = False
        else:
            Thav = np.mean([results[inx,7], results[inx1,7], results[inx2,7]])
            avgposs = True
    except Exception:
        print("error: averaging")
        pass
    
    #note previous avg files    
    try:    
        outav = np.genfromtxt(filenameavg + form, dtype='float', delimiter = ',', skip_header=0)
        #print(type(out))
        # print("out: ", out)
        if np.shape(outav) == (0,):
            print("empty txt detected")
            outav = np.empty((2,len(res)))
        else:
            print("non empty txt detected")
        #print(np.shape(out))
        #print(type(np.shape(out)))
    except Exception:
        print("error: fetching solution array avg")
        pass
    
    if avgposs == True:
        #calculating delta
        try:
            deltaav = Thav - raw[valdpos]
            print("delta: ", deltaav)
            deltaarrav = np.array([])
            deltaarrav = np.append(deltaarrav, deltaav)
            #print(deltaarr)
        except Exception:
            print("error: calculating delta average")
            pass
        
        #creating new average solution
        try:
            solutionav = np.array([Thav, solution[1], solution[2]])
        except Exception:
            print("error: creating average solution line")
    elif avgposs == False:
        solutionav = solution
    else:
        print("error in averaging logic")
        pass
    
    #creating solution line to append
    try:
        resav = np.array([A, B, C, D, E, F, raw[valdpos]])
        resav = np.append(resav, solutionav)
        resav = np.append(resav, deltaarrav)
        #print(np.shape(res))
        print("Results: Tval, Thav, Tc, k, deltaav", resav)
    except Exception:
        print("error: forming average solution line")
        pass
    
    #appending and saving array
    try:
        resultsav = np.append(outav, [resav], axis=0)
        #print(results)
        np.savetxt(filenameavg + form, resultsav, delimiter = ',')
    except Exception:
        print("error: average appendation")
        pass
    
    inx += 1
    print(inx)
    #print("----------")
   