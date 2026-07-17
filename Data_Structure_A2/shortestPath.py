from collections import deque
import heapq


class Graph:
    def __init__(self):
        self.vertices = []
        self.matrix = []

    # Add a building (vertex)
    def add_vertex(self, v):
        if v not in self.vertices:
            self.vertices.append(v)
            n = len(self.vertices)
            for row in self.matrix:
                row.append(0)
            self.matrix.append([0] * n)

    # Add an edge
    def add_edge(self, u, v, w):
        i = self.vertices.index(u)
        j = self.vertices.index(v)
        self.matrix[i][j] = w
        self.matrix[j][i] = w  # Undirected graph

    # Remove an edge
    def remove_edge(self, u, v):
        i = self.vertices.index(u)
        j = self.vertices.index(v)
        self.matrix[i][j] = 0
        self.matrix[j][i] = 0

    # Display adjacency matrix
    def display_matrix(self):
        print("\nAdjacency Matrix")
        print("{:15}".format(""), end="")
        for v in self.vertices:
            print("{:15}".format(v), end="")
        print()

        for i in range(len(self.vertices)):
            print("{:15}".format(self.vertices[i]), end="")
            for j in range(len(self.vertices)):
                print("{:15}".format(self.matrix[i][j]), end="")
            print()

    # BFS
    def bfs(self, start):
        visited = set()
        queue = deque([start])
        visited.add(start)

        print("\nBFS Traversal:")
        while queue:
            current = queue.popleft()
            print(current, end=" -> ")

            i = self.vertices.index(current)
            for j in range(len(self.vertices)):
                if self.matrix[i][j] != 0:
                    neighbor = self.vertices[j]
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
        print("End")

    # DFS
    def dfs(self, start):
        visited = set()

        def dfs_visit(node):
            visited.add(node)
            print(node, end=" -> ")

            i = self.vertices.index(node)
            for j in range(len(self.vertices)):
                if self.matrix[i][j] != 0:
                    neighbor = self.vertices[j]
                    if neighbor not in visited:
                        dfs_visit(neighbor)

        print("\nDFS Traversal:")
        dfs_visit(start)
        print("End")

    # Dijkstra's Algorithm
    def dijkstra(self, start):
        distances = {v: float('inf') for v in self.vertices}
        distances[start] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_distance > distances[current_vertex]:
                continue

            i = self.vertices.index(current_vertex)

            for j in range(len(self.vertices)):
                weight = self.matrix[i][j]

                if weight != 0:
                    neighbor = self.vertices[j]
                    distance = current_distance + weight

                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        heapq.heappush(priority_queue, (distance, neighbor))

        print("\nShortest Distance from", start)
        for vertex in self.vertices:
            print(f"{start} -> {vertex} = {distances[vertex]} meters")


# ---------------- MAIN PROGRAM ----------------

g = Graph()

# RUPP Buildings
buildings = [
    "Gate",
    "Library",
    "Building A",
    "Building T",
    "STEM Building",
    "IFL"
]

# Add vertices
for building in buildings:
    g.add_vertex(building)

# Add weighted edges (approximate distances in meters)
g.add_edge("Gate", "Library", 150)
g.add_edge("Gate", "Building A", 120)
g.add_edge("Library", "Building T", 100)
g.add_edge("Building A", "Building T", 80)
g.add_edge("Building A", "STEM Building", 140)
g.add_edge("Building T", "IFL", 110)
g.add_edge("STEM Building", "IFL", 90)
g.add_edge("Library", "STEM Building", 170)

# Display graph
g.display_matrix()

# BFS from Gate
g.bfs("Gate")

# DFS from Gate
g.dfs("Gate")

# Dijkstra from Gate
g.dijkstra("Gate")

# Remove an edge
print("\nRemoving edge between Library and STEM Building...")
g.remove_edge("Library", "STEM Building")

# Display updated graph
g.display_matrix()