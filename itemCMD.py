from itemType import *
from manifestType import *

if __name__ == '__main__':
    bow = item("Bow", True)
    print(bow)

    bow2 = item("Bow2", False)
    print(bow2)

    print(str(bow.editItem("name", "bow3")))
    print(str(bow2.editItem("homebrew", True)))

    print(bow)

    testMani = manifest("Testing")
    print(testMani)

    testMani.editItem(bow.itemName(), 0)
    print(testMani)

    testMani.editItem("Testing", 100)
    print(testMani)

    testMani.editItem(bow.itemName(), 1)
    print(testMani)

    testMani.editItem("Testing", "Remove")
    print(testMani)  


    