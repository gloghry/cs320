import classes.cmdFuncs as cmdf
from os import system, path
from classes.LoreSearcher import Searcher
from classes.LorePage import Page
from classes.LoreSection import Section
from classes.LoreMaster import Master

master = Master("drizzt")
master.addSection(Section("inspiration"))
master.addSection(Section("bruh"))
master.cClass = "skirmisher"
master.cSex = "male"
master.cOrigin = "underdark"
master.cRace = "drow"
master.cBio = """Drizzt Do'Urden was a drow. He stood about 5 feet and 4 inches (1.6 meters) tall and weighed about 130 pounds (59 kilograms).[13] His handsome features were sharp and well proportioned and, like other drow, Drizzt's skin was black and his stark white hair was long, thick, and flowing. His eyes were a lavender hue (quite different from the drow race's typical red, even when he used his infravision, which normally caused eyes to glow red) and seemed to glow fiercely when he was angry or determined.[20]"""

textBound = 80
ixPath = "data/index"
if not path.exists(ixPath):
    searcher = Searcher(ixPath, "data/pages.json")
else:
    searcher = Searcher(ixPath)


def cmdFuncs(cmd, args):
    funcs = {
        "add_section": lambda: cmdf.addSection(master, args),
        "as": lambda: cmdf.addSection(master, args),
        "print_page": lambda: cmdf.printPage(searcher, args),
        "pp": lambda: cmdf.printPage(searcher, args),
        "del_section": lambda: cmdf.deleteSection(master, args),
        "ds": lambda: cmdf.deleteSection(master, args),
        "ls": lambda: cmdf.listSection(master, args),
        "search": lambda: cmdf.search(searcher, args),
        "s": lambda: cmdf.search(searcher, args),
        "add_page": lambda: cmdf.addPage(master, searcher, args),
        "ap": lambda: cmdf.addPage(master, searcher, args),
        "del_page": lambda: cmdf.delPage(master, args),
        "dp": lambda: cmdf.delPage(master, args),
        "la": lambda: master.listAllSections(),
        "save": lambda: cmdf.saveLore(master, args),
        "pretty_save": lambda: cmdf.prettySave(master, textBound, args),
        "psave": lambda: cmdf.prettySave(master, textBound, args),
        "load": lambda: cmdf.loadLore(master, searcher, args),
        "print_lore": lambda: master.printLore(textBound),
        "pl": lambda: master.printLore(textBound),
        "print_section": lambda: cmdf.printSection(master, args),
        "ps": lambda: cmdf.printSection(master, args),
        "clear": lambda: system('clear')
    }

    if cmd not in funcs:
        print(
            f"Command '{cmd}' not recognized. Enter 'help' to see available commands")
        return

    funcs[cmd]()


while True:
    uInput = input("> ").lower()
    if uInput == 'q' or uInput == 'quit':
        break
    if uInput == '':
        continue
    tmp = uInput.split(",")
    cmdFuncs(tmp[0], list(map(lambda x: x.strip().lower(), tmp[1:])))
