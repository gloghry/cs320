import os
import json
from .LoreSection import Section
from .LoreMaster import Master

def addSection(master, args):
    if len(args) != 1:
        print("Invalid number of arguments: <add_section, sectionName>")
        return
    newSection = Section(args[0])
    if master.addSection(newSection) == False:
        print(f"Section '{args[0]}' already exists, aborting...")


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
        print("Invalid number of arguments: <del_section, sectionName>")
        return
    if master.delSection(args[0]) == False:
        print(f"No '{args[0]}' section found, aborting...")


def listSection(master, args):
    if len(args) != 1:
        print("Invalid number of arguments: <list_section,sectionName>")
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
        uinput = input("Would you like to view next page (y/n): ")
        if uinput.lower() == 'y' or uinput.lower() == "":
            pageno += 1
        else:
            break

def addPage(master, searcher, args):
    if len(args) != 2:
        print("Invalid number of arguments: <del_page,sectionName,pageID>")
        return
    sName = args[0]
    if sName not in master.sectionDict:
        print(f"No section titled '{sName}' found")
        return

    pageID = args[1]
    page = searcher.searchID(pageID)
    if page == None:
        print(f"Sorry, a page with id:{pageID} could not be found")
        return

    master.sectionDict[sName].addPage(page)


def delPage(master, args):
    if len(args) != 2:
        print("Invalid number of arguments: <del_page,sectionName,pageID>")
        return
    sName = args[0]
    if sName not in master.sectionDict:
        print(f"No section titled '{sName}' found")
        return
    pageID = args[1]
    if pageID not in master.sectionDict[sName].pageIDs:
        print(f"'{sName}' does not have that page")
        return

    master.sectionDict[sName].delPage(pageID)


def saveLore(master, args):
    filename = master.cName.replace(' ', '_').lower()
    path = f"lore_files/{filename}.lore"
    if len(args) != 0:
        print("Invalid save command: <save>")
        return
    if master.saveLore(path) == False:
        print("An error occured while trying to save, aborting..")
    else:
        print("Lore saved successfully")


def prettySave(master, textBound, args):
    filename = master.cName.replace(' ', '_').lower()
    path = f"lore_files/{filename}.txt"
    if len(args) != 0:
        print("Invalid pretty save command: <pretty_save>")
        return
    if master.prettySave(path, textBound) == False:
        print("An error occured while trying to save, aborting..")
    else:
        print("Lore saved successfully")


def loadLore(master, searcher, args):
    if len(args) != 1:
        print("Invalid number of arguments: <load_lore,path_to_file>")
        return False

    filePath = args[0]
    if not os.path.exists(filePath):
        print(f"File path '{filePath}' could not be found, aborting...")
        return False

    newMaster = Master()

    with open(filePath, 'r') as fd:
        data = json.load(fd)

    master.cName = data['character-name']
    master.cBio = data['cBio']
    master.cClass = data['cClass']
    master.cOrigin = data['cOrigin']
    master.cRace = data['cRace']
    master.cSex = data['cSex']
    master.sectionNames = data['section-names']

    for section in data['sections']:
        newSection = Section(section['name'])
        for page in section['page-list']:
            tmpPage = searcher.searchID(page['id'])
            if tmpPage == None:
                print(
                    f"Sorry, a page with id:{page['id']} could not be found, skipping...")
                continue
            newSection.addPage(tmpPage)
        master.sectionDict[section['name']] = newSection

    print("Lore loaded successfully")
    return True


def printSection(master, args):
    if len(args) != 1:
        print("Invalid number of arguments: <print_section,sectionName>")
        return
    sName = args[0]
    if sName not in master.sectionDict:
        print(f"Section '{sName}' not found")
        return
    master.sectionDict[sName].printSection()

def printHelp():
    print("You have made it to help")
