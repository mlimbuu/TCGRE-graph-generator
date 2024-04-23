import networkx as nx
import matplotlib.pyplot as plt

class ErdosRenyi_GNM_Graph_Generator:
    '''
    1) Nodes Initialization: The graph starts with n nodes.
    2) Random Edge Selection: M edges are selected randomly from 
    the set of all possible nC2 edges. Each selected edge is unique and
    totall number of edges is  exactly M.

    Note: For n=10 nodes, there are nC2 = 45 possible edges that can be added.
    The total number of edges M is specified by the user and should be less than nC2.
    '''
    def __init__(self, n, M):
        self.n = n
        self.M = M
        self.G = None

    # Create a random graph using the G(n, M) model
    def create_gnm_random_graph(self):
        # Check if the number of edges M is less than n*(n-1)/2
        if self.M > self.n*(self.n-1)/2:
            raise Exception(f"Number of edges M should be less than n*(n-1)/2 = {self.n*(self.n-1)/2}")
        G = nx.gnm_random_graph(self.n, self.M)
        self.G = G
        return self.G
    
    # Plot the graph
    def draw_ER_graph(self):
        plt.figure(figsize=(8, 6))
        nx.draw(self.G, with_labels=True, node_color='lightgreen', node_size=700, edge_color='k')
        plt.title('Random Graph from G(n, M) Model')
        # Save the plot
        plt.savefig(f'./erdos_renyi/plots/random_graph_gnm_G({self.n},{self.M}).png')
        # Show the plot
        plt.show()

