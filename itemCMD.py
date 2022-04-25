from itemDB import *

if __name__ == '__main__':
    items = itemDB()
    items.updateList()
    print(items.deleteItem("Longbow"))
    print(items.addItem("Longbow", homebrew = True))
    print(items.addItem("Longbow", homebrew = True))
    #print(items.editItem("Longbow", "homebrew", False))
    #print(items.editItem("Longbow", "homebrew", False))
    print(items.editItem("Longbow", "homebrewW", False))
    print(items.printItem("Longbow"))
    print(items.deleteItem("Longbow"))
    print(items.printItem("Longbow"))
