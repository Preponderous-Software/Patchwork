from operator import truediv
import random
import pygame
from environment import Environment
from graphik import Graphik


black = (0,0,0)
white = (255,255,255)

displayWidth = 1920
displayHeight = 1080

gridSize = 50

def drawEnvironment(environment, graphik, locationWidth, locationHeight):
    for location in environment.getGrid().getLocations():
        red = random.randrange(50, 200)
        green = random.randrange(50, 200)
        blue = random.randrange(50, 200)
        graphik.drawRectangle(location.getX() * locationWidth, location.getY() * locationHeight, locationWidth, locationHeight, (red,green,blue))

def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    graphik = Graphik(gameDisplay)
    pygame.display.set_caption("Visualizing Environment With Random Colors")

    environment = Environment("Test", gridSize)

    locationWidth = displayWidth/environment.getGrid().getRows()
    locationHeight = displayHeight/environment.getGrid().getColumns()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        gameDisplay.fill(white)
        drawEnvironment(environment, graphik, locationWidth, locationHeight)
        pygame.display.update()

main()