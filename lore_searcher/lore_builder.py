import os
import json
from classes.LoreSearcher import Searcher
from classes.LorePage import Page
from classes.LoreSection import Section
from classes.LoreMaster import Master

master = Master("drizzt")
s1 = Section("inspiration")
master.addSection(s1)
s2 = Section("bruh")
master.addSection(s2)
master.cClass = "skirmisher"
master.cSex = "male"
master.cOrigin = "underdark"
master.cRace = "drow"
master.cBio = """Drizzt Do'Urden was a drow. He stood about 5 feet and 4 inches (1.6 meters) tall and weighed about 130 pounds (59 kilograms).[13] His handsome features were sharp and well proportioned and, like other drow, Drizzt's skin was black and his stark white hair was long, thick, and flowing. His eyes were a lavender hue (quite different from the drow race's typical red, even when he used his infravision, which normally caused eyes to glow red) and seemed to glow fiercely when he was angry or determined.[20]"""

textBound = 80
searcher = Searcher("data/index")

def addSection(args):
    if len(args) != 1:
        print("Invalid number of arguments: <add_section, sectionName>")
        return
    newSection = Section(args[0])
    if master.addSection(newSection) == False:
        print(f"Section '{args[0]}' already exists, aborting...")

def printPage(args):
    if len(args) != 1:
        return
    page = searcher.searchID(args[0])
    if page != None:
        page.printFull()
    else:
        print(f"Sorry, no page with id: {args[0]} exists in index")

def deleteSection(args):
    if len(args) != 1:
        print("Invalid number of arguments: <del_section, sectionName>")
        return
    if master.delSection(args[0]) == False:
        print(f"No '{args[0]}' section found, aborting...")

def listSection(args):
    if len(args) != 1:
        print("Invalid number of arguments: <list_section,sectionName>")
    if master.listSection(args[0]) == False:
        print(f"Section '{args[0]}' was not found")

def search(args):
    if len(args) < 1:
        return
    query = args[0]
    results = searcher.search(query)
    if results['results'] == None:
        print(f"0 results found for '{results['query']}', did you mean '{results['corrected']}'?")
    else:
        for result in results['results']:
            result.printSummary()

def addPage(args):
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
    
def delPage(args):
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

def saveLore(args):
    filename = master.cName.replace(' ', '_').lower()
    path = f"lore_files/{filename}.lore"
    if len(args) != 0:
        print("Invalid save command: <save_lore>")
        return
    if master.saveLore(path) == False:
        print("An error occured while trying to save, aborting..")
    else:
        print("Lore saved successfully")

def prettySave(args):
    pass

def loadLore(args):
        if len(args) != 1:
            print("Invalid number of arguments: <load_lore,path_to_file>")
            return

        filePath = args[0]
        if not os.path.exists(filePath):
            print(f"File path '{filePath}' could not be found, aborting")
            return

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
                    print(f"Sorry, a page with id:{page['id']} could not be found, skipping...")
                    continue
                newSection.addPage(tmpPage)
            master.sectionDict[section['name']] = newSection

        print("Lore loaded successfully")

def printSection(args):
    if len(args) != 1:
        print("Invalid number of arguments: <print_section,sectionName>")
        return
    sName = args[0]
    if sName not in master.sectionDict:
        print(f"Section '{sName}' not found")
        return
    master.sectionDict[sName].printSection()

def func(cmd, args):
    funcs = {
        "add_section": lambda: addSection(args),
        "print_page": lambda: printPage(args),
        "del_section": lambda: deleteSection(args),
        "list": lambda: listSection(args),
        "search": lambda: search(args),
        "add_page": lambda: addPage(args),
        "del_page": lambda: delPage(args),
        "list_all": lambda: master.listAllSections(),
        "save": lambda: saveLore(args),
        "pretty_save": lambda: prettySave(args),
        "load": lambda: loadLore(args),
        "print_lore": lambda: master.printLore(textBound),
        "print_section": lambda: printSection(args)
    }

    if cmd not in funcs:
        print(f"Command '{cmd}' not recognized. Enter 'help' to see available commands")
        return

    funcs[cmd]()


while True:
    uInput = input("> ").lower()
    if uInput == 'q' or uInput == 'quit':
        break
    if uInput =='':
        continue
    tmp = uInput.split(",")
    func(tmp[0], list(map(lambda x: x.strip().lower(), tmp[1:])))

