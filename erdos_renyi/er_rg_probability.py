import networkx as nx
import matplotlib.pyplot as plt

class ErdosRenyi_GNP_Graph_Generator:
    '''
    1) Nodes Initialization: The graph starts with n nodes and no edges.
    2) Edge Consideration: For each pair of nodes (let's say nodes i and j), the algorithm considers whether to add an edge between them.
    3) Random Decision: For each pair, a random number is generated (typically uniformly distributed between 0 and 1). If this number is less than or equal to 
    p, an edge between i and j is added to the graph. If the number is greater than 
    p, no edge is added between those nodes.
    
    Note: For n=10 nodes, there are nC2 = 45 possible edges that can be added. 
    When you use p=0.3, each of these 45 possible edges has a 30% chance of being included in the graph.
    '''
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.G = None

    # Create a random graph using the G(n, p) model
    def create_gnp_random_graph(self):
        G = nx.erdos_renyi_graph(self.n, self.p)
        self.G = G
        return self.G
    
    # Plot the graph
    def draw_ER_graph(self):
        plt.figure(figsize=(8, 6))
        nx.draw(self.G, with_labels=True, node_color='skyblue', node_size=700, edge_color='k')
        plt.title('Random Graph from G(n, p) Model')
        # Save the plot
        plt.savefig(f'./erdos_renyi/plots/random_graph_gnp_G({self.n},{self.p}).png')
        # Show the plot
        plt.show()