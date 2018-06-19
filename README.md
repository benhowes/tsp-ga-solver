
TSP solver exercise
====

This exercise is a solution to the programming challenge which was used at Zoetrope Ltd from 2016->2018 to get candidates to demonstrate coding abilites (see `challenge_brief.md`). Now that we don't use the challenge any more, this is an example submission, with a genetic algorithm to show how a better solution may be achieved.

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

Running tests:
```
PYTHONPATH=. py.test -v
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

#### Genetic Algorithm `--alg=ga`
The genetic algorithm implementation has been done to demonstrate how a GA works more than to
perform well enough to be practical to use.

When run, this will run 5000 generations (which takes a lot longer than 60 seconds specified in the brief)
to run a GA with cyclic crossover and random swap mutations.

Currently random starting solution genomes are used, however this can be improved by using NN or another hueristic
for the starting genomes.