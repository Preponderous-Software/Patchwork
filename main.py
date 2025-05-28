import random
import pygame
from Viron.src.main.python.preponderous.viron.services.environmentService import EnvironmentService
from Viron.src.main.python.preponderous.viron.services.gridService import GridService
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

exit_after_create = False
if len(sys.argv) > 2 and sys.argv[2] == "--exit-after-create":
    exit_after_create = True

class LocationRenderer:
    def __init__(self, graphik):
        self.graphik = graphik

    def draw(self, location, width, height):
        x = location.get_x() * width
        y = location.get_y() * height
        color = self.get_random_color()
        self.graphik.drawRectangle(x - 1, y - 1, width * 1.5, height * 1.5, color)
    
    def get_random_color(self):
        red = random.randrange(50, 200)
        green = random.randrange(50, 200)
        blue = random.randrange(50, 200)
        return (red, green, blue)

class GridRenderer:
    def __init__(self, graphik, url, port):
        self.graphik = graphik
        self.locationService = LocationService(url, port)
        self.location_renderer = LocationRenderer(graphik)
        self.locationsCache = {}
    
    def draw(self, grid):
        gridId = grid.get_grid_id()
        if gridId not in self.locationsCache:
            self.locationsCache[gridId] = self.locationService.get_locations_in_grid(gridId)
        
        locations = self.locationsCache[gridId]
        width = displayWidth / grid.get_columns()
        height = displayHeight / grid.get_rows()
        for location in locations:
            self.location_renderer.draw(location, width, height)

class EnvironmentRenderer:
    def __init__(self, graphik, grid_size, url, port):
        self.graphik = graphik
        self.grid_size = grid_size
        self.grid_service = GridService(url, port)
        self.grid_renderer = GridRenderer(graphik, url, port)

    def draw(self, environment):
        grids = self.grid_service.get_grids_in_environment(environment.getEnvironmentId())
        # assume one grid for now, can be extended later
        if grids:
            self.grid_renderer.draw(grids[0])
        else:
            self.graphik.drawText("No grids found in environment.", displayWidth/2, displayHeight/2, 20, "red")

def loadEnvironmentsFile(env_file):
    if os.path.exists(env_file):
        log("Environments file exists, loading...")
        with open(env_file, "r") as f:
            return json.load(f)
    else:
        log("No existing environments found.")
        return {}

def loadExistingEnvironment(graphik, env_key, environments, environmentService):
    graphik.drawText("Loading existing environment, please wait...", displayWidth/2, displayHeight/2, 20, "white")
    env_id = environments[env_key]["environment_id"]
    try:
        return environmentService.get_environment_by_id(env_id)
    except Exception as e:
        log(f"Error loading existing environment: {e}")
        graphik.drawText("Error loading environment, please check logs.", displayWidth/2, displayHeight/2 + 30, 20, "red")
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        return

def create_environment(graphik, numGrids, gridSize):
    environmentService = EnvironmentService(url, port)
    graphik.drawText("Creating environment, please wait...", 400, 400, 20,"white")
    pygame.display.update()
    log("Creating environment with " + str(numGrids) + " grid(s) of size " + str(gridSize) + "x" + str(gridSize))
    start_time = time.time()
    environment = environmentService.create_environment("Test", numGrids, gridSize)
    end_time = time.time()
    log(f"Created new environment with id {environment.getEnvironmentId()} in {end_time - start_time:.2f} seconds.")
    return environment

def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    graphik = Graphik(gameDisplay)
    pygame.display.set_caption("Visualizing Environment With Random Colors")
 
    env_file = "environments.json"
    environments = {}

    # Load existing environments if file exists
    environments = loadEnvironmentsFile(env_file)

    # Create a unique key for the environment based on grid size and numGrids
    env_key = f"{numGrids}x{gridSize}"
    
    environmentService = EnvironmentService(url, port)

    if env_key in environments:
        log(f"Environment with key {env_key} already exists, loading...")
        environment = loadExistingEnvironment(graphik, env_key, environments, environmentService)
    else:
        log(f"No existing environment found with key {env_key}, creating new one.")
        environment = create_environment(graphik, numGrids, gridSize)
        
        if exit_after_create:
            log("Exiting after environment creation.")
            environmentRenderer = EnvironmentRenderer(graphik, gridSize, url, port)
            environmentRenderer.draw(environment)
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            return

    running = True
    
    environmentRenderer = EnvironmentRenderer(graphik, gridSize, url, port)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        environmentRenderer.draw(environment)
        pygame.display.update()

main()