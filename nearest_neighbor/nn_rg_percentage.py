import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from random import randint

# Calculate the Euclidean distance between two points
def distance(u, v):
    return np.sqrt((u[0] - v[0])**2 + (u[1] - v[1])**2)

# Generate random positions within the given dimensions
def random_position(width, height, n):
    positions = {}
    i = 0
    while len(positions) < n:
        x = randint(0+1, width-1)
        y = randint(0+1, height-1)
        if (x, y) not in positions.values():
            positions[i] = (x, y)
            i += 1
    return positions

# Add nodes to the graph
def add_nodes(G, positions):
    for node, pos in positions.items():
        G.add_node(node, pos=pos)
    return G

## only add edges closest to each node based on a percentage
def add_edges_by_distance(G, positions, percentage):
    n = len(positions)
    for i in range(len(G.nodes())):
        # Create a list of distances from node i to all other nodes
        distances = [(j, distance(positions[i], positions[j])) for j in range(n) if i != j]
        # Sort nodes by distance
        distances.sort(key=lambda x: x[1])
        # Determine the number of closest nodes to connect based on the percentage
        num_neighbors = int(np.ceil(percentage / 100.0 * (n - 1)))

        print("distances: ", distances)
        print("num_neighbors: ", num_neighbors)

        # Connect to the closest 'num_neighbors' nodes
        for j in range(num_neighbors):
            G.add_edge(i, distances[j][0])
    return G

class NearestNeighbor_Percentage_Graph_Generator:
    '''
    Edges formation: 
    1. For N nodes, P% of the nearest neighbours are connected to each node.
    3. Isolated nodes are connected to their nearest neighbour.
    4. Isolated graph sub-components are connected to the main component.
    '''
    def __init__(self, N, P, width, height):
        self.N = N
        self.P = P
        self.G = None

        self.width = width
        self.height = height

        self.positions = None

    def create_nearest_neighbor_percentage_graph(self):
        # Create an empty graph
        G = nx.Graph()

        # Generate random positions for the nodes
        self.positions = random_position(self.width, self.height, self.N)

        # Add nodes to the graph
        self.G = add_nodes(G, self.positions)

        # Add edges based on distance, connecting P% of the nearest neighbors
        self.G = add_edges_by_distance(self.G, self.positions, self.P)

        # Check and connect isolated nodes
        self.G = self.check_and_connect_isolates()

        # Check and connect components if any
        self.G = self.connect_components()

        return self.G, self.positions

    def check_and_connect_isolates(self):
        isolates = list(nx.isolates(self.G))
        if isolates:
            print(f"Isolated nodes detected: {isolates}")
            for node in isolates:
                # You might want to connect this node to its nearest neighbor not isolated
                distances = [(neighbor, distance(self.positions[node], self.positions[neighbor]))
                            for neighbor in set(self.G.nodes()) - set(isolates)]
                if distances:
                    closest_neighbor = min(distances, key=lambda x: x[1])[0]
                    self.G.add_edge(node, closest_neighbor)
                    print(f"Connected isolated node {node} to {closest_neighbor}")
        else:
            print("No isolated nodes detected.")
        return self.G

    def connect_components(self):
        # Find all connected components
        components = list(nx.connected_components(self.G))
        if len(components) > 1:
            print(f"Graph is not fully connected; it has {len(components)} components.")
            # Sort components by size and connect smallest to largest to minimize added edge length
            components = list(sorted(components, key=len))
            main_component = components[-1]  # Largest component
            for component in components[:-1]:
                # Connect each smaller component to the largest component
                closest_pair = None
                min_distance = float('inf')
                for node in component:
                    for main_node in main_component:
                        dist = distance(self.positions[node], self.positions[main_node])
                        if dist < min_distance:
                            min_distance = dist
                            closest_pair = (node, main_node)
                self.G.add_edge(*closest_pair)
                print(f"Connected {closest_pair[0]} to {closest_pair[1]} to unify components.")
        else:
            print("Graph is fully connected.")
        return self.G
    
    # plot the graph
    def plot_graph(self):
        # Draw the graph
        plt.figure()
        nx.draw(self.G, pos=self.positions, node_size=150, with_labels=True, node_color='skyblue', edge_color='gray')

        # Configure and show grid
        plt.grid(True, which='both', color='gray', linewidth=0.8, linestyle='--')  # Ensuring the grid is visible
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')

        # Setting axis labels and ticks
        plt.title('Nearest Neighbor Graph on a Grid')
        plt.axis('on')  # Ensure the axis is shown
        plt.xlabel('Width')
        plt.ylabel('Height')
        plt.xticks(range(0, width+1))  # Set ticks for x-axis
        plt.yticks(range(0, height+1))  # Set ticks for y-axis
        # Save the plot
        plt.savefig(f'./TCGRE_graph_generator/nearest_neighbor/plots/nearest_neighbor_graph:{n}N_{percentage}P.png')
        # Show the plot
        plt.show()




# # Number of nodes
# n = 20  
# # Area dimensions
# width, height = n+1, n+1  
# # Percentage of nearest neighbors to connect
# percentage = 30

# nn_rg_percentage = NearestNeighbor_Percentage_Graph_Generator(n, percentage, width, height)
# nn_rg_percentage.create_nearest_neighbor_percentage_graph()
# nn_rg_percentage.plot_graph()



