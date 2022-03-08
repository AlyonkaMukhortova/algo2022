# LAB2: Random generator of graphs and checking if there're Hamiltonian and Eulerian cycles

### generate_graph.py
Usage:

python3 generate_graph.py num_of_nodes file_name

- Default file name - input
- Default num of nodes - 5
- Num of graph edges is random from 0 to max

Output:

binary file with generated graph

### find_cycle.py
Usage:

python3 find_cycle.py file_name

- Default file_name - input_default

Output:

In console there'll be information if there're Hamiltonian and Eulerian cycles

If true, cycles will be printed

Example:

There's no  Hamiltonian cycle

There's an Eulerian cycle:

[node1, node2, ..., node l]

### input_default

Default input file used in find_cycle.py

Format of file:

*Node name + '\n'
Num of edges + '\n'
1st edge node + '\n'
...
n-th edge node + '\n'*

**for each node of graph**