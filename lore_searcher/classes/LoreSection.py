class Section:
    def __init__(self, sectionName):
        self.sectionName = sectionName
        self.pageDict = {}
        self.pageIDs = []
        self.totalPages = 0

    def addPage(self, page):
        if page.id not in self.pageDict:
            self.pageDict[page.id] = page
            self.pageIDs.append(page.id)
            self.totalPages += 1

    def delPage(self, pageID):
        if pageID in self.pageDict:
            del self.pageDict[pageID]
            del self.pageIDs[self.pageIDs.index(pageID)]
            self.totalPages -= 1

    def printSection(self, bound=80):
        title = f"\nSection: {self.sectionName.title()}"
        print(title)
        print(len(title)*"-")
        for id, page in self.pageDict.items():
            page.printSummary(bound)

    def getSection(self):
        return {
            "name": self.sectionName,
            "total-pages": self.totalPages,
            "ids": self.pageIDs,
            "page-list": list(map(lambda x: self.pageDict[x].getFull(), self.pageIDs))
        }

    def listSection(self):
        print("\n" + self.sectionName.title())
        print(len(self.sectionName)*"-")
        for id, page in self.pageDict.items():
            print(f"|- {page.pageName} (id:{id})")
        print()
