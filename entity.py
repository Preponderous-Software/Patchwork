# Copyright (c) 2022 Preponderous Software
# MIT License
import datetime
import uuid


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
class Entity(object):

    def __init__(self, name, energy, living, edibleEntityTypes):
        self.id = uuid.uuid4()
        self.name = name
        self.energy = energy
        self.living = living
        self.edibleEntityTypes = edibleEntityTypes
        self.targetEnergy = energy
        self.creationDate = datetime.datetime.now()
        self.environmentID = -1
        self.gridID = -1
        self.locationID = -1
    
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name

    def getEnvironmentID(self):
        return self.environmentID

    def getCreationDate(self):
        return self.creationDate

    def getEnvironmentID(self):
        return self.environmentID

    def getGridID(self):
        return self.gridID

    def getLocationID(self):
        return self.locationID
    
    def setID(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setEnvironmentID(self, environmentID):
        self.environmentID = environmentID
    
    def setCreationDate(self, creationDate):
        self.creationDate = creationDate

    def setGridID(self, gridID):
        self.gridID = gridID

    def setLocationID(self, locationID):
        self.locationID = locationID
    
    def printInfo(self):
        print("--------------")
        print(self.name)
        print("--------------")
        print("ID: ", self.getID())
        print("Creation Date: ", self.getCreationDate())
        print("Environment ID: ", self.getEnvironmentID())
        print("Grid ID: ", self.getGridID())
        print("Location ID: ", self.getLocationID())
        print("\n")
    
    def getEnergy(self):
        return self.energy

    def addEnergy(self, amount):
        self.energy += amount
    
    def removeEnergy(self, amount):
        self.energy -= amount
    
    def needsEnergy(self):
        return self.energy < self.targetEnergy
    
    def canEat(self, entity):
        for entityType in self.edibleEntityTypes:
            if type(entity) is entityType:
                return True
        return False
    
    def isLiving(self):
        return self.living