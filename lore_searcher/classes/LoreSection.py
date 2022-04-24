#from .LorePage import Page

class Section:
    def __init__(self, sectionName):
        self.sectionName = sectionName
        self.pageList = {}
        self.pageIDs = []
        self.totalPages = 0

    def addPage(self, page):
        if page.id not in self.pageList:
            self.pageList[page.id] = page
            self.pageIDs.append(page.id)
            self.totalPages += 1

    def delPage(self, pageID):
        if pageID in self.pageList:
            del self.pageList[pageID]
            del self.pageIDs[self.pageIDs.indexOf(pageID)]
            self.totalPages -= 1

    def printSection(self, bound):
        print(self.sectionName.title())
        print(len(self.sectionName)*"-")
        for id, page in self.pageList.items():
            page.printFull(bound)

    def listSection(self):
        print(self.sectionName.title())
        print(len(self.sectionName)*"-")
        for id, page in self.pageList.items():
            print(f"|- {page.pageName} (id:{id})")
        print("\n")
    
    def printPage(self, pageID, bound):
        if pageID in self.pageList:
            self.pageList[pageID].printFull(bound)
