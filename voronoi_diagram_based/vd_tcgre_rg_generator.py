import networkx as nx
import matplotlib.pyplot as plt

class VD_RandomGraph:
    def __init__(self, N, R):
        self.N = N
        self.R = R
        
    def create_graph(self):
        G = nx.Graph()
        for i in range(self.N):
            G.add_node(i)
        return G
    
class TCGRE_VD_RandomGraph:
    def __init__(self, N, R):
        self.N = N
        self.R = R
        
    def create_graph(self):
        G = nx.Graph()
        for i in range(self.N):
            G.add_node(i)
        return G
    
# Parameters
N = 10  # number of nodes
R = 1  # radius of the circle

    