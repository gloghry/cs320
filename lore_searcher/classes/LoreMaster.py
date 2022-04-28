import textwrap
import os
import sys
import json
from functools import reduce
from .LorePage import Page
from .LoreSection import Section
from .LoreSearcher import Searcher


class Master:
    def __init__(self, characterName="new lore", isCamp=False, bio="", cClass="", cArch="", race="", origin="", sex=""):
        self.cName = characterName
        self.cBio = bio
        self.cClass = cClass
        self.cRace = race
        self.cOrigin = origin
        self.cSex = sex
        self.cArch = cArch
        self.version = 0
        self.isSaved = False
        self.isCamp = isCamp
        self.sectionDict = {}
        self.sectionNames = []

    def addSection(self, section) -> bool:
        sName = section.sectionName
        if sName in self.sectionDict:
            return False
        self.sectionDict[sName] = section
        self.sectionNames.append(sName)
        return True

    def delSection(self, sectionName) -> bool:
        if sectionName not in self.sectionDict:
            return False
        del self.sectionDict[sectionName]
        del self.sectionNames[self.sectionNames.index(sectionName)]
        return True

    def printSection(self, sectionName, bound=80):
        if sectionName in self.sectionDict:
            self.sectionDict[sectionName].printSection(bound)

    def getPageTotal(self) -> int:
        if len(self.sectionNames) == 0:
            return 0
        return reduce(lambda x, y: x+y, list(map(lambda x: self.sectionDict[x].totalPages, self.sectionDict)))

    def printLore(self, bound=80):
        os.system('clear')
        cType = "Campaign:" if self.isCamp else "Character:"
        print(f"<{{{{  {cType} {self.cName.title()}  }}}}>\n".center(bound))
        if self.isCamp != True:
            print("Class:", self.cClass.title(), f"({self.cArch})")
            print("Race:", self.cRace.title())
            print("Sex:", self.cSex.title())
            print("Origin:", self.cOrigin.title(), "\n")

        print(textwrap.fill(f"{self.cBio}", width=bound))
        print()
        for name, section in self.sectionDict.items():
            section.printSection(bound)

    def getMaster(self):
        return {
            "character-name": self.cName,
            "cBio": self.cBio,
            "cClass": self.cClass,
            "cRace": self.cRace,
            "cOrigin": self.cOrigin,
            "cSex": self.cSex,
            "cArch": self.cArch,
            "vNum": self.version,
            "page-total": self.getPageTotal(),
            "section-names": self.sectionNames,
            "sections": list(map(lambda x: self.sectionDict[x].getSection(), self.sectionNames))
        }

    def listSection(self, sectionName) -> bool:
        if sectionName in self.sectionDict:
            self.sectionDict[sectionName].listSection()
            return True
        return False

    def listAllSections(self):
        for name, section in self.sectionDict.items():
            section.listSection()

    def saveLore(self, filePath) -> bool:
        try:
            data = self.getMaster()
            with open(filePath, 'w+') as fd:
                json.dump(data, fd, indent=4)
        except Exception as e:
            print(e)
            return False

    def loadLore(self, filePath) -> bool:
        if not os.path.exists(filePath):
            return False

        data = json.load(filePath)
        self.cName = data['character-name']
        self.cBio = data['cBio']
        self.cClass = data['cClass']
        self.cOrigin = data['cOrigin']
        self.cRace = data['cRace']
        self.cSex = data['cSex']
        self.cArch = data['cArch']
        self.version = data['vNum']
        self.sectionNames = data['section-names']

        for section in data['sections']:
            newSection = Section(section['name'])
            for page in section['page-list']:
                tmpPage = Searcher.searchID()

    def prettySave(self, path, bound=80) -> bool:
        try:
            # redirecting stdout to file
            sys.stdout = open(path, 'w+')
            self.printLore(bound)

            # closing file pointer and restoring stdout
            sys.stdout.close()
            sys.stdout = sys.__stdout__

            return True
        except:
            return False
