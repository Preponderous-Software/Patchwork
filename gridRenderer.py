from Viron.src.main.python.preponderous.viron.services.locationService import LocationService
from graphik import Graphik
from locationRenderer import LocationRenderer


class GridRenderer:
    def __init__(self, graphik: Graphik, url, port):
        self.graphik = graphik
        self.locationService = LocationService(url, port)
        self.location_renderer = LocationRenderer(graphik)
        self.locationsCache = {}
    
    def draw(self, grid):
        gridId = grid.get_grid_id()
        if gridId not in self.locationsCache:
            self.locationsCache[gridId] = self.locationService.get_locations_in_grid(gridId)
        
        locations = self.locationsCache[gridId]
        width = self.graphik.getGameDisplay().get_width() / grid.get_columns()
        height = self.graphik.getGameDisplay().get_height() / grid.get_rows()
        for location in locations:
            self.location_renderer.draw(location, width, height)
