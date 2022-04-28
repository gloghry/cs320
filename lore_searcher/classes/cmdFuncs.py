from os import path, remove, listdir, system
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
        system('clear')
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


def search(searcher, args, start):
    argc = len(args)
    if argc < 1 or argc > 2:
        return
    query = args[0]
    sType = args[1] if argc == 2 else 'AND'
    pageno = 1
    while True:
        results = searcher.search(query, pageNum=pageno, searchType=sType)
        if results['results'] == None:
            if start == False:
                print(
                    f"0 results found for '{results['query']}', did you mean '{results['corrected']}'?")
                return False
            else:
                return False
        elif results['results'] != None and pageno == 1:
            system('clear')
        pageTot = results['total-pages']
        for result in results['results']:
            result.printSummary()
        if pageno == pageTot:
            if start == False:
                print(f"No more results for '{query}'")
            return True
        uinput = input(
            "Press [Enter] for more results, or [n] to stop: ").lower()
        while uinput not in ['', 'n']:
            uinput = input(
                "Press [Enter] for more results, or [n] to stop: ").lower()
        if uinput == "":
            pageno += 1
        else:
            return True


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

def loadChar(master, args):
    filePath = args[0]
    if not path.exists(filePath):
        print(f"ERROR: '{filePath}' could not be found")
        return False

    with open(filePath, 'r') as fd:
        charFile = fd.read()
    
    fields = charFile.split('\n')
    master.cName = fields[0]
    # subrace + race (e.g. 'Hill Giant')
    master.cRace = f"{fields[3]} {fields[2]}"
    master.cClass = fields[4]
    master.cArch = fields[5]

    # getting full bio
    bio = ""
    for string in fields[9:]:
        if string == "**":
            break
        bio += f"{string}\n"
    master.cBio = f"{fields[6].title()}: {bio}"


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

    field = args[0].lower()
    validFields = ['name', 'bio', 'class', 'race', 'sex', 'origin', 'type', 'archetype']
    if field not in validFields:
        print(f"Field '{field}' not recognized")
        print(f"Valid Fields: " + ', '.join(validFields))
        return

    if argc == 2:
        newVal = args[1]
    elif field != 'bio' and argc == 1:
        newVal = input("Enter new value: ")

    updateMsg = lambda x: print(f"{x} updated!")

    if field == 'name':
        master.cName = newVal
        updateMsg("Name")
    elif field == 'bio':
        if argc != 2:
            print("Enter Bio (press [ctrl/cmd + d] when done): ")
            newVal = stdin.read()
        master.cBio = newVal
        updateMsg("Bio")
    elif field == 'class':
        master.cClass = newVal
        updateMsg("Class")
    elif field == 'archetype':
        master.cArch = newVal
        updateMsg("Archetype")
    elif field == 'race':
        master.cRace = newVal
        updateMsg("Race")
    elif field == 'sex':
        master.cSex = newVal
        updateMsg("Sex")
    elif field == 'origin':
        master.cOrigin = newVal
        updateMsg("Origin")
    else:
        while newVal not in ['camp', 'char']:
            newVal = input("Enter [camp] or [char]: ").lower()
        master.isCamp = True if newVal == 'camp' else False
    tmpSave(master)


def printHelp():
    print("""
Command Line Options:                                                                                                   
    -l <path/to/file.lore>  Loads found lore file to new session                                                        
    -c <path/to/char.txt>   Loads randomly generated character to new session                                           
                                                                                                                        
Session Commands:                                                                                                       
    edit_lore | edit, <field>, <new_value>  Changes field to new value                                                  
    load_lore | load, <path/to/file.lore>   Loads character/campaign from file (CURRENT SESSION LOST)                   
    save_lore | save                        Saves current session to name.lore file (Json format)                       
    pretty_save | psave                     Saves current session to name.txt file in print_lore format                 
    clear | clr                             Clears console                                                              
    help | h                                Prints command list
    q | quit                                Quits current session                                                         
                                                                                                                        
Section Commands:                                                                                                       
    add_section | mks, <section_name>           Creates a new section titled 'section_name'                             
    del_section | rms, <section_name>           Removes section and all section pages                                   
    list_section | ls, <section_name>           Lists the pages present in section                                      
    print_section | ps, <section_name>          Prints page summaries for section pages                                 
    add_page | mkp, <section_name>, <page_id>   Adds page associated with id to section                                 
    del_page | rmp, <section_name>, <page_id>   Removes page associated with id from section                            
    list_all | la                               Lists all sections and their pages                                      
                                                                                                                        
Page Commands:                                                                                                          
    print_page | pp, <page_id>  Prints full page to console                                                             
                                                                                                                        
Search Commands:                                                                                                        
    search | s, <search_terms>  Searches index and prints summaries of relevant pages found

REMEMBER: Command arguments should be seperated by COMMAS. Most prompts can be skipped with [ENTER]                                                              
Example: add_page, inspiration, 400  (Adds page associated with id=400 to inspiration section)
    """)
