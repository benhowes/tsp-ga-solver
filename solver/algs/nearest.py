import logging

from solver.map_utils import Route
from .base import RouteAlgorithm

logger = logging.getLogger(__name__)

class NearestRouteAlg(RouteAlgorithm):
    """Creates a route by visiting each nearest neighbour in turn"""

    cli_name = "nn"

    def get_route(self, route: Route) -> Route:
        """
    
        """
        nn_route = Route()

        # initialize by picking a starting point
        current_point = route.pop(0)

        while len(route):
            nn_route.add(current_point)

            # 1. create a list of tuples with the point and the distance
            # 2. pick the closest
            # 3. remove that from the source route and add to the new route 
            distances = [(other, current_point.distance(other)) for other in route]
            next_point, distance = min(distances, key=lambda x: x[1])
            route.remove(next_point)
            current_point = next_point

        return nn_route