
TSP solver exercise
====

Running
---

Requires python 3.6 and pipenv


Installation:

```
pipenv --python 3.6
pipenv install
```

Running:

```
pipenv shell #Only needed once per session
python -m solver.solver <map path> --alg=<alg name>
```


Available Algorithms
---

#### Shuffle `--alg=shuffle`
The most simple algorithm simply produces a shuffled route.

#### Nearest Neighbour `--alg=nn`
This algorithm produces a route by hopping to the nearest unvisited neighbour until
all have been visited.

This loops over all nodes, and for each of those calulates the distance to the
next nearest node, giving an `O(n*log(n))` run time