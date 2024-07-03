import copy
import networkx as nx
from database.DAO import DAO
import matplotlib.pyplot as plt
class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._colori = DAO.getColore()
        self._anni=DAO.getAnni()
        self._prodotti=[]

    @property
    def Anni(self):
        return self._anni
    @property
    def Colori(self):
        return self._colori

    def creaGrafo(self, colore, anno):
        self._prodotti = DAO.getProdotti(colore)
        for v in self._prodotti:
            self._idMap[v.Product_number] = v
        self._grafo.add_nodes_from(self._prodotti)
        self.addEdges(anno, colore)
        return self._grafo

    def getProdotti(self,colore):
        if len(self._prodotti)==0:
            return DAO.getProdotti(colore)
        else:
            return self._prodotti

    def addEdges(self, anno, colore):
        self.coppie = DAO.getCombinazioneProdotti(anno, colore)
        for tupla in self.coppie:
            u_partenza = self._idMap[tupla.Product_number1]
            u_finale = self._idMap[tupla.Product_number2]
            self._grafo.add_edge(u_partenza, u_finale, weight=tupla.Conteggio)

    def numEdges(self):
        return len(self._grafo.edges)

    def numNodes(self):
        return len(self._grafo.nodes)

    def calcolaStatistiche(self):
        listaArchi = self._grafo.edges(data=True)
        lista = sorted(listaArchi, key=lambda v: v[2]["weight"], reverse=True)
        #print(lista[0:3])
        return lista[0:3]

    def calcoloMaggiore(self, lista):
        codici = []
        ripetuti = set()
        for elemento in lista:
            codici.append(elemento[0].Product_number)
            codici.append(elemento[1].Product_number)
        for codice in codici:
            numero = codici.count(codice)
            if numero > 1:
                ripetuti.add(codice)
        return ripetuti

    def cercaPercorso(self, v0):
        # Inizia con il vertice iniziale
        self.best_path = []
        visited = set()
        path = [v0]
        for neighbor in self._grafo.neighbors(v0):
            if (v0, neighbor) not in visited and self.controllo(path, neighbor):
                visited.add((v0, neighbor))
                visited.add((neighbor, v0))
                path.append(neighbor)
                self._dfs(neighbor, path, visited)
                path.pop()
                visited.remove((v0, neighbor))
                visited.remove((neighbor, v0))
        return self.getMassimo()

    def _dfs(self, current, path, visited):
        if len(path) > len(self.best_path):
            self.best_path = copy.deepcopy(path)

        if self.uscita(path, current):
            return

        for neighbor in self._grafo.neighbors(current):
            if (current, neighbor) not in visited and self.controllo(path, neighbor):
                visited.add((current, neighbor))
                visited.add((neighbor, current))
                path.append(neighbor)
                self._dfs(neighbor, path, visited)
                path.pop()
                visited.remove((current, neighbor))
                visited.remove((neighbor, current))

    def uscita(self, path, current):
        archi = [(current, neighbor) for neighbor in self._grafo[current].keys()]
        for arco in archi:
            if self._grafo[arco[0]][arco[1]]["weight"] >= self._grafo[path[-2]][path[-1]]['weight']:
                return False
        return True

    def controllo(self, path, neighbor):
        if len(path) == 1:
            return True
        last_edge_weight = self._grafo[path[-2]][path[-1]]['weight']
        current_edge_weight = self._grafo[path[-1]][neighbor]['weight']
        return current_edge_weight >= last_edge_weight

    def getMassimo(self):
        return self.best_path

    # def searchPath(self, product_number):
    #     nodoSource = self.idMap[product_number]
    #
    #     parziale = []
    #
    #     self.ricorsione(parziale, nodoSource, 0)
    #
    #     print("final", len(self._solBest), [i[2]["weight"] for i in self._solBest])
    #
    # def ricorsione(self, parziale, nodoLast, livello):
    #     archiViciniAmmissibili = self.getArchiViciniAmm(nodoLast, parziale)
    #
    #     if len(archiViciniAmmissibili) == 0:
    #         if len(parziale) > len(self._solBest):
    #             self._solBest = list(parziale)
    #             print(len(self._solBest), [ii[2]["weight"] for ii in self._solBest])
    #
    #     for a in archiViciniAmmissibili:
    #         parziale.append(a)
    #         self.ricorsione(parziale, a[1], livello + 1)
    #         parziale.pop()
    #
    # def getArchiViciniAmm(self, nodoLast, parziale):
    #
    #     archiVicini = self._grafo.edges(nodoLast, data=True)
    #     result = []
    #     for a1 in archiVicini:
    #         if self.isAscendent(a1, parziale) and self.isNovel(a1, parziale):
    #             result.append(a1)
    #     return result
    #
    # def isAscendent(self, e, parziale):
    #     if len(parziale) == 0:
    #         print("parziale is empty in isAscendent")
    #         return True
    #     return e[2]["weight"] >= parziale[-1][2]["weight"]
    #
    # def isNovel(self, e, parziale):
    #     if len(parziale) == 0:
    #         print("parziale is empty in isnovel")
    #         return True
    #     e_inv = (e[1], e[0], e[2])
    #     return (e_inv not in parziale) and (e not in parziale)

if __name__=="__main__":
    #from modello.prodotto import Prodotto
    myModel=Model()
    myModel.creaGrafo("Red",2015)
    print(myModel.numNodes())
    #print(myModel.calcoloMaggiore(myModel.calcolaStatistiche()))



