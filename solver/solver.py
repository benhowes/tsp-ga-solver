import click

from map_utils import load_map

#TODO: add help docs
@click.command()
@click.option("--alg", default=None) # TODO: provide options
@click.option("--draw", default=False, is_flag=True)
@click.option("--log", default=False, is_flag=True)
@click.option("--time", default=False, is_flag=True)
@click.argument("map_file")
def main(alg, draw, log, time, map_file):

    route = load_map(map_file)

    # if alg: ...
    print(route)

    route = route.shuffle()
    print(route)

    if draw:
        pass # TODO: matplotlib stuff
    

if __name__ == "__main__":
    main()