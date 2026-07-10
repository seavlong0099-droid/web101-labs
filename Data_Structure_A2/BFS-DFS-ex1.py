from collections import deque

class Graph:
    def __init__(self, N):
        # Initialize graph with N vertices
        self.N = N

        # Create N x N adjacency matrix
        self.adj_matrix = [[0 for _ in range(N)] for _ in range(N)]

    def add_edge(self, u, v):
        # Add edge from u to v
        if u >= self.N or v >= self.N or u < 0 or v < 0:
            print("Invalid edge!")
        else:
            self.adj_matrix[u][v] = 1
            self.adj_matrix[v][u] = 1  # Undirected graph

    def remove_edge(self, u, v):
        # Remove edge from u to v
        if u >= self.N or u < 0:
            print("Vertex", u, "does not exist!")
        elif v >= self.N or v < 0:
            print("Vertex", v, "does not exist!")
        elif u == v:
            print("Same Vertex!")
        else:
            self.adj_matrix[u][v] = 0
            self.adj_matrix[v][u] = 0  # Undirected graph

    def display_matrix(self):
        # Display adjacency matrix
        print("Adjacency Matrix:")
        for row in self.adj_matrix:
            print(row)

    def bfs(self, start):
        visited = [False] * self.N
        queue = deque()

        visited[start] = True
        queue.append(start)

        print("BFS Traversal:", end=" ")

        while queue:
            vertex = queue.popleft()
            print(vertex + 1, end=" ")

            for i in range(self.N):
                if self.adj_matrix[vertex][i] == 1 and not visited[i]:
                    visited[i] = True
                    queue.append(i)

        print()


# Main Program

g = Graph(5)

# Graph from the picture
g.add_edge(0, 1)  # 1-2
g.add_edge(0, 4)  # 1-5
g.add_edge(1, 2)  # 2-3
g.add_edge(1, 3)  # 2-4
g.add_edge(1, 4)  # 2-5
g.add_edge(2, 3)  # 3-4
g.add_edge(3, 4)  # 4-5

print("Original Graph")
g.display_matrix()

print()
g.bfs(0)   # Start BFS from Vertex 1

print("\nAfter Removing Edge (2,5)")
g.remove_edge(1, 4)   # Remove edge 2-5

g.display_matrix()