import os
import json
from .LoreSection import Section


def helpErrorMsg():
    print("Enter 'help' or 'h' for more details")


def tmpSave(master):
    path = os.path.join("lore_files", "tmp.lore")
    master.saveLore(path)


def addSection(master, args):
    if len(args) != 1:
        print("Invalid number of arguments\nUsage: <add_section / mks, sectionName>")
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
        print("Invalid number of arguments\nUsage: <del_section / rms, sectionName>")
        helpErrorMsg()
        return
    if master.delSection(args[0]) == False:
        print(f"ERROR: No '{args[0]}' section found")
        return
    tmpSave(master)


def listSection(master, args):
    if len(args) != 1:
        print("Invalid number of arguments\nUsage: <list_section / ls, sectionName>")
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
        print("Invalid number of arguments\nUsage: <add_page / mkp, sectionName, pageID>")
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
        print("Invalid number of arguments\nUsage: <del_page / rmp, sectionName, pageID>")
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
    filename = master.cName.replace(' ', '_').lower()
    path = os.path.join("lore_files", f"{filename}.lore")
    if len(args) != 0:
        print("Invalid save command\nUsage: <save_lore / save>")
        helpErrorMsg()
        return
    if master.saveLore(path) == False:
        print(f"An error occured while attempting save to '{path}'")


def prettySave(master, textBound, args):
    filename = master.cName.replace(' ', '_').lower()
    path = os.path.join("lore_files", f"{filename}.txt")
    if len(args) != 0:
        print("Invalid pretty save command\nUsage: <pretty_save / psave>")
        helpErrorMsg()
        return
    if master.prettySave(path, textBound) == False:
        print(f"An error occured while attempting save to '{path}'")


def loadLore(master, searcher, args):
    if len(args) != 1:
        print("Invalid number of arguments\nUsage: <load_lore / load, path_to_file>")
        helpErrorMsg()
        return False

    filePath = args[0]
    if not os.path.exists(filePath):
        print(f"ERROR: '{filePath}' could not be found")
        return False

    if os.path.isdir(filePath):
        print(f"ERROR: '{filePath}' is a directory")
        return False

    with open(filePath, 'r') as fd:
        data = json.load(fd)

    master.cName = data['character-name']
    master.cBio = data['cBio']
    master.cClass = data['cClass']
    master.cOrigin = data['cOrigin']
    master.cRace = data['cRace']
    master.cSex = data['cSex']
    master.sectionNames = data['section-names']

    sectionDict = {}

    for section in data['sections']:
        newSection = Section(section['name'])
        for page in section['page-list']:
            tmpPage = searcher.searchID(page['id'])
            if tmpPage == None:
                print(
                    f"Sorry, a page with id:{page['id']} could not be found, skipping...")
                continue
            newSection.addPage(tmpPage)
        sectionDict[section['name']] = newSection

    master.sectionDict = sectionDict
    print("Lore loaded successfully")
    return True


def printSection(master, args):
    if len(args) != 1:
        print("Invalid number of arguments\nUsage: <print_section / ps, sectionName>")
        helpErrorMsg()
        return
    sName = args[0]
    if sName not in master.sectionDict:
        print(f"Section '{sName}' not found")
        return
    master.sectionDict[sName].printSection()

def editLore(master):
    pass


def printHelp():
    print("You have made it to help")
