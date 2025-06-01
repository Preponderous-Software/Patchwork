from Viron.src.main.python.preponderous.viron.models.grid import Grid
from Viron.src.main.python.preponderous.viron.services.locationService import LocationService
from graphik import Graphik
from locationRenderer import LocationRenderer


class GridRenderer:
    def __init__(self, graphik: Graphik, url: str, port: int):
        self.graphik = graphik
        self.location_service = LocationService(url, port)
        self.location_renderer = LocationRenderer(graphik)
        self.locations_cache = {}
    
    def draw(self, grid: Grid):
        grid_id = grid.get_grid_id()
        if grid_id not in self.locations_cache:
            self.locations_cache[grid_id] = self.location_service.get_locations_in_grid(grid_id)
        
        locations = self.locations_cache[grid_id]
        width = self.graphik.getGameDisplay().get_width() / grid.get_columns()
        height = self.graphik.getGameDisplay().get_height() / grid.get_rows()
        for location in locations:
            self.location_renderer.draw(location, width, height)
