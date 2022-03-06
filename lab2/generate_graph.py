import random
import sys


def generate_graph (n = 10):
    max = n + 100
    list_nodes = []
    node = 0
    dict_graph = {}
    for i in range(n):
        node = random.randint(0, max)
        while node in list_nodes:
            node = random.randint(0, max)
        #node = i
        list_nodes.append(node)
        dict_graph[node] = []
    for node in list_nodes:
        list_edges = [] * n
        for i in range(n):
            if random.randint(0, max) % 2:
                edge = list_nodes[random.randint(0, n - 1)]
                if not edge in list_edges and edge != node and not node in dict_graph[edge]:
                    dict_graph[node].append(edge)
                    dict_graph[edge].append(node)
        
    return dict_graph


def write_int(num, file):
    str_num = str(num) + '\n'
    bt = str_num.encode()
    file.write(bt)


def to_file(graph, file_name = "input"):
    with open(file_name, "wb") as file:
        for node in graph:
            write_int(node, file)
            write_int(len(graph[node]), file)
            for edge in graph[node]:
                write_int(edge, file)


def gen():
    n = 10
    file_name = "input"
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    if len(sys.argv) > 2:
        file_name = sys.argv[2]
    graph = generate_graph(n)
    to_file(graph, file_name)


gen()