
from .base import RouteAlgorithm
from .shuffle import ShuffleRouteAlg
from .nearest import NearestRouteAlg
from .genetic import GeneticRouteAlg

registered_algs = [
    RouteAlgorithm,
    ShuffleRouteAlg,
    NearestRouteAlg,
    GeneticRouteAlg,
]

class AlgorithmNotFoundException(Exception):
    pass

def get_algorithm(name: str) -> RouteAlgorithm:
    """ Resolve a route algorithm from the list
        of registered algorithms.
    """
    for alg in registered_algs:
        if alg.cli_name == name:
            return alg

    raise AlgorithmNotFoundException("No algorithm called %s", name)

__all__ = [
    'get_algorithm'
]