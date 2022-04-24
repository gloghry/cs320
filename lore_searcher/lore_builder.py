from classes.LoreSearcher import Searcher
from classes.LorePage import Page
from classes.LoreSection import Section


sections = {"inspiration": Section("inspiration"), "bruh": Section("bruh")}
searcher = Searcher("data/index")

def addSection(args):
    if len(args) > 1 or args[0] in sections:
        return
    sections[args[0]] = Section(args[0])

def printPage(args):
    if len(args) < 2:
        return
    sName = args[0]
    pageID = args[1]

    if sName in sections:
        sections[sName].printPage(pageID, 80)

def deleteSection(args):
    if len(args) == 1 and args[0] in sections:
        del sections[args[0]]

def listSection(args):
    if len(args) == 1 and args[0] in sections:
        sections[args[0]].listSection()

def search(args):
    if len(args) < 1:
        return
    query = args[0]
    results = searcher.search(query)
    if results['results'] == None:
        print(f"0 results found for '{results['query']}', did you mean '{results['corrected']}'?")
    else:
        for result in results['results']:
            result.printSummary(80)

def addPage(args):
    tmp = len(args)
    if tmp != 2:
        return
    sName = args[0]
    if sName not in sections:
        print(f"No section titled '{sName}' found")
        return

    pageID = args[1]
    page = searcher.searchID(pageID)
    if page == None:
        print(f"Sorry, a page with id:{pageID} could not be found")
        return

    sections[sName].addPage(page)

    
def delPage(args):
    tmp = len(args)
    if tmp != 2:
        return
    sName = args[0]
    if sName not in sections:
        print(f"No section titled '{sName}' found")
        return

    pageID = args[1]
    if pageID not in sections[sName].pageIDs:
        print(f"{sName} does not have that page")
        return

    sections[sName].delPage(pageID)


def func(cmd, args):
    funcs = {
        "add_section": lambda: addSection(args),
        "print_page": lambda: printPage(args),
        "del_section": lambda: deleteSection(args),
        "list_section": lambda: listSection(args),
        "search": lambda: search(args),
        "add_page": lambda: addPage(args),
        "del_page": lambda: delPage(args)
    }

    funcs[cmd]()


while True:
    uInput = input("> ")
    if uInput == 'q':
        break
    tmp = uInput.split(",")
    func(tmp[0], list(map(lambda x: x.strip(), tmp[1:])))

