from operator import truediv
import random
import pygame
from environment import Environment
from environmentService import EnvironmentService
from graphik import Graphik
from locationService import ServiceConfig
from locationService import LocationService
from location import Location


black = (0,0,0)
white = (255,255,255)

displayWidth = 600
displayHeight = 600

numGrids = 1
gridSize = 50

url = "http://localhost"
port = 9999

locationServiceConfig = ServiceConfig(viron_host=url, viron_port=port)
locationService = LocationService(locationServiceConfig)

environmentServiceBaseUrl = f"{url}:{port}"
environmentService = EnvironmentService(environmentServiceBaseUrl)

def log(message):
    print(message)

def drawEnvironment(locations, graphik, locationWidth, locationHeight):
    for location in locations:
        location = Location(location_id=location['locationId'], x=location['x'], y=location['y'])
        red = random.randrange(50, 200)
        green = random.randrange(50, 200)
        blue = random.randrange(50, 200)
        graphik.drawRectangle(location.get_x() * locationWidth, location.get_y() * locationHeight, locationWidth, locationHeight, (red,green,blue))

def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    graphik = Graphik(gameDisplay)
    pygame.display.set_caption("Visualizing Environment With Random Colors")
 
    log("Creating environment with " + str(numGrids) + " grid(s) of size " + str(gridSize) + "x" + str(gridSize))
    environment = environmentService.create_environment("Test", numGrids, gridSize)

    locationWidth = displayWidth/gridSize
    locationHeight = displayHeight/gridSize
    
    locationsCache = {}

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        if locationsCache == {}:
            log("Fetching locations from service...")
            locationsCache = locationService.get_locations_in_environment(environment.getEnvironmentId())
            
        gameDisplay.fill(white)
        drawEnvironment(locationsCache, graphik, locationWidth, locationHeight)
        pygame.display.update()

main()