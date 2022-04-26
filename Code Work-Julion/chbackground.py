import random
import pathlib

def bgchooser():
    try:
        bgnum = 0
        bgList = open("CharDatabase/Background/$List.txt")
        bgread = bgList.read()
        bgEntries = bgread.split("\n")
        for o in bgEntries:
            if o:
                bgnum += 1
        bgChosen = bgEntries[random.randint(0,bgnum-1)]
    finally:
        bgList.close()
        return bgChosen


def bgrollertry(bgChosen):
    while True:
        bgtest = bgChosen
        opentest = False
        bgpath = "CharDatabase/Background/"+str(bgtest)+".txt"
        path = pathlib.Path(str(bgpath))
        if path.exists():
            opentest = True
        else:
            opentest = False
            return False
        if opentest:
            break
    return bgtest

def fullbg():
    while True:
        while True:
            mybg = bgchooser()
            if bgrollertry(mybg):
                break
        print("Current Background: "+str(mybg))
        bgFlage = False
        while True:
            incheck = input("Reroll? (y/n): ")
            if incheck == "n":
                bgFlag = True
                break
            if incheck == "y":
                bgFlag = False
                break
            else:
                print("Not Correct. 'y' or 'n' Only Please. ")
        if bgFlag is True:
            break
    return mybg

def bgabbilitiesadd(filename, bg):
    try:
        charfile = open("CharDatabase/characters/"+str(filename)+".txt",'a')
        bgfile = open("CharDatabase/Background/"+str(bg)+".txt")
        bgread = bgfile.read()
        bgsplit = bgread.split("\n")
        j = 7
        while bgsplit[j] != "**":
            charfile.write(str(bgsplit[j])+"\n")
            j += 1
    finally:
        charfile.write("**\n")
        bgfile.close()
        charfile.close()