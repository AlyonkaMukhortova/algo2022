import random


def find_eulerian_tour(dict_graph):
    stack = []
    path = []
 
    stack.append(list(dict_graph.keys())[0])
 
    while len(stack) > 0:
        v = stack[len(stack) - 1]
 
        degree = len(dict_graph[v])
        if degree == 0:
            stack.pop()
            path.append(v)
        else:
            edge = (v, dict_graph[v][0])
            #print(degree, v, dict_graph[edge[0]], dict_graph[edge[1]], edge)
            dict_graph[edge[0]].remove(edge[1])
            dict_graph[edge[1]].remove(edge[0])
             
            stack.append(edge[1] if v == edge[0] else edge[0])
    return path


n = 4
Visited = [False] * n
Path = []
def hamilton(curr, dict_graph):
    node_curr = list(dict_graph.keys())[curr]
    Path.append(node_curr)
    if len(Path) == n:
        if Path[-1] in dict_graph[Path[0]]:
            return True 
        else: 
            Path.pop()
            return False 
    Visited[curr] = True
    for next in range(n):
        node_next = list(dict_graph.keys())[next]
        if node_next in dict_graph[node_curr] and not Visited[next]: 
            if hamilton(next, dict_graph): 
                return True 
    Visited[curr] = False
    Path.pop()
    return False


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
                if not edge in list_edges and edge != node:
                    dict_graph[node].append(edge)
                    dict_graph[edge].append(node)
        
    return dict_graph




def check_ec (dict_graph):
    return (True if [len(x)%2 == 0 for x in dict_graph.values()] == [True] * len(dict_graph) 
    else [x for x in dict_graph.keys() if len(dict_graph[x]) % 2 == 1])
 
 
graph = [(0, 1), (1, 5), (1, 7), (4, 5),
(4, 8), (1, 6), (3, 7), (5, 9),
(2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]

dict_graph = {0 : [1, 4], 1 : [0, 5, 7, 6],
 2 : [4, 5], 3 : [7, 6], 4 : [5, 8, 2, 0], 5 : [1, 4, 9, 2], 
 6 : [1, 3], 7 : [1, 3], 8: [4, 9], 9 : [5, 8]}

dict_graph1 = {0 : [1, 3], 1 : [0, 2],
2 : [1, 3], 3 : [0, 2]}
 
print((find_eulerian_tour(dict_graph)))
print (check_ec(dict_graph))
print(hamilton(0, dict_graph1))
print(Path)
dict_graph = generate_graph()
print(dict_graph)
print(hamilton(0, dict_graph1))
print (check_ec(dict_graph))
print((find_eulerian_tour(dict_graph)))
