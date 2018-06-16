import click

from map_utils import load_map

#TODO: add help docs
@click.command
@click.option("--alg", default=None) # TODO: provide options
@click.option("--draw", default=False, is_flag=True)
@click.option("--log", default=False, is_flag=True)
@click.option("--time", default=False, is_flag=True)
@click.argument("input_file",
		 help="The filepath to the input map CSV")
def main(alg, draw, log, filename):

	route = load_map(filename)

	# if alg: ...

	print(route)

	if draw:
		pass # TODO: matplotlib stuff
	

if __name__ == "__main__":
	main()