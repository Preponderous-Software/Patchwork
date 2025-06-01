import pygame
from Viron.src.main.python.preponderous.viron.services.environmentService import EnvironmentService
from environmentRenderer import EnvironmentRenderer
from graphik import Graphik
import os
import json
import sys
import time


black = (0,0,0)
white = (255,255,255)

display_width = 800
display_height = 800

def log(message):
    print(message)

num_grids = 1
if len(sys.argv) > 1:
    try:
        grid_size = int(sys.argv[1])
    except ValueError:
        log("Invalid grid size argument, using default of 50.")
        grid_size = 50
else:
    grid_size = 50

url = "http://localhost"
port = 9999

exit_after_create = False
if len(sys.argv) > 2 and sys.argv[2] == "--exit-after-create":
    exit_after_create = True

def load_environments_file(env_file):
    if os.path.exists(env_file):
        log("Environments file exists, loading...")
        with open(env_file, "r") as f:
            return json.load(f)
    else:
        log("No existing environments found.")
        return {}

def load_existing_environment(graphik, env_key, environments, environmentService):
    graphik.drawText("Loading existing environment, please wait...", display_width/2, display_height/2, 20, "white")
    env_id = environments[env_key]["environment_id"]
    try:
        return environmentService.get_environment_by_id(env_id)
    except Exception as e:
        log(f"Error loading existing environment: {e}")
        graphik.drawText("Error loading environment, please check logs.", display_width/2, display_height/2 + 30, 20, "red")
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        return

def create_environment(graphik, num_grids, grid_size):
    environmentService = EnvironmentService(url, port)
    graphik.drawText("Creating environment, please wait...", 400, 400, 20,"white")
    pygame.display.update()
    log("Creating environment with " + str(num_grids) + " grid(s) of size " + str(grid_size) + "x" + str(grid_size))
    start_time = time.time()
    environment = environmentService.create_environment("Test", num_grids, grid_size)
    end_time = time.time()
    log(f"Created new environment with id {environment.getEnvironmentId()} in {end_time - start_time:.2f} seconds.")
    
    return environment, start_time, end_time

def main():
    pygame.init()
    game_display = pygame.display.set_mode((display_width, display_height))
    graphik = Graphik(game_display)
    pygame.display.set_caption("Visualizing Environment With Random Colors")
 
    env_file = "environments.json"
    environments = {}

    # Load existing environments if file exists
    environments = load_environments_file(env_file)

    # Create a unique key for the environment based on grid size and numGrids
    env_key = f"{num_grids}x{grid_size}"
    
    environment_service = EnvironmentService(url, port)

    if env_key in environments:
        log(f"Environment with key {env_key} already exists, loading...")
        environment = load_existing_environment(graphik, env_key, environments, environment_service)
    else:
        log(f"No existing environment found with key {env_key}, creating new one.")
        environment, start_time, end_time = create_environment(graphik, num_grids, grid_size)
        
        environments[env_key] = {
            "environment_id": environment.getEnvironmentId(),
            "grid_size": grid_size,
            "num_grids": num_grids,
            "creation_time_seconds": end_time - start_time
        }
        with open(env_file, "w") as f:
            json.dump(environments, f, indent=2)
        
        if exit_after_create:
            log("Exiting after environment creation.")
            environment_renderer = EnvironmentRenderer(graphik, url, port)
            environment_renderer.draw(environment)
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            return

    running = True
    
    environment_renderer = EnvironmentRenderer(graphik, url, port)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        game_display.fill(white)
        environment_renderer.draw(environment)
        pygame.display.update()
        
        time.sleep(0.1)

main()