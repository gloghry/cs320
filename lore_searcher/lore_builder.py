from sys import argv
import classes.cmdFuncs as cmdf
from os import system, path, remove
from classes.LoreSearcher import Searcher
from classes.LorePage import Page
from classes.LoreSection import Section
from classes.LoreMaster import Master

"""

Todo:
 - write help function
 - write setup
 - write editLore
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
        ("add_section", "mks"): lambda: cmdf.addSection(master, args),
        ("print_page", "pp"): lambda: cmdf.printPage(searcher, args),
        ("del_section", "rms"): lambda: cmdf.deleteSection(master, args),
        ("list_section", "ls"): lambda: cmdf.listSection(master, args),
        ("search", "s"): lambda: cmdf.search(searcher, args),
        ("add_page", "mkp"): lambda: cmdf.addPage(master, searcher, args),
        ("del_page", "rmp"): lambda: cmdf.delPage(master, args),
        ("list_all", "la"): lambda: master.listAllSections(),
        ("save_lore", "save"): lambda: cmdf.saveLore(master, args),
        ("pretty_save", "psave"): lambda: cmdf.prettySave(master, textBound, args),
        ("load_lore", "load"): lambda: cmdf.loadLore(master, searcher, args),
        ("print_lore", "pl"): lambda: master.printLore(textBound),
        ("print_section", "ps"): lambda: cmdf.printSection(master, args),
        ("clear", "clr"): lambda: system('clear'),
        ("help", "h"): lambda: cmdf.printHelp(),
        ("edit_lore", "elore"): lambda: cmdf.editLore(master)
    }

    for pair in funcs:
        if cmd in pair:
            funcs[pair]()
            return
    print(
        f"Command '{cmd}' not recognized. Enter 'help' to see available commands")


def finalSave():
    print("Would you like to save your current session?")
    uinput = input("Press [y] for yes, anything else for no: ")
    if uinput == 'y':
        filename = master.cName.replace(' ', '_').lower()
        lorePath = path.join("lore_files", f"{filename}.lore")
        if master.saveLore(lorePath) == False:
            return

    uinput = input("Would you like to PRETTY save your current session (y): ")
    if uinput == 'y':
        filename = master.cName.replace(' ', '_').lower()
        lorePath = path.join("lore_files", f"{filename}.txt")
        if master.prettySave(lorePath) == False:
            return

    # session ended normally, remove tmp.lore file
    tmpPath = path.join("lore_files", "tmp.lore")
    if path.exists(tmpPath):
        remove(tmpPath)


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
    print("Goodbye!")


if __name__ == '__main__':
    main(argv)
