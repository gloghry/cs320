from itemDB import *
import re

def commandParser(commandInput):
    commandParsed = ["", ""]

    try:
        commandParsed[1] = str(re.search(r"\(([A-Za-z0-9_]+)\)", commandInput))

        try:
            commandParsed[0] = commandInput.replace("({commandArgs})", "")
            #print("3", command)
        except:
            print("Couldn't figure out what you were saying")
    except:
        print("Couldn't figure out what you were saying")   

    return commandParsed


if __name__ == '__main__':
    items = itemDB()#Start the database
    items.updateList()#Must call this function, else you are fucked

    print("Welcome to the item database command line interface.\nThis the command line version of the database.\nType 'help()' to get a list of commands.\nType 'exit()' to exit the CMD inteface.")

    command = ""

    while command != "exit()":
        commandInput = input(">")
        commandParsed = commandParser(commandInput)
        command = commandParsed[0]