import numpy as np
import matplotlib.pyplot as plt
import aseegg as ag
import pandas as pd

electrode = 4
t =  5
f = 1

daneRaw04= np.genfromtxt('904.txt', delimiter=', ')

dane04 = ag.pasmowozaporowy(daneRaw04[:,electrode],250, 49, 51)
dane04 = ag.pasmowoprzepustowy(dane04, 250, f , 49)



daneRaw45= np.genfromtxt('945.txt', delimiter=', ')

dane45 = ag.pasmowozaporowy(daneRaw45[:,electrode],250, 49, 51)
dane45 = ag.pasmowoprzepustowy(dane45, 250, f , 49)

#o1 - 6, o2 - 5, oz - 4, p2 - 3, p3 - 8, p4 - 7, cz - 2, fpz - 1
daneSum = [[0 for i in range(1250)]for j in range(6)]
daneFFT = [[0 for i in range(1250)]for j in range(6)]
triggers = [6,8,10,14,20,24]
triggerOrder04 = [0,5,4,1,5,2,4,5,2,2,4,3,1,3,3,1,0,0]
triggerOrder45 = [0,5,2,2,4,3,5,5,1,4,4,2,3,0,1,1,0,3]


def sum(triggerOrder, daneSum, daneRaw, dane):
    first = True
    triggerNumber = 0

    for i in range(daneRaw.shape[0]):
        
        if first == True:
            if daneRaw[i, 15] == 0 and daneRaw[i-1, 15] == 1:
                n = 0
                for j in range( i - 1250,i):
                    daneSum[triggerOrder[triggerNumber]][n] += dane[j]
                    n += 1 
            
            triggerNumber += 1
            first = False

        else:
            if daneRaw[i, 15] == 1 and daneRaw[i-1, 15] == 0 and triggerNumber != 18:
                n = 0
                for j in range( i,i + 1250 ):
                    daneSum[triggerOrder[triggerNumber]][n] += dane[j]
                    n += 1 
                triggerNumber += 1


def sumFFT(triggerOrder, daneFFT, daneRaw, dane):
    first = True
    triggerNumber = 0
    tempFFT = [0 for i in range(1250)]
    for i in range(daneRaw.shape[0]):
        
        if first == True:
            if daneRaw[i, 15] == 0 and daneRaw[i-1, 15] == 1:
                n = 0
                for j in range(i-1250,i):
                    tempFFT[n] = dane[j]
                    n += 1

                tempFFT = ag.FFT(tempFFT)

                for j in range(len(tempFFT)):
                    daneFFT[triggerOrder[triggerNumber]][j] += tempFFT[j]
         
            triggerNumber += 1
            first = False

        else:
            if daneRaw[i, 15] == 1 and daneRaw[i-1, 15] == 0 and triggerNumber != 18:
                n = 0
                for j in range(i,i+1250):
                    tempFFT[n] = dane[j]
                    n += 1

                tempFFT = ag.FFT(tempFFT)

                for j in range( len(tempFFT) ):
                    daneFFT[triggerOrder[triggerNumber]][j] += tempFFT[j]

                triggerNumber += 1


#sumFFT(triggerOrder04, daneFFT, daneRaw04, dane04)
#sumFFT(triggerOrder45, daneFFT, daneRaw45, dane45)

for i in range(len(daneFFT)):
    for j in range(len(daneFFT[i])):
        daneFFT[i][j] = daneFFT[i][j]/6

ag.spektrogram(dane04,250)
#t = np.linspace(-1.5, 0.5, 500)
#plt.plot (t, daneSum)
#plt.xlabel("t[s]")
#plt.ylabel(r"U [$\mu V$]")
#plt.show()