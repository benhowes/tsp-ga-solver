import sys
import click
import logging

from solver.map_utils import load_map
from solver.algs import get_algorithm

logger = logging.getLogger(__name__)

#TODO: add help docs
@click.command()
@click.option("--alg", default=None) # TODO: provide options
@click.option("--draw", default=False, is_flag=True)
@click.option("--log", default=False, is_flag=True)
@click.option("--time", default=False, is_flag=True)
@click.argument("map_file")
def main(alg, draw, log, time, map_file):

    if log:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)

    route = load_map(map_file)

    if not alg:
        print("A valid --alg name is required")
        sys.exit(1)

    router_algorithm = get_algorithm(alg)
    logger.info("Loaded algorithm %s", alg)
    new_route = router_algorithm().get_route(route)

    print(new_route)

    if draw:
        pass # TODO: matplotlib stuff
    

if __name__ == "__main__":
    main()