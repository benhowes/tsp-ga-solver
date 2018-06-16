from solver.map_utils import Route
from .base import RouteAlgorithm

class ShuffleRouteAlg(RouteAlgorithm):
    """Returns a new random route """

    cli_name = "shuffle"

    def get_route(self, route: Route) -> Route:
        return route.shuffle()