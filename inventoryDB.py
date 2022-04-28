import json
import os

class inventoryDB:
    def __init__(self):
        self.current = ""
        self.inventoryList = []

    def updateList(self):
        self.inventoryList = []
        for file in os.listdir("inventory/"):
            if file.endswith(".inventory"):
                self.inventoryList.append(self.inventoryName("inventory/" + file))

    def setInventory(self, name):
        if(not self.inventoryExists(name)):
            return self.jsonFormat(False, reason = "Inventory for {name} does not exist")

        self.current = self.inventoryName(f"inventory/{self.fileName(name)}.inventory")

        return self.jsonFormat(True)

    def createNewInventory(self, name):
        if(self.inventoryExists(name)):
            return self.jsonFormat(False, reason = "Inventory for {name} already exists")

        with open(f"inventory/{self.fileName(name)}.inventory", "w") as newInventory:
            json.dump({"name": name}, newInventory)

        self.updateList()

        return self.jsonFormat(True)

    def deleteInventory(self, name):
        if(not self.inventoryExists(name)):
            return self.jsonFormat(False, reason = "Inventory for {name} does not exist")

        if os.path.exists(f'inventory/{self.fileName(name)}.inventory'):
            os.remove(f'inventory/{self.fileName(name)}.inventory')
        else:
            return self.jsonFormat(False, reason = "No such file exists")

        if(self.current = name):
            self.current = ""

        self.updateList()

        return self.jsonFormat(True)

    def incrementItem(self, itemName, amount):
        if(not self.inventoryExists(name)):
            return self.jsonFormat(False, reason = "Inventory for {name} does not exist")

        inventory = {}

        with open(f'inventory/{self.fileName(self.current)}.inventory', "r") as inventoryFile:
            inventory = json.load(inventoryFile)
            if itemName in inventory:
                tmp = inventory[itemName]
                tmp += amount
                inventory[itemName] = tmp
            else:
                inventory.update({itemName, amount})
            
        with open(f'inventory/{self.fileName(self.current)}.inventory', "w") as inventoryFile:
            json.dump(inventory, inventoryFile)

        self.updateList()
        
        return self.jsonFormat(False, reason = "Cause yeah")

    def decrementItem(self, itemName, amount):
        if(not self.inventoryExists(self.current)):
            return self.jsonFormat(False, reason = "Inventory for {self.current} does not exist")

        inventory = {}

        with open(f'inventory/{self.fileName(self.current)}.inventory', "r") as inventoryFile:
            inventory = json.load(inventoryFile)
            if itemName in inventory:
                tmp = inventory[itemName]
                tmp -= amount
                inventory[itemName] = tmp
            else:
                inventory.update({itemName, (-1 * amount)})
            
        with open(f'inventory/{self.fileName(self.current)}.inventory', "w") as inventoryFile:
            json.dump(inventory, inventoryFile)

        self.updateList()

        return self.jsonFormat(True)

    def removeItem(self, itemName):
        if(not self.inventoryExists(self.current)):
            return self.jsonFormat(False, reason = "Inventory for {self.current} does not exist")

        if os.path.exists(f'items/{self.fileName(self.current))}.item'):
            os.remove(f'items/{self.fileName(self.current)}.item')
        else:
            return self.jsonFormat(False, reason = "No such file exists")

        self.updateList()

        return self.jsonFormat(True)

    def printInventory(self):
        if(not self.inventoryExists(self.current)):
            return self.jsonFormat(False, reason = "Inventory for {self.current} does not exist")

        with open(f'inventory/{self.fileName(self.current)}.inventory', "r") as inventoryFile:
            inventory = json.load(inventoryFile)
            return self.jsonFormat(True, **inventory)

    def inventoryExists(self, name):
        for inventoryName in self.itemList:
            if (inventoryName == name):
                return True

        return False

    def inventoryName(self, file):
        file = open(filePath)
        data = json.load(file)
        file.close()
        return data["name"] 

    def fileName(self, name):#Converts an item's name to an acceptable file name
        return name.lower().strip()  

    def jsonFormat(self, success, **kwargs):#Takes in the arguments and converts it into a dict/json
        dataFormated = {"success": success}

        for tName, dType in kwargs.items():
            dataFormated.update({str(tName): dType})

        return dataFormated

    def __str__(self):
        return "hello there"