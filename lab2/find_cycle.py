import sys


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
            dict_graph[edge[0]].remove(edge[1])
            dict_graph[edge[1]].remove(edge[0])
             
            stack.append(edge[1] if v == edge[0] else edge[0])
    return path


def hamilton(curr, dict_graph, n, Visited, Path):
    node_curr = list(dict_graph.keys())[curr]
    Path.append(node_curr)
    
    if len(Path) == n or len(Path) == 0:
        if Path[-1] in dict_graph[Path[0]]:
            Path.append(Path[0])
            return True 
        else: 
            Path.pop()
            return False 
    Visited[curr] = True
    for next in range(n):
        node_next = list(dict_graph.keys())[next]
        if node_next in dict_graph[node_curr] and not Visited[next]: 
            if hamilton(next, dict_graph, n, Visited, Path): 
                return True 
    Visited[curr] = False
    Path.pop()
    return False


def check_ec (dict_graph):
    return (True if [len(x)%2 == 0 for x in dict_graph.values()] == [True] * len(dict_graph) 
    else [x for x in dict_graph.keys() if len(dict_graph[x]) % 2 == 1])
 
 
def from_file(file_name = "input_default"):
    graph = {}
    with open(file_name, "rb") as file:
        i = -1
        node = None
        edges = 0
        for ln in file:
            num = int(ln)
            if i == -1:
                graph[num] = []
                node = num
            elif i == 0:
                edges = num
            else:
                graph[node].append(num)
            if len(graph[node]) == edges and i != -1:
                i = -1
            else:
                i+=1
    return graph


def main():
    file_name = "input_default"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    graph = from_file(file_name)
    n = len(list(graph.keys()))
    Visited = [False] * n
    Path = []
    if (hamilton(0, graph, n, Visited, Path)):
        print("There's a Hamilton cycle:")
        print(Path)
    else:
        print("There's no Hamilton_cycle")
    if check_ec(graph):
        print("There's an Eulerian cycle:")
        print(find_eulerian_tour(graph))

 

if __name__ == '__main__':
    main()
