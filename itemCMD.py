from itemDB import *

def commandParser(rawInput):
    args = { 
        "c": rawInput.split()
    }
    args.update({"v": len(args["c"])})
    return args

def keyCreation(unformatedData):
    keyValue = {}
    for entry in unformatedData:
        tmp = entry.split("=")
        keyValue.update({str(tmp[0]): tmp[1]})

    if "homebrew" in keyValue:
        keyValue["homebrew"] = strToBool(keyValue["homebrew"])

    return keyValue

def printResult(result):
    if result["success"]:
        for key, value in result.items():
            if(not key == "success"):
                print(value)

    else:
        print(f"Error!!", result["reason"], sep="\n")

def strToBool(string):

    return string.lower() in ['true']

if __name__ == '__main__':
    items = itemDB()#Start the database
    items.updateList()#Must call this function, else you are fucked

    print("Welcome to the item database command line interface.\nThis the command line version of the database.\nType 'help' to get a list of commands.\nType 'exit' to exit the CMD inteface.")

    command = ""

    while command != "exit":
        commandInput = input(">")
        args = commandParser(commandInput)
        command = args["c"][0]

        print(args)

        if(command == "addItem" and args["v"] >= 3):
            keyValue = keyCreation(args["c"][2:])
            printResult(items.addItem(args["c"][1], **keyValue))

        elif(command == "deleteItem" and args["v"] == 2):
            printResult(items.deleteItem(args["c"][1]))

        elif(command == "editItem" and args["v"] == 4):
            if "homebrew" == args["c"][2]:
                args["c"][3] = strToBool(args["c"][3])
            printResult(items.editItem(args["c"][1], args["c"][2], args["c"][3]))

        elif(command == "printItem" and args["v"] == 2):
            printResult(items.printItem(args["c"][1]))

        elif(command == "listItems" and args["v"] == 1):
            print("List of all items in the database:")
            print(items)

        elif(command == "help" and args["v"] == 1):
            print("Hasn't been implemented yet")

        elif(command == "exit"):
            print("Have a good day!")

        else:
            print("No such command exists or not enough arguments.\nRun 'help' to get help")
