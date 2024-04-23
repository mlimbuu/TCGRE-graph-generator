import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from random import randint

# Calculate the Euclidean distance between two points
def distance(u, v):
    return np.sqrt((u[0] - v[0])**2 + (u[1] - v[1])**2)

# Generate random positions within the given dimensions
def random_position(width, height, N):
    positions = {}
    i = 0
    while len(positions) < N:
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

## only add edges closest to each node based on fixed radius
def add_edges_by_fixed_radius(G, positions, fixed_radius):
    # Add edges based on distance
    for i in range(len(G.nodes())):
        edges_per_node = 0
        for j in range(i + 1, len(G.nodes())):
            dist = distance(positions[i], positions[j])
            print("dist: ", dist)
            # Probability of connection decreases within fixed radius
            if dist < fixed_radius:
                G.add_edge(i, j)
                print(f"Connected nodes {i} and {j} with distance {dist}")
                edges_per_node += 1
        print(f"Node {i} has {edges_per_node} edges.")
    return G

class NearestNeighbor_FixedRadius_Graph_Generator:
    '''
    Edges formation: 
    1. For N nodes, nearest neighbours within P fixed raidus are connected to each node.
    3. Isolated nodes are connected to their nearest neighbour.
    4. Isolated graph sub-components are connected to the main component.
    '''
    def __init__(self, N, width, height, fixed_radius):
        self.N = N
        self.G = None # nearest neighbor fixed radius graph
        
        self.width = width
        self.height = height
        self.fixed_radius = fixed_radius
        
        self.positions = None

    def create_nearest_neighbor_fixed_radius_graph(self):
        # Create an empty graph
        G = nx.Graph()

        # Generate random positions for the nodes
        positions = random_position(self.width, self.height, self.N)
        self.positions = positions

        # Add nodes to the graph
        self.G = add_nodes(G, positions)
        # Add edges based on distance, edges are for nearest neighbors within fixed radius
        self.G = add_edges_by_fixed_radius(self.G, positions, self.fixed_radius)
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
        nx.draw(self.G, pos=self.positions, node_size=200, with_labels=True, node_color='skyblue', edge_color='black', font_color='gray')

        # Configure and show grid
        plt.grid(True, which='both', color='gray', linewidth=0.8, linestyle='--')  # Ensuring the grid is visible
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')

        # Setting axis labels and ticks
        plt.title('Nearest Neighbor Fixed Radius Graph')
        plt.axis('on')  # Ensure the axis is shown
        plt.xlabel('Width', fontsize=12)
        plt.ylabel('Height', fontsize=12)
        plt.xticks(range(0, self.width))  # Set ticks for x-axis
        plt.yticks(range(0, self.height))  # Set ticks for y-axis
        # Save the plot
        plt.savefig(f"./nearest_neighbor/plots/nearest_neighbor_graph:N{self.N}_{self.fixed_radius}FR.png")
        plt.show()

