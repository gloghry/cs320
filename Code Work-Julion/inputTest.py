import random
import array
import os
if __name__ == '__main__':
    test = 1

    if test == 0:
        print("State your name:")
        wrInput = input()
        print("Your name is: "+str(wrInput)+".")
        if str(wrInput) == str("0"):
            print("Zero Detected. Nice.")
        else:
            print("Non-Zero.")

    if test == 1:
        print("Name Class:")
        wrInput = input()
        f = open("Class/"+str(wrInput)+".txt")
        print(f.read())
