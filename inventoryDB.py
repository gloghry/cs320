class inventoryDB:
    def __init__(self):
        self.current = ""

    def setInventory(self, name):
        return self.jsonFormat(False, reason = "Cause yeah")

    def createNewInventory(self, name):
        return self.jsonFormat(False, reason = "Cause yeah")

    def deleteInventory(self, name):
        return self.jsonFormat(False, reason = "Cause yeah")

    def incrementItem(self, itemName):
        return self.jsonFormat(False, reason = "Cause yeah")

    def decrementItem(self, itemName):
        return self.jsonFormat(False, reason = "Cause yeah")

    def removeItem(self, itemName):
        return self.jsonFormat(False, reason = "Cause yeah")

    def jsonFormat(self, success, **kwargs):#Takes in the arguments and converts it into a dict/json
        dataFormated = {"success": success}

        for tName, dType in kwargs.items():
            dataFormated.update({str(tName): dType})

        return dataFormated