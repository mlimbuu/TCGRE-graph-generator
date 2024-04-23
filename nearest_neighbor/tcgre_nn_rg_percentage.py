import numpy as np
import random
from random import randint
import networkx as nx
import matplotlib.pyplot as plt
from nn_rg_percentage import NearestNeighbor_Percentage_Graph_Generator


class TCGRE_NN_Percentage_Graph_Generator:
    def __init__(self, N, P, width, height, risk_edge_ratio):
        self.N = N # Number of nodes
        self.P = P # percentage of nearest neighbors
        self.TCGRE_G = None
        self.positions = None

        self.width = width
        self.height = height

        self.risk_edge_ratio = risk_edge_ratio # risk edges to total edges ratio
        self.risk_edges_with_support_nodes = None # Risk edges with support nodes


    def create_nn_percentage_graph(self):
        # Create a graph with N nodes
        G = NearestNeighbor_Percentage_Graph_Generator(self.N, self.P, self.width, self.height)
        self.TCGRE_G, self.positions = G.create_nearest_neighbor_percentage_graph()
        print("Nearest Neighbor Graph created...")
        return self.TCGRE_G
    
   # just pick the shortest path
    def pick_edges_on_shortest_path(self):
        source = list(self.TCGRE_G.nodes())[0]
        target = len(self.TCGRE_G.nodes())-1

        print(f"Source: {source}, Target: {target}")
        # Find all shortest paths between source and target
        all_shoretest_paths = list(nx.all_shortest_paths(self.TCGRE_G, source=source, target=target, weight='weight'))

    
        # Extra unique edges from all paths
        unique_edges = set()
        for path in all_shoretest_paths:
            # Extract edges from the path (consecutive pairs of nodes) and add them to the set
            edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            unique_edges.update(edges)    

        return all_shoretest_paths, list(unique_edges)
    
    # dont add cost to the edges, just pick the risk edges and support nodes
    def pick_risk_edges_and_support_nodes(self):
        print("Picking risk edges and support nodes...")
        print(f"Total edges: {self.TCGRE_G.edges()}")
        print(f"Total nodes: {self.TCGRE_G.nodes()}")

        #Pick radome edges as risk edges from edges, it should be 0.2 of the total edges
        # Calculate the number of edges to select as risky
        num_risk_edges = int(len(self.TCGRE_G.edges()) * self.risk_edge_ratio)

        # Randomly select edges without replacement
        ## one way: add at least some risk edges on the shortest path with other edges
        all_shortest_paths, unique_edges_on_shortest_path = self.pick_edges_on_shortest_path()
        risk_edges = random.sample(self.TCGRE_G.edges(), num_risk_edges-1)
        # Filter out edges that are already in risk_edges
        available_edges = [edge for edge in unique_edges_on_shortest_path if edge not in risk_edges]
        ## add the edge on the shortest path
        # Check if there are any available edges to add
        if available_edges:
            # Randomly select an edge that's not already a risk edge
            chosen_edge = random.choice(available_edges)
            print(f"chosen_edge: {chosen_edge}")
            # Add this edge to risk_edges
            risk_edges.append(chosen_edge)

        ## pick up neighbors of the risk edges as support nodes
        ## check if node is in the neighbors of the risk edges

        risk_edge_with_support_nodes = {}
        support_nodes_used = set() 
        for edge in risk_edges:
            total_neighbors =  list(self.TCGRE_G.neighbors(edge[0])) +  list(self.TCGRE_G.neighbors(edge[1]))
            ## only pick the neighbors that are not used as support nodes before
            for neighbor in total_neighbors:
                if neighbor in support_nodes_used:
                    total_neighbors.remove(neighbor)
            random_support_node = random.choice(total_neighbors)
            risk_edge_with_support_nodes[edge] = (random_support_node,)
            # update the support nodes used
            support_nodes_used.add(random_support_node)

            print(f"risk_edge_with_support_nodes: {risk_edge_with_support_nodes}")
        self.risk_edges = risk_edge_with_support_nodes
        return self.risk_edges

    #  add cost to the edges including the risk edges
    def add_cost_to_edges(self):
        print("Adding cost to the edges...")
        for edge in self.TCGRE_G.edges():
            if edge in self.risk_edges.keys():
                print(f"risk_edge: {edge}, support_nodes: {self.risk_edges[edge][0]}")
                self.TCGRE_G[edge[0]][edge[1]]['cost'] = [20, (self.risk_edges[edge][0],)]
            else:
                print(f"normal_edge: {edge}")
                # either fixed cost for normal edges, lesser than the risk edge cost
                # self.TCGRE_G[edge[0]][edge[1]]['cost'] = 5
                # or random cost for normal edges, between 1 and 10, lesser than the risk edge cost
                self.TCGRE_G[edge[0]][edge[1]]['cost'] = random.randint(1, 10)

        return self.TCGRE_G

    # convert the graph to compatible graph
    def convert_to_compatible_graph(self):
        print("Converting to compatible graph...")
        nodes = {node: {} for node in self.TCGRE_G.nodes()}
        for edge in self.TCGRE_G.edges():
            # Unpack the edge nodes
            node1, node2 = edge
            nodes[node1][node2] = self.TCGRE_G[node1][node2]['cost']  # For node1 -> node2
            nodes[node2][node1] =  self.TCGRE_G[node1][node2]['cost'] # For node2 -> node1
        return nodes
    
    # plot the graph
    def plot_graph(self):
         # Draw the graph
        plt.figure()
        nx.draw(self.TCGRE_G, pos=self.positions, node_size=200, with_labels=True, node_color='skyblue', edge_color='black',font_size=12, font_color='gray')
        nx.draw_networkx_edge_labels(self.TCGRE_G, pos=self.positions, edge_labels={(u, v): d['cost'] for u, v, d in self.TCGRE_G.edges(data=True)})
        # change color to red for the risk edges
        nx.draw_networkx_edges(self.TCGRE_G, pos=self.positions, edgelist=self.risk_edges.keys(), edge_color='red', width=1.0)
        
        # Configure and show grid
        plt.grid(True, which='both', color='gray', linewidth=0.8, linestyle='--')  # Ensuring the grid is visible
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')

        # Setting axis labels and ticks
        plt.title(f"TCGRE Nearest Neighbor Graph with Fixed Radius")
   
        plt.axis('on')  # Ensure the axis is shown
        plt.xlabel('Width', fontsize=12)
        plt.ylabel('Height', fontsize=12)
        plt.xticks(range(0, self.width))  # Set ticks for x-axis
        plt.yticks(range(0, self.height))  # Set ticks for y-axis
        # Save the plot
        plt.savefig(f"./TCGRE_graph_generator/nearest_neighbor/plots/tcgre_nearest_neighbor_percentage_graph:N{self.N}_{int(self.P)}P.png")
        plt.show()







        # Using nx.spring_layout for positioning nodes, with the incremented graph
        # pos = nx.spring_layout(self.TCGRE_G, seed=42)
        # nx.draw(self.TCGRE_G, pos, with_labels=True, node_color='lightgreen', edge_color='gray')
        # nx.draw_networkx_edge_labels(self.TCGRE_G, pos, edge_labels={(u, v): d['cost'] for u, v, d in self.TCGRE_G.edges(data=True)})
        # # change color to red for the risk edges
        # nx.draw_networkx_edges(self.TCGRE_G, pos, edgelist=self.risk_edges.keys(), edge_color='red', width=1.0)
        # plt.title(f"TCGRE Nearest Neighbor Graph with Fixed Radius")
        # # Save the plot
        # plt.savefig(f'./TCGRE_graph_generator/nearest_neighbor/plots/tcgre_nn_fixedradius_N{self.N}.png')
        # # Show the plot
        # plt.show()


# Number of nodes
n = 25  
# Area dimensions
width, height = n+1, n+1  
# Percentage of nearest neighbors to connect
percentage = 30
risk_edge_ratio = 0.2   

tcgre_nn_fixed_radius = TCGRE_NN_Percentage_Graph_Generator(n, percentage, width, height, risk_edge_ratio)
tcgre_nn_fixed_radius.create_nn_percentage_graph()
tcgre_nn_fixed_radius.pick_risk_edges_and_support_nodes()
tcgre_nn_fixed_radius.add_cost_to_edges()
tcgre_nn_fixed_radius.convert_to_compatible_graph()
tcgre_nn_fixed_radius.plot_graph()


