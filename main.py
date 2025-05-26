import random
import pygame
from Viron.src.main.python.preponderous.viron.services.environmentService import EnvironmentService
from Viron.src.main.python.preponderous.viron.services.locationService import LocationService
from graphik import Graphik
import os
import json
import sys
import time


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
exit_after_create = False
if len(sys.argv) > 2 and sys.argv[2] == "--exit-after-create":
    exit_after_create = True
def drawEnvironment(locations, graphik, locationWidth, locationHeight):
    for location in locations:
        red = random.randrange(50, 200)
        green = random.randrange(50, 200)
        blue = random.randrange(50, 200)
        graphik.drawRectangle(location.get_x() * locationWidth, location.get_y() * locationHeight, locationWidth, locationHeight, (red,green,blue))

def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    graphik = Graphik(gameDisplay)
    pygame.display.set_caption("Visualizing Environment With Random Colors")
 
    env_file = "environments.json"
    environments = {}

    # Load existing environments if file exists
    if os.path.exists(env_file):
        log("Environments file exists, loading...")
        with open(env_file, "r") as f:
            environments = json.load(f)

    # Create a unique key for the environment based on grid size and numGrids
    env_key = f"{numGrids}x{gridSize}"

    if env_key in environments:
        graphik.drawText("Loading existing environment, please wait...", displayWidth/2, displayHeight/2, 20, "white")
        env_id = environments[env_key]["environment_id"]
        try:
         environment = environmentService.get_environment_by_id(env_id)
         log(f"Loaded existing environment with id {env_id} and size {gridSize}x{gridSize} with {numGrids} grid(s).")
        except Exception as e:
            log(f"Error loading existing environment: {e}")
            graphik.drawText("Error loading environment, please check logs.", displayWidth/2, displayHeight/2 + 30, 20, "red")
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            return
    else:
        graphik.drawText("Creating environment, please wait...", 400, 400, 20,"white")
        pygame.display.update()
        log("Creating environment with " + str(numGrids) + " grid(s) of size " + str(gridSize) + "x" + str(gridSize))
        start_time = time.time()
        environment = environmentService.create_environment("Test", numGrids, gridSize)
        end_time = time.time()
        environments[env_key] = {
            "environment_id": environment.getEnvironmentId(),
            "grid_size": gridSize,
            "num_grids": numGrids,
            "creation_time_seconds": end_time - start_time
        }
        with open(env_file, "w") as f:
            json.dump(environments, f, indent=2)
        log(f"Created new environment with id {environment.getEnvironmentId()} in {end_time - start_time:.2f} seconds.")
        
        if exit_after_create:
            log("Exiting after environment creation.")
            locations = locationService.get_locations_in_environment(environment.getEnvironmentId())
            drawEnvironment(locations, graphik, displayWidth/gridSize, displayHeight/gridSize)
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            return

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