from chbackground import *
from chrace import *
from chclass import *

def pickbackground():
    try:
        bgList = open("CharDatabase/Background/$List.txt")
        bgread = bgList.read()
        bgEntries = bgread.split("\n")
        bgnum = len(bgEntries)
        bgTrueList = []
        for x in bgEntries:
            if bgrollertry(str(x)):
                bgTrueList.append(str(x))
        i = 0
        for y in bgTrueList:
            print("Number ["+str(i)+"]: "+str(y))
            i = i+1
        while True:
            num = input("Enter Number You Want: ")
            if (int(num) <= i-1) and (int(num) >= 0):
                print("Chosen: "+str(bgTrueList[int(num)]))
                return bgTrueList[int(num)]
            else:
                print("Try Again.")
    finally:
        bgList.close()
def pickclass():
    try:
        clList = open("CharDatabase/Class/$List.txt")
        clread = clList.read()
        clEntries = clread.split("\n")
        clnum = len(clEntries)
        clTrueList = []
        for x in clEntries:
            if classrollertry(str(x)):
                clTrueList.append(str(x))
        i = 0
        for y in clTrueList:
            print("Number ["+str(i)+"]: "+str(y))
            i = i+1
        while True:
            num = input("Enter Number You Want: ")
            if (int(num) <= i-1) and (int(num) >= 0):
                print("Chosen: " + str(clTrueList[int(num)]))
                return clTrueList[int(num)]
            else:
                print("Try Again.")
    finally:
        clList.close()
def pickrace():
    try:
        raList = open("CharDatabase/Race/$List.txt")
        raread = raList.read()
        raEntries = raread.split("\n")
        ranum = len(raEntries)
        raTrueList = []
        for x in raEntries:
            if racerollertry(str(x)):
                raTrueList.append(str(x))
        i = 0
        for y in raTrueList:
            print("Number ["+str(i)+"]: "+str(y))
            i = i+1
        while True:
            num = input("Enter Number You Want: ")
            if (int(num) <= i-1) and (int(num) >= 0):
                print("Chosen: " + str(raTrueList[int(num)]))
                return raTrueList[int(num)]
            else:
                print("Try Again.")
    finally:
        raList.close()