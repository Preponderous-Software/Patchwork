# Copyright (c) 2022 Preponderous Software
# MIT License


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
import random
import uuid

from entity import Entity
from location import Location


class Grid(object):

    def __init__(self, columns, rows):
        self.id = uuid.uuid4()
        self.columns = columns
        self.rows = rows
        self.locations = []
        self.generateLocations()

    def getID(self):
        return self.id

    def getColumns(self):
        return self.columns

    def getRows(self):
        return self.rows

    def getLocations(self):
        return self.locations

    def getFirstLocation(self):
        return self.locations[0]

    def getSize(self):
        return len(self.locations)
    
    def getLocations(self):
        return self.locations
    
    def getNumEntities(self):
        count = 0
        for location in self.locations:
            count += location.getNumEntities()
        return count
    
    def setID(self, id):
        self.id = id
    
    def setColumns(self, columns):
        self.columns = columns
    
    def setRows(self, rows):
        self.rows = rows
    
    def setLocations(self, locations):
        self.locations = locations
    
    def addLocation(self, location: Location):
        self.locationss.append(location)
    
    def removeLocation(self, location: Location):
        self.locations.remove(location)
    
    def addEntity(self, entity: Entity):
        entity.setGridID(self.getID())
        self.getRandomLocation().addEntity(entity)
    
    def addEntityToLocation(self, entity: Entity, location):
        entity.setGridID(self.getID)
        self.getLocation(location.getID()).addEntity(entity)
    
    def removeEntity(self, entity: Entity):
        for location in self.grid.getLocations():
            if location.isEntityPresent(entity):
                location.removeEntity(entity)
                return
    
    def isEntityPresent(self, entity: Entity):
        for location in self.grid.getLocations():
            if location.isEntityPresent(entity):
                return True

    def generateLocations(self):
        for x in range(self.getColumns()):
            for y in range(self.getRows()):
                location = Location(x, y)
                self.locations.append(location)
    
    def getLocation(self, id):
        for location in self.locations:
            if location.getID() == id:
                return location
        return -1
    
    def getRandomLocation(self):
        index = random.randrange(0, len(self.locations))
        return self.locations[index]
    
    def getLocationByCoordinates(self, x, y):
        for location in self.locations:
            if location.getX() == x and location.getY() == y:
                return location
        return -1

    def getUp(self, location: Location):
        return self.getLocationByCoordinates(location.getX(), location.getY() - 1)
    
    def getRight(self, location: Location):
        return self.getLocationByCoordinates(location.getX() + 1, location.getY())
    
    def getDown(self, location: Location):
        return self.getLocationByCoordinates(location.getX(), location.getY() + 1)
    
    def getLeft(self, location: Location):
        return self.getLocationByCoordinates(location.getX() - 1, location.getY())
