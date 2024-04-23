import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d

def generate_voronoi_graph(num_points):
    points = np.random.rand(num_points, 2)
    vor = Voronoi(points)
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2, line_alpha=0.6, point_size=2)

    G = nx.Graph()
    for i in range(len(vor.point_region)):
        G.add_node(i)
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        # if v1 >= 0 and v2 >= 0: # Filter out ridges with one or two infinite end points, this is optional
        G.add_edge(p1, p2)
    pos = {i: point for i, point in enumerate(points)}
    nx.draw(G, pos, node_color='skyblue', node_size=200, with_labels=True, edge_color='gray', font_size=10)
    # Save the plot
    plt.savefig(f'./random_graph_generator/voronoi_diagram/plots/voronoi_graph_N{num_points}.png')
    # Show the plot
    # plt.show()
    return G, points

def distance(u, v):
    return np.sqrt((u[0] - v[0])**2 + (u[1] - v[1])**2)

def connect_isolated_nodes(G, points):
    isolates = list(nx.isolates(G))
    if isolates:
        print(f"Isolated nodes found: {isolates}")
        for node in isolates:
            # Calculate distances from the isolated node to all other nodes
            distances = {i: distance.euclidean(points[node], points[i]) for i in range(len(points)) if i != node}         
            print(f"Distances from node {node}: {distances}")
            # Find the closest node that is not the same as the isolated node
            nearest_neighbor = min(distances, key=distances.get)
            print(f"Nearest neighbor to node {node}: {nearest_neighbor}")
        G.add_edge(node, nearest_neighbor)
    else:
        print("No isolated nodes found.")
    return G

# Generate a random graph using the Voronoi diagram
N = 10 # number of nodes as well as voronoi points
G, points = generate_voronoi_graph(N)
G = connect_isolated_nodes(G, points)
print(G.nodes())
##
