from operator import truediv
import random
import pygame
from Viron.src.main.python.preponderous.viron.models.location import Location
from Viron.src.main.python.preponderous.viron.services.environmentService import EnvironmentService
from Viron.src.main.python.preponderous.viron.services.locationService import LocationService
from graphik import Graphik
import os
import json
import sys


black = (0,0,0)
white = (255,255,255)

displayWidth = 800
displayHeight = 800

def log(message):
    print(message)

numGrids = 1
if len(sys.argv) > 1:
    try:
        gridSize = int(sys.argv[1])
    except ValueError:
        log("Invalid grid size argument, using default of 50.")
        gridSize = 50
else:
    gridSize = 50

url = "http://localhost"
port = 9999

locationService = LocationService(url, port)
environmentService = EnvironmentService(url, port)

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
 
    env_file = "environment.json"

    if os.path.exists(env_file):
        log("Environment file exists, loading...")
        with open(env_file, "r") as f:
            data = json.load(f)
            env_id = data.get("environment_id")
            saved_grid_size = data.get("grid_size")
            saved_num_grids = data.get("num_grids")
            if saved_grid_size == gridSize and saved_num_grids == numGrids:
                environment = environmentService.get_environment_by_id(env_id)
                log(f"Loaded existing environment with id {env_id} and size {saved_grid_size}x{saved_grid_size} with {saved_num_grids} grid(s).")
            else:
                log("Environment size does not match, creating new environment.")
                environment = environmentService.create_environment("Test", numGrids, gridSize)
                with open(env_file, "w") as fw:
                    json.dump({
                        "environment_id": environment.getEnvironmentId(),
                        "grid_size": gridSize,
                        "num_grids": numGrids
                    }, fw)
                log(f"Created new environment with id {environment.getEnvironmentId()}")
    else:
        log("Creating environment with " + str(numGrids) + " grid(s) of size " + str(gridSize) + "x" + str(gridSize))
        environment = environmentService.create_environment("Test", numGrids, gridSize)
        with open(env_file, "w") as f:
            json.dump({
                "environment_id": environment.getEnvironmentId(),
                "grid_size": gridSize,
                "num_grids": numGrids
            }, f)
        log(f"Created new environment with id {environment.getEnvironmentId()}")

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