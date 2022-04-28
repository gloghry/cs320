from os import path, remove, listdir
from sys import stdin
from .LoreSection import Section


def helpErrorMsg():
    print("Enter 'help' or 'h' for more details")


def usageMsg(usageStr):
    print(f"Invalid number of arguments\nUsage: {usageStr}")


def clrTmp():
    # session ended normally, remove tmp.lore file
    tmpPath = path.join("lore_files", "tmp.lore")
    if path.exists(tmpPath):
        remove(tmpPath)


def tmpSave(master):
    tmpPath = path.join("lore_files", "tmp.lore")
    master.saveLore(tmpPath)


def addSection(master, args):
    if len(args) != 1:
        usageMsg("<add_section / mks, sectionName>")
        helpErrorMsg()
        return
    newSection = Section(args[0])
    if master.addSection(newSection) == False:
        print(f"ERROR: Section '{args[0]}' already exists")
        return
    tmpSave(master)


def printPage(searcher, args):
    if len(args) != 1:
        return
    page = searcher.searchID(args[0])
    if page != None:
        page.printFull()
    else:
        print(f"Sorry, no page with id: {args[0]} exists in index")


def deleteSection(master, args):
    if len(args) != 1:
        usageMsg("<del_section / rms, sectionName>")
        helpErrorMsg()
        return
    if master.delSection(args[0]) == False:
        print(f"ERROR: No '{args[0]}' section found")
        return
    tmpSave(master)


def listSection(master, args):
    if len(args) != 1:
        usageMsg("<list_section / ls, sectionName>")
        helpErrorMsg()
        return
    if master.listSection(args[0]) == False:
        print(f"Section '{args[0]}' was not found")


def search(searcher, args):
    if len(args) < 1:
        return
    query = args[0]
    pageno = 1
    while True:
        results = searcher.search(query, pageNum=pageno)
        if results['results'] == None:
            print(
                f"0 results found for '{results['query']}', did you mean '{results['corrected']}'?")
            break

        pageTot = results['total-pages']
        for result in results['results']:
            result.printSummary()
        if pageno == pageTot:
            print(f"No more results for {query}")
            break
        uinput = input(
            "Press [Enter] for more results, or [n] to stop: ").lower()
        while uinput not in ['', 'n']:
            uinput = input(
                "Press [Enter] for more results, or [n] to stop: ").lower()
        if uinput == "":
            pageno += 1
        else:
            break


def addPage(master, searcher, args):
    if len(args) != 2:
        usageMsg("<add_page / mkp, sectionName, pageID>")
        helpErrorMsg()
        return
    sName = args[0]
    if sName not in master.sectionDict:
        print(f"ERROR: No section titled '{sName}' found")
        return

    pageID = args[1]
    page = searcher.searchID(pageID)
    if page == None:
        print(f"Sorry, a page with id:{pageID} could not be found")
        return

    master.sectionDict[sName].addPage(page)
    tmpSave(master)


def delPage(master, args):
    if len(args) != 2:
        usageMsg("<del_page / rmp, sectionName, pageID>")
        helpErrorMsg()
        return
    sName = args[0]
    if sName not in master.sectionDict:
        print(f"ERROR: No section titled '{sName}' found")
        return
    pageID = args[1]
    if pageID not in master.sectionDict[sName].pageIDs:
        print(f"ERROR: '{sName}' does not have that page")
        return

    master.sectionDict[sName].delPage(pageID)
    tmpSave(master)


def saveLore(master, args):
    meta = master.getMeta()
    filename = master.cName.replace(' ', '_').lower()
    v = meta['vNum']
    file = f"{filename}.lore" if v == 0 else f"{filename}({v}).lore"
    filePath = path.join("lore_files", file)

    if path.exists(filePath) and meta['isSaved'] == False:
        uinput = input(
            f"A file named '{file}' already exists\nWould you like to replace it (y/n): ").lower()
        while uinput not in ['y', 'n']:
            uinput = input("Enter 'y' for yes, or 'n' for no: ").lower()

        if uinput == 'n':
            dirFiles = listdir('lore_files')
            vNums = [x[x.find('(') + 1:x.find(')')]
                     for x in dirFiles if "(" in x and ").lore" in x]
            print(vNums)
            maxV = int(max(vNums)) + 1 if len(vNums) != 0 else 0
            master.version = maxV
            print(master.version)
            filePath = path.join(
                "lore_files", f"{filename}({master.version}).lore")
            print(filePath)

    if len(args) != 0:
        print("Invalid save command\nUsage: <save_lore / save>")
        helpErrorMsg()
        return
    if master.saveLore(filePath) == False:
        print(f"An error occured while attempting save to '{filePath}'")
        return
    master.isSaved = True if path.basename(
        filePath) != 'tmp.lore' else master.isSaved
    clrTmp()


def prettySave(master, textBound, args):
    filename = master.cName.replace(' ', '_').lower()
    filePath = path.join("lore_files", f"{filename}.txt")
    if len(args) != 0:
        usageMsg("<pretty_save / psave>")
        helpErrorMsg()
        return
    if master.prettySave(filePath, textBound) == False:
        print(f"An error occured while attempting save to '{filePath}'")


def loadLore(master, searcher, args):
    if len(args) != 1:
        usageMsg("<load_lore / load, path_to_file>")
        helpErrorMsg()
        return False

    filePath = args[0]
    master.loadLore(filePath, searcher)
    master.isSaved = True if path.basename(
        filePath) != 'tmp.lore' else master.isSaved


def printSection(master, args):
    if len(args) != 1:
        usageMsg("<print_section / ps, sectionName>")
        helpErrorMsg()
        return
    sName = args[0]
    if sName not in master.sectionDict:
        print(f"Section '{sName}' not found")
        return
    master.sectionDict[sName].printSection()


def editLore(master, args):
    argc = len(args)
    if argc < 1 or argc > 2:
        usageMsg("<edit, field> or <edit, field, new_value")
        helpErrorMsg()
        return

    field = args[0]
    validFields = ['name', 'bio', 'class', 'race', 'sex', 'origin', 'type']
    if field not in validFields:
        print(f"Field '{field}' not recognized")
        print(f"Valid Fields: " + ', '.join(validFields))
        return

    if argc == 2:
        newVal = args[1]
    elif field != 'bio' and argc == 1:
        newVal = input("Enter new value: ")

    if field == 'name':
        master.cName = newVal
    elif field == 'bio':
        if argc != 2:
            print("Enter Bio (press [ctrl/cmd + d] when done): ")
            newVal = stdin.read()
        master.cBio = newVal
    elif field == 'class':
        master.cClass = newVal
    elif field == 'race':
        master.cRace = newVal
    elif field == 'sex':
        master.cSex = newVal
    elif field == 'origin':
        master.cOrigin = newVal
    else:
        while newVal not in ['camp', 'char']:
            newVal = input("Enter [camp] or [char]: ").lower()
        master.isCamp = True if newVal == 'camp' else False
    tmpSave(master)


def printHelp():
    print("You have made it to help")
