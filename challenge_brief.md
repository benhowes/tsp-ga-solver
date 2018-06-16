Routing problem
---

In the /maps folder you will find 3 different maps in 2D space. These CSV files are defined as a node number, followed by the (X,Y) coordinates of that point in space. Let's assume the units of the distances is in KM.

To get an idea of what one of these files would look like as a graph, see `map_a.png`.

We'd like you to create a python program which:

1. Reads in one of these files (selectable by command line arguments)
2. Generates a random route which visits each of the points. It does not matter which node is the starting node, nor how many times each is visited, so long as a route which visits all is generated.
3. prints out a formatted list of the order in which the points are visited in your random solution
4. prints the total length of the distance between points.

Finding the route between these points which minimises the total distance is the classic travelling salesman problem. As a follow on to the initial part, we'd love to see a small implementation of a heuristic which helps to find routes which tend to be shorter than the maximum - though the program should not take more than (approximately) 1 minute to run.

What we're looking for:
1. Good understanding of the abstract problem
2. Coding style - we'd like to see you make use of libraries and not reinvent the wheel.
3. Coding docs / testing
4. Creative thinking on the heuristics

Please don't spend more than 4 hours on this problem and do regard the route heuristics as entirely optional.

Please submit to us a zip/gzip containing:

1. Your code
2. Instructions on running