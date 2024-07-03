import copy
import networkx as nx
def cercaPercorso(grafo, v0):
    # Start with the initial vertex
    best_path = []
    visited = set()
    path=[]
    path.append(v0)
    for neighbor in grafo.neighbors(v0):
        if (v0, neighbor) not in visited and controllo(grafo, path, neighbor):
            visited.add((v0, neighbor))
            visited.add((neighbor, v0))
            path.append(neighbor)
            _dfs(grafo, neighbor, path, visited, best_path)
            path.pop()
            visited.remove((v0, neighbor))
            visited.remove((neighbor, v0))
    return best_path


def _dfs( grafo,current, path, visited,best_path):
    best_path.append(copy.deepcopy(path))
    if uscita(path,current,grafo):
        return
    else:
        for neighbor in grafo.neighbors(current):
            if (current,neighbor) not in visited and controllo(grafo,path, neighbor):
                visited.add((current,neighbor))
                visited.add((neighbor,current))
                path.append(neighbor)
                _dfs(grafo,neighbor, path, visited,best_path)
                path.pop()
                visited.remove((current,neighbor))
                visited.remove((neighbor, current))

def uscita(path,current,grafo):
    trovato=True
    archi = [(current, neighbor) for neighbor in grafo[current].keys()]
    for arco in archi:
        if grafo[arco[0]][arco[1]]["weight"]>grafo[path[-1]][path[-2]]['weight']:
            trovato=False
    return trovato


def controllo(grafo, path, neighbor):
        if len(path) == 1:
            return True
        last_edge_weight = grafo[path[-1]][path[-2]]['weight']
        current_edge_weight = grafo[path[-1]][neighbor]['weight']
        return current_edge_weight >= last_edge_weight

edge=[("A","B",2),("A","C",3),("C","B",14),("C","D",12),("B","E",5),("D","E",10)]
grafo=nx.Graph()
grafo.add_weighted_edges_from(edge)
print(cercaPercorso(grafo,"A"))


