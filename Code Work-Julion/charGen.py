import math
import random
import array


if __name__ == '__main__':
    print("Welcome to the Character Creator! What Level are you starting at? Enter Integer Bellow (1-20)")
    while True:
        lvlNum = input()
        try:
            intVal = int(lvlNum)
            if int(lvlNum) in range(1, 21):
                break
            else:
                print("Not a integer between 1 and 20.")
        except ValueError:
            print("This is not a integer, please try again.")
    print("You have entered "+str(lvlNum)+".")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

    try:
        raceNum = 0
        raceList = open("Race/$List.txt")
        raceRead = raceList.read()
        raceEntries = raceRead.split("\n")
        for i in raceEntries:
            if i:
                raceNum += 1
        raceFlag = False  # please don't cancel me, this stuff is just easy term.
        while True:
            raceRand = raceEntries[random.randint(0, raceNum)]
            print("Currently Random Race: " + str(raceRand) + ".")
            while True:
                raceInp = input("Would you like to roll your race again? (y/n): ")
                if str(raceInp) == "n":
                    raceFlag = True
                    break
                if str(raceInp) == "y":
                    print("Re-rolling...")
                    break
                else:
                    print("Not valid, please choose y or n")
            if raceFlag is True:
                break
        raceNum = 0

        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
        classNum = 0
        classList = open("Class/$List.txt")
        classRead = classList.read()
        classEntries = classRead.split("\n")
        for j in classEntries:
            if j:
                classNum += 1
        classFlag = False
        while True:
            classRand = classEntries[random.randint(0, classNum)]
            print("Currently Random Class: " + str(classRand) + ".")
            while True:
                classInp = input("Would you like to roll your class again? (y/n): ")
                if str(classInp) == "n":
                    classFlag = True
                    break
                if str(classInp) == "y":
                    print("Re-rolling...")
                    break
                else:
                    print("Not valid, please choose y or n")
            if classFlag is True:
                break
        classNum = 0
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
        print(str(raceRand + " " + classRand))

    finally:
        try:
            raceList.close()
            classList.close()
        finally:
            raceRand = 0
            classRand = 0
