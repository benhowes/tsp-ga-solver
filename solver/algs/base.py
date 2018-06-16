

class RouteAlgorithm():
    """Route Algorithms are used to determine an order of points to visit.

    This base class defines the interface and methods which abstract the 
    implementation.
    
    all classes must have a `cli_name` string and a `get_route` method
    """

    cli_name :str = "none"

    def get_route(self):
        raise NotImplementedError("get_route needs to be implemented in a subclass")