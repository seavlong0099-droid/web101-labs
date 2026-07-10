class Graph:
    def __init__(self, num_nodes, is_directed=False):
        
        #Constructor to initialize the graph.
        
        self.num_nodes = num_nodes
        self.is_directed = is_directed
        
        # 1. Initialize an empty dictionary for the Adjacency List
        self.adj_list = {}
        for i in range(1, num_nodes + 1):
            self.adj_list[i] = []
            
        # 2. Initialize a grid of zeros for the Adjacency Matrix
        self.matrix = []
        for i in range(num_nodes):
            self.matrix.append([0] * num_nodes)

    def add_edge(self, start, end):
        
        #Method to add a connection/edge to both representations.
        
        # Add to Adjacency List
        self.adj_list[start].append(end)
        
        # Add to Adjacency Matrix (subtract 1 for 0-based index)
        self.matrix[start - 1][end - 1] = 1
        
        # If the graph is undirected, add the connection backwards too
        if not self.is_directed:
            self.adj_list[end].append(start)
            self.matrix[end - 1][start - 1] = 1

    def display(self):
        
        #Method to print out both layouts nicely.
        
        print("\n--- Adjacency Matrix Grid ---")
        for row in self.matrix:
            print(row)
            
        print("\n--- Adjacency List Mapping ---")
        for node, neighbors in self.adj_list.items():
            print(f"Node {node} -> {neighbors}")


# CREATING THE UNDIRECTED GRAPH ---

print("     UNDIRECTED GRAPH        ")


# Instantiate a 5-node undirected graph object
undirected_graph = Graph(num_nodes=5, is_directed=False)

# Add all the edge connections
undirected_edges = [(1, 2), (1, 4), (2, 3), (2, 4), (3, 5), (4, 5)]
for start, end in undirected_edges:
    undirected_graph.add_edge(start, end)

# Display the matrix and list side-by-side
undirected_graph.display()


