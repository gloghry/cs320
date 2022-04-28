import os
import json

class itemDB:
    def __init__(self):#Intilizes the database
        self.itemList = []
        self.validKeys = [
            "name",
            "homebrew",
            "description",
            "range",
            "ac",
            "damage",
            "rarity",
            "weight"
        ]
        
    def updateList(self):#Updates the current list of items in the database
        self.itemList = []
        for file in os.listdir("items/"):
            if file.endswith(".item"):
                self.itemList.append(self.itemName("items/" + file))

    def addItem(self, name, **kwargs):#This will add an item to the database
        if(self.isItem(name)):
            return self.jsonFormat(False, reason = "Item already exists")

        tmp = self.convertKwargs(**kwargs)

        if(not ('homebrew' in tmp)):
            return self.jsonFormat(False, reason = "Must contain the homebrew key")

        newItem = {"name": name}
        for tName, dType in kwargs.items():
            if tName in self.validKeys:
                newItem.update({str(tName): dType})

        self.save(newItem)
        self.updateList()

        return self.jsonFormat(True)

    def deleteItem(self, name):#This will delete and item from the database
        if(not self.isItem(name)):
            return self.jsonFormat(False, reason = "Item does not exist")

        if(not self.isHomebrew(name)):
            return self.jsonFormat(False, reason = "Don't have permission to delete item")

        if os.path.exists(f'items/{self.fileName(name)}.item'):
            os.remove(f'items/{self.fileName(name)}.item')
        else:
            return self.jsonFormat(False, reason = "No such file exists")

        self.updateList()

        return self.jsonFormat(True)

    def editItem(self, name, key, value):#This will edit the item in the database
        if(not self.isItem(name)):
            return self.jsonFormat(False, reason = "Item does not exist")
        
        if(not self.isHomebrew(name)):
            return self.jsonFormat(False, reason = "Don't have permission to edit item")

        if key not in self.validKeys:
            return self.jsonFormat(False, reason = "{key} is not a valid key")

        if(key == "name"):
            with open(f'items/{self.fileName(name)}.item', 'r') as file:
                item = json.load(file)
                item[key] = value
                self.save(item)
            os.remove(f'items/{self.fileName(name)}.item')
            self.updateList()
            return self.jsonFormat(True)                      

        with open(f'items/{self.fileName(name)}.item', 'r') as file:
            item = json.load(file)
            if key in item:
                item.update({key: value})
                self.save(item)
                return self.jsonFormat(True)
            else:
                return self.jsonFormat(False, reason = "Doesn't exist for {name}")

    def printItem(self, name):#This prints out the item in a nice format
        if(not self.isItem(name)):
            return self.jsonFormat(False, reason = "Item does not exist")

        with open(f'items/{self.fileName(name)}.item', 'r') as file:
            item = json.load(file)
            itemString = ""
            for key, value in item.items():
                itemString += f"{str(key).capitalize()}: {value}\n"

            return self.jsonFormat(True, string = itemString, **item)

    def returnValidKeys(self):
        return self.validKeys

    def isItem(self, name):#Checks to see if item exists in the data base
        for itemName in self.itemList:
            if (itemName == name):
                return True

        return False

    def isHomebrew(self, itemName):#Checks to see if item is homebrew or not
        with open(f'items/{self.fileName(itemName)}.item', 'r') as file:
            item = json.load(file)
            return item["homebrew"]

    def itemName(self, filePath):#Returns the item's name
        file = open(filePath)
        data = json.load(file)
        file.close()
        return data["name"]   

    def save(self, data):#Saves the item
        with open(f'items/{self.fileName(data["name"])}.item', 'w') as item:
            json.dump(data, item)

    def fileName(self, name):#Converts an item's name to an acceptable file name
        return name.lower().strip()

    def convertKwargs(self, **kwargs):
        formatedKwargs = {}
        
        for key, value in kwargs.items():
            formatedKwargs.update({str(key): value})

        return formatedKwargs     

    def jsonFormat(self, success, **kwargs):#Takes in the arguments and converts it into a dict/json
        dataFormated = {"success": success}

        for tName, dType in kwargs.items():
            dataFormated.update({str(tName): dType})

        return dataFormated

    def __str__(self):#Will return the full list of items in database
        return str('\n'.join(map(str, self.itemList)))