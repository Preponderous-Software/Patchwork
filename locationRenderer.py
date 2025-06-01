import random


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