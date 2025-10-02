#!/usr/bin/env python3
"""
Example demonstrating RenderWindow usage in the Patchwork context.
This shows how to refactor main.py to use RenderWindow instead of raw Pygame calls.
"""

import random
import pygame
from render_window import RenderWindow
from graphik import Graphik

# Example 1: Simple usage replacing raw Pygame initialization
def simple_example():
    """Demonstrates basic RenderWindow usage"""
    # Instead of:
    #   pygame.init()
    #   gameDisplay = pygame.display.set_mode((800, 800))
    #   pygame.display.set_caption("Title")
    
    # Use RenderWindow:
    window = RenderWindow("Simple Example", 800, 800)
    surface = window.get_surface()
    
    # Create Graphik instance with the surface
    graphik = Graphik(surface)
    
    # Main loop - instead of manual event handling
    while window.should_continue():
        surface.fill((255, 255, 255))
        graphik.drawText("RenderWindow Example", 400, 400, 30, (0, 0, 0))
        pygame.display.update()
        window.tick(60)
    
    pygame.quit()


# Example 2: With custom event handlers
def event_handler_example():
    """Demonstrates custom event handler registration"""
    window = RenderWindow("Event Handler Example", 800, 800)
    surface = window.get_surface()
    graphik = Graphik(surface)
    
    # State
    click_count = [0]
    
    # Custom event handler
    def handle_mouse_click(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_count[0] += 1
            print(f"Mouse clicked! Total clicks: {click_count[0]}")
    
    # Register the handler
    window.register_event_handler(handle_mouse_click)
    
    # Main loop
    while window.should_continue():
        surface.fill((255, 255, 255))
        graphik.drawText(f"Clicks: {click_count[0]}", 400, 400, 30, (0, 0, 0))
        graphik.drawText("Click anywhere or close window", 400, 450, 20, (100, 100, 100))
        pygame.display.update()
        window.tick(60)
    
    pygame.quit()


# Example 3: Integration pattern for main.py
def integration_example():
    """
    Shows how main.py could be refactored to use RenderWindow.
    
    The refactored main() function would replace:
        pygame.init()
        gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
        pygame.display.set_caption("Visualizing Environment With Random Colors")
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
    
    With:
        window = RenderWindow("Visualizing Environment With Random Colors", displayWidth, displayHeight)
        surface = window.get_surface()
        graphik = Graphik(surface)
        
        while window.should_continue():
            # ... existing drawing code ...
            window.tick(60)  # Optional: add frame rate limiting
    """
    displayWidth = 800
    displayHeight = 800
    
    # Create window using RenderWindow
    window = RenderWindow("Visualizing Environment With Random Colors", displayWidth, displayHeight)
    surface = window.get_surface()
    graphik = Graphik(surface)
    
    # Example: drawing random rectangles (simulating environment visualization)
    white = (255, 255, 255)
    
    while window.should_continue():
        surface.fill(white)
        
        # Draw some example content
        for i in range(10):
            for j in range(10):
                red = random.randrange(50, 200)
                green = random.randrange(50, 200)
                blue = random.randrange(50, 200)
                x = i * (displayWidth / 10)
                y = j * (displayHeight / 10)
                graphik.drawRectangle(x, y, displayWidth / 10, displayHeight / 10, (red, green, blue))
        
        pygame.display.update()
        window.tick(60)  # Limit to 60 FPS
    
    pygame.quit()


if __name__ == "__main__":
    print("RenderWindow Usage Examples")
    print("=" * 60)
    print("1. Simple example")
    print("2. Event handler example")
    print("3. Integration example (simulates main.py refactoring)")
    print()
    choice = input("Select example (1-3): ").strip()
    
    if choice == "1":
        simple_example()
    elif choice == "2":
        event_handler_example()
    elif choice == "3":
        integration_example()
    else:
        print("Invalid choice. Running integration example by default.")
        integration_example()
