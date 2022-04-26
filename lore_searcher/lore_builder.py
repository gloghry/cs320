from sys import argv
import classes.cmdFuncs as cmdf
from os import system, path
from classes.LoreSearcher import Searcher
from classes.LorePage import Page
from classes.LoreSection import Section
from classes.LoreMaster import Master

"""

Todo:
 - write finalSave()
    * remove 'lore_files/tmp.lore' on successful final save
 - save to 'lore_files/tmp.lore' in any function that changes lore state
 - write help function
 - update readme

"""

master = Master()

textBound = 80
ixPath = path.join("data", "index")
if not path.exists(ixPath):
    searcher = Searcher(ixPath, path.join("data", "pages.json"))
else:
    searcher = Searcher(ixPath)


def cmdFuncs(cmd, args):
    funcs = {
        "add_section": lambda: cmdf.addSection(master, args),
        "mks": lambda: cmdf.addSection(master, args),
        "print_page": lambda: cmdf.printPage(searcher, args),
        "pp": lambda: cmdf.printPage(searcher, args),
        "del_section": lambda: cmdf.deleteSection(master, args),
        "rms": lambda: cmdf.deleteSection(master, args),
        "ls": lambda: cmdf.listSection(master, args),
        "search": lambda: cmdf.search(searcher, args),
        "s": lambda: cmdf.search(searcher, args),
        "add_page": lambda: cmdf.addPage(master, searcher, args),
        "mkp": lambda: cmdf.addPage(master, searcher, args),
        "del_page": lambda: cmdf.delPage(master, args),
        "rmp": lambda: cmdf.delPage(master, args),
        "la": lambda: master.listAllSections(),
        "save": lambda: cmdf.saveLore(master, args),
        "pretty_save": lambda: cmdf.prettySave(master, textBound, args),
        "psave": lambda: cmdf.prettySave(master, textBound, args),
        "load": lambda: cmdf.loadLore(master, searcher, args),
        "print_lore": lambda: master.printLore(textBound),
        "pl": lambda: master.printLore(textBound),
        "print_section": lambda: cmdf.printSection(master, args),
        "ps": lambda: cmdf.printSection(master, args),
        "clear": lambda: system('clear'),
        "help": lambda: cmdf.printHelp()
    }

    if cmd not in funcs:
        print(
            f"Command '{cmd}' not recognized. Enter 'help' to see available commands")
        return

    funcs[cmd]()


def finalSave():
    print("made it to final save point")


def setupPrompts():
    print("yoooooo, you made it!")


def mainPrompts():
    while True:
        uInput = input("> ").lower()
        if uInput in ['q', 'quit']:
            break
        if uInput == '':
            continue
        tmp = uInput.split(",")
        cmdFuncs(tmp[0], list(map(lambda x: x.strip().lower(), tmp[1:])))


def main(args):
    argc = len(args)
    isNew = True

    # loading .lore file on startup with 'python3 lore_builder.py -l some_file'
    if argc > 1 and args[1] == '-l':
        if argc != 3:
            print(
                "Invalid amount of arguments\nUsage: python(3) lore_builder.py -l some_file")
            return
        if cmdf.loadLore(master, searcher, args[2:]) == False:
            return
        isNew = False

    # last session closed before final save, ask if user wants to cached lore tmp.lore
    tmpPath = path.join("lore_files", "tmp.lore")
    if path.exists(tmpPath):
        uinput = input(
            "tmp.lore file detected from a previous session\nWould you like to load it (y/n): ").lower()
        while uinput not in ['n', 'y']:
            uinput = input("Please enter 'y' or 'n': ").lower()
        if uinput == 'y':
            if cmdf.loadLore(master, searcher, [tmpPath]) == False:
                return
            isNew = False

    # no lore file loaded on startup, create new lore
    if isNew:
        master.addSection(Section("inspiration"))
        setupPrompts()

    mainPrompts()
    finalSave()


if __name__ == '__main__':
    main(argv)
