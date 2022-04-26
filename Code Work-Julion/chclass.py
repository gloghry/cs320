import random
import pathlib


def classchooser():
    try:
        classNum = 0
        classList = open("CharDatabase/Class/$List.txt")
        classRead = classList.read()
        classEntries = classRead.split("\n")
        for j in classEntries:
            if j:
                classNum += 1
        ClassChosen = classEntries[random.randint(0, classNum-1)]
    finally:
        classList.close()
        return ClassChosen


def classrollertry(ClassChoosen):
    while True:
        classtest = ClassChoosen
        opentest = False
        classpath = "CharDatabase/Class/"+str(classtest)+".txt"
        path = pathlib.Path(str(classpath))
        if path.exists():
            #  print("😊 Class File Exists! -> "+str(classtest))
            opentest = True
        else:
            #  print("😢 Class File DOESNT Exist... -> "+str(classtest))
            opentest = False
            return False
        if opentest:
            break
    return classtest


def archchoose(classname):
    #  Chooses archetype based on class.
    #  print("Choosing archetype. . .")
    try:
        file = open("CharDatabase/Class/"+classname+".txt")
        classRead = file.read()
        classLineList = classRead.split("\n")
        archetypeList = classLineList[8].split(", ")
        archnum = 0
        for i in archetypeList:
            if i:
                archnum += 1
        gotarch = archetypeList[random.randint(0, archnum-1)]
    except:
        print("Somehow an error in the archetype choosing!!")
    return str(gotarch)


def fullclass():
    while True:
        while True:
            myClass = classchooser()
            if classrollertry(myClass):
                arch = archchoose(myClass)
                break
        print("Current Class: "+str(arch)+" "+str(myClass))
        classFlag = False
        while True:
            incheck = input("Reroll? (y/n): ")
            if incheck == "n":
                classFlag = True
                break
            if incheck == "y":
                classFlag = False
                break
            else:
                print("Not Correct. 'y' or 'n' Only Please. ")
        if classFlag is True:
            break
    return myClass, arch

def classbaseadd(filename, myclass, level):
    try:
        charfile = open("CharDatabase/characters/"+str(filename)+".txt",'a')
        classfile = open("CharDatabase/Class/" + str(myclass) + ".txt")
        classread = classfile.read()
        classsplit = classread.split("\n")
        j = 11
        while (j-11) < level:
            charfile.write("Level ["+str(j-10)+"]: "+str(classsplit[j])+"\n")
            j += 1
    finally:
        charfile.write("**\n")
        classfile.close()
        charfile.close()