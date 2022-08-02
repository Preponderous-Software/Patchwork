# Copyright (c) 2022 Preponderous Software
# MIT License


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
import uuid

from entity import Entity


class Location(object):

    def __init__(self, x, y):
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.entities = []
    
    def getID(self):
        return self.id
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def getNumEntities(self):
        return len(self.entities)
    
    def addEntity(self, entity: Entity):
        if not self.isEntityPresent(entity):
            self.entities.append(entity)
            entity.setLocationID(self.getID())
        else:
            print("Warning: An entity was already present when attempting to add it to a location.")
    
    def removeEntity(self, entity: Entity):
        if self.isEntityPresent(entity):
            self.entities.remove(entity)
        else:
            print("Warning: An entity was not present when attempting to remove it from a location.")
    
    def isEntityPresent(self, entity: Entity):
        return entity in self.entities
    
    def getEntities(self):
        return self.entities