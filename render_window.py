import pygame

#  @author Daniel McCoy Stephenson
#  @since October 2nd, 2025
class RenderWindow:
    """
    RenderWindow class encapsulates Pygame window initialization and management.
    Designed for composition, not inheritance - use as a container for rendering.
    
    Manages:
    - Pygame initialization
    - Window creation and display surface
    - Event loop processing
    - Frame rate control
    - Custom event handlers
    """
    
    def __init__(self, title, width, height):
        """
        Initialize the RenderWindow with the specified title and dimensions.
        
        Args:
            title (str): Window title
            width (int): Window width in pixels
            height (int): Window height in pixels
        """
        pygame.init()
        self._surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self._clock = pygame.time.Clock()
        self._running = True
        self._event_handlers = []
    
    def get_surface(self):
        """
        Get the display surface for rendering.
        
        Returns:
            pygame.Surface: The display surface
        """
        return self._surface
    
    def tick(self, fps):
        """
        Control the frame rate by limiting the number of frames per second.
        
        Args:
            fps (int): Target frames per second
        """
        self._clock.tick(fps)
    
    def should_continue(self):
        """
        Process events and check if the window should continue running.
        Handles QUIT events internally and calls registered event handlers.
        
        Returns:
            bool: True if the window should continue running, False otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            else:
                # Call all registered event handlers
                for handler in self._event_handlers:
                    handler(event)
        
        return self._running
    
    def register_event_handler(self, handler):
        """
        Register a custom event handler function.
        The handler will be called for each event (except QUIT which is handled internally).
        
        Args:
            handler (callable): A function that takes a pygame.Event as parameter
        """
        self._event_handlers.append(handler)
