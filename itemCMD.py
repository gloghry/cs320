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


    result = items.addItem("LongbowHB", homebrew = True, damage = "1d8 Piercing", rarity = "Standard", range = "150/600", weight = 2)

    #result = items.deleteItem("LongbowHB")

    #result = items.editItem("LongbowHB", "name", "testing")

    #result = items.printItem("LongbowHB")

    #print(items)

    print(result)






    #print("Welcome to the item database command line interface.\nThis the command line version of the database.\nType 'help()' to get a list of commands.\nType 'exit()' to exit the CMD inteface.")

    #command = ""

    #while command != "exit()":
     #   commandInput = input(">")
      #  commandParsed = commandParser(commandInput)
       # command = commandParsed[0]

        #if(commandParsed[0] == "addItem()"):
         #   items.addItem(**commandParsed[1])

    #print("""\nAdding a new item non homebrew item to the data base.\nCommand sent: addItem("Longbow", homebrew = False, damage = "1d8 Piercing", rarity = "Standard", range = "150/600", weight = 2)\nResult: """, items.addItem("Longbow", homebrew = False, damage = "1d8 Piercing", rarity = "Standard", range = "150/600", weight = 2))
    #print("""\nTrying to edit that same non homebrew item.\nCommand sent: editItem("Longbow", "rarity", "Rare")\nResult: """, items.editItem("Longbow", "rarity", "Rare"))
    #print("""\nDeleting a non homebrew item.\nCommand sent: deleteItem("Longbow")\nResult: """, items.deleteItem("Longbow"))

    #print("""\n\nNow we do the same except with a homebrew item\n""")

    #print("""\nAdding a new item non homebrew item to the data base.\nCommand sent: addItem("LongbowHB", homebrew = True, damage = "1d8 Piercing", rarity = "Standard", range = "150/600", weight = 2)\nResult: """, items.addItem("LongbowHB", homebrew = True, damage = "1d8 Piercing", rarity = "Standard", range = "150/600", weight = 2))
    #print("""\nTrying to edit that same non homebrew item.\nCommand sent: editItem("LongbowHB", "rarity", "Rare")\nResult: """, items.editItem("LongbowHB", "rarity", "Rare"))
    #print("""\nDeleting a non homebrew item.\nCommand sent: deleteItem("LongbowHB")\nResult: """, items.deleteItem("LongbowHB"))


    #items.addItem("LongbowHB", homebrew = True, damage = "1d8 Piercing", rarity = "Standard", range = "150/600", weight = 2)
    #print("""\n\nLets add back that item we just deleted back into the data base.\nNow lets print out the entire database, which you can do so by just calling items.\n""", items)

    #print("""\nNow lets just print out an individual item.\nCommand sent: printItem("Longbow")\nResult: """, items.printItem("Longbow"))
    #print("""\nLets do the same with the other item.\nCommand sent: printItem("LongbowHB")\nResult: """, items.printItem("LongbowHB"))

    #items.deleteItem("LongbowHB")

    #print("""\n\nI am now going to delete the homebrew item and try to print it again.\n""", items.printItem("LongbowHB"))