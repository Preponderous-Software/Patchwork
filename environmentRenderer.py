from Viron.src.main.python.preponderous.viron.services.gridService import GridService
from graphik import Graphik
from gridRenderer import GridRenderer


class EnvironmentRenderer:
    def __init__(self, graphik: Graphik, url, port):
        self.graphik = graphik
        self.grid_service = GridService(url, port)
        self.grid_renderer = GridRenderer(graphik, url, port)

    def draw(self, environment):
        grids = self.grid_service.get_grids_in_environment(environment.getEnvironmentId())
        # assume one grid for now, can be extended later
        if grids:
            self.grid_renderer.draw(grids[0])
        else:
            self.graphik.drawText("No grids found in environment.", self.graphik.getGameDisplay().get_width()/2, self.graphik.getGameDisplay().get_height()/2, 20, "red")