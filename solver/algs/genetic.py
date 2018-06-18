import logging
import random

from solver.map_utils import Route
from .base import RouteAlgorithm

logger = logging.getLogger(__name__)

class GeneticRouteAlg(RouteAlgorithm):
    """Creates a route by visiting each nearest neighbour in turn"""

    cli_name = "ga"

    # ---------------------
    # Variables for running
    # ---------------------

    # The number of iterations
    loops = 10000

    # The number of chromosomes (Routes in this case) which make up the
    # population for each round
    population_size = 20

    # The probability that a child will be mutated
    mutation_prob = 0.1

    # The number of top ranking chromosomes which will "survive" each round
    # The top n survivors will be randomly combined to create a new population
    iteration_survivors = 6

    # ---------------------

    def ranked_population(self) -> list:
        """Return the best N chromosomes

        Args:
            n (int) - The number of chromosomes to return

        Returns:
            list[Route] - the best n routes
        """
        ranked = sorted(self.population, key=lambda x: x.total_distance)
        return ranked

    def get_seed_chromosome(self, route):
        """Creates a random chrosome, from the starting route.

        This calls the shuffle algorithm
        """
        return route.shuffle()

    def setup(self, route):
        """Sets up the starting condition for the GA"""

        self.starting_route = route
        self.population = [self.get_seed_chromosome(route) for _ in range(self.population_size)]

    def store_best(self, iteration :int = 0):
        self.best_chromosome = self.ranked_population().pop(0)
        self.best_chromosome_iter = iteration
        print("{}: Best route so far: {}".format(iteration, self.best_chromosome))

    def get_random_parents(self) -> list:
        """Gets 2 random parents.

        Returns:
            list[Route] - A list containing 2 random surviving chromosomes
        """
        ranked = self.ranked_population()
        survivors = ranked[:self.iteration_survivors]
        parent_a = random.choice(survivors)
        survivors.remove(parent_a)
        parent_b = random.choice(survivors)
        return [parent_a, parent_b]

    def combine_get_cycles(self, parent_a: Route, parent_b: Route) -> list:
        """Gets the loops from 2 parents. This is done using the method described here:
        http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/CycleCrossoverOperator.aspx
        """
        seen = [False] * len(parent_a) # Tracks which parts have been seen
        cycles = []

        for cycle_start in range(len(parent_a)):
            if not seen[cycle_start]:

                cycle = [cycle_start]
                seen[cycle_start] = True
                index = parent_a.index(parent_b[cycle_start])

                while index != cycle_start:
                    cycle.append(index)
                    seen[index] = True
                    index = parent_a.index(parent_b[index])

                cycles.append(cycle)
        return cycles

    def combine(self, parent_a: Route, parent_b: Route) -> list:
        """Uses Cyclic Crossover to combine 2 parents"""
        cycles = self.combine_get_cycles(parent_a, parent_b)

        child_a = [False]*len(parent_a)
        child_b = [False]*len(parent_a)

        # Use alternate loops
        for i, cycle in enumerate(cycles):
            for index in cycle:
                if i % 2:
                    child_a[index] = parent_a[index]
                    child_b[index] = parent_b[index]
                else:
                    child_a[index] = parent_b[index]
                    child_b[index] = parent_a[index]

        child_a = Route(child_a)
        child_b = Route(child_b)
        return [child_a, child_b]

    def maybe_mutate(self, route: Route) -> Route:
        """Uses `self.mutation_prob` to decide if a random swapping of 2 nodes should be
            performed

            The swapping picks two locations, ensuring that one is greater than the
            other, then uses array slicing (of Routes) to create a new route, e.g.

            [  1  ,  2  ,  3  ,  4  ,  5  ]
                     A           B

            The result will be:

            [  1  ,  4  ,  3  ,  2  ,  5  ]

            This is done occasionally to help prevent the solution being stuck
            in a local minima.
            """
        if random.random() < self.mutation_prob:
            swap_a = random.randrange(len(route) - 1)
            swap_b = swap_a+1#random.randrange(swap_a+1,len(route))
            new_route = route[:swap_a] | route[swap_b:swap_b] | route[swap_a + 1:swap_b] | route[swap_b+1:]
            return new_route
        return route

    def get_route(self, route: Route) -> Route:
        """ Performs a number of iterations of the genetic algorithm to help
        hone in on better and better solutions to the route.

        Args:
            route (Route) - The starting route

        Returns:
            Route - The best route from the algorithm
        """
        self.setup(route)

        for n in range(self.loops):

            # Generate a new population
            # Keep the best 2
            new_population = self.ranked_population()[:2]

            #import ipdb; ipdb.set_trace()
            while len(new_population) < self.population_size:
                parents = self.get_random_parents()
                new_population += self.combine(*parents)
            self.population = new_population

            # Mutate some children
            for route in self.population:
                self.maybe_mutate(route)

            # store the best
            self.store_best(n)

        return self.best_chromosome