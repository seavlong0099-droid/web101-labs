"""
graph.py

Implements an undirected Graph using an adjacency list, where every
movie is a node and an edge connects two movies that are "similar".

WHY A GRAPH?
------------
Movie similarity is naturally a *relationship* between items, not a
single lookup key -- a movie can be similar to several other movies
at once, and similarity can be discovered indirectly (a movie similar
to a movie that is similar to yours). That's exactly the kind of
"connected data" a Graph is built to represent; a Hash Table alone
cannot express these many-to-many relationships.

GRAPH REPRESENTATION
---------------------
We use an Adjacency List: a dictionary where each key is a movie_id
and the value is a set of movie_ids it is directly connected to.
This is more space-efficient than an adjacency matrix (O(V + E) vs
O(V^2)) when, as here, each movie is only similar to a handful of
others rather than every other movie.

TIME COMPLEXITY (V = number of movies, E = number of edges)
-------------------------------------------------------------
- add_node                 : O(1)
- add_edge                 : O(1)
- show_adjacency_list       : O(V + E)
- find_similar_movies (1 hop) : O(degree of node) ~ O(1) average
- BFS / DFS traversal        : O(V + E)
"""

from collections import deque


class Graph:
    """An undirected graph of movies connected by similarity."""

    def __init__(self):
        self.adjacency_list = {}   # movie_id -> set of connected movie_ids

    # ------------------------------------------------------------
    def reset(self):
        """
        Clears all nodes/edges. Used by Admin operations (add/update/
        delete movie) so the graph can be rebuilt from scratch with
        build_graph() whenever the catalog changes -- simpler and
        safer for a beginner project than patching individual edges.
        """
        self.adjacency_list = {}

    def add_node(self, movie_id):
        """Add a movie as a node in the graph. O(1)."""
        if movie_id not in self.adjacency_list:
            self.adjacency_list[movie_id] = set()

    def add_edge(self, movie_id_1, movie_id_2):
        """
        Connect two movies (undirected edge). O(1).
        Both nodes must already exist (added automatically if missing).
        """
        self.add_node(movie_id_1)
        self.add_node(movie_id_2)
        if movie_id_1 != movie_id_2:
            self.adjacency_list[movie_id_1].add(movie_id_2)
            self.adjacency_list[movie_id_2].add(movie_id_1)

    # ------------------------------------------------------------
    def build_graph(self, movies):
        """
        Builds the entire graph from a list of Movie objects.

        Two movies are connected if ANY of these hold:
          - Same genre
          - Rating difference <= 1
          - Release year difference <= 5

        This is O(n^2) since we compare every pair once -- acceptable
        here because a catalog of a few thousand movies is still fast,
        and it only needs to run once when the catalog changes.
        """
        for movie in movies:
            self.add_node(movie.movie_id)

        n = len(movies)
        for i in range(n):
            for j in range(i + 1, n):
                m1, m2 = movies[i], movies[j]
                same_genre = m1.genre.lower() == m2.genre.lower()
                close_rating = abs(m1.rating - m2.rating) <= 1
                close_year = abs(m1.year - m2.year) <= 5

                if same_genre or close_rating or close_year:
                    self.add_edge(m1.movie_id, m2.movie_id)

    # ------------------------------------------------------------
    def show_adjacency_list(self, movie_lookup=None):
        """
        Returns a printable string of the adjacency list.
        If movie_lookup (a function id -> Movie) is given, titles are
        shown instead of raw IDs for readability.
        """
        lines = []
        for movie_id, neighbors in self.adjacency_list.items():
            if movie_lookup:
                name = movie_lookup(movie_id).title
                neighbor_names = [movie_lookup(n).title for n in neighbors]
                lines.append(f"{name} -> {neighbor_names}")
            else:
                lines.append(f"{movie_id} -> {list(neighbors)}")
        return "\n".join(lines)

    def find_similar_movies(self, movie_id):
        """
        Returns the direct neighbors (1 hop) of a movie -- i.e. the
        set of movies most similar to it. O(degree of node).
        """
        return list(self.adjacency_list.get(movie_id, set()))

    # ------------------------------------------------------------
    def bfs(self, start_id):
        """
        Breadth-First Search: explores the graph level by level using
        a queue. Good for finding the "closest" similar movies first
        (fewest hops away). O(V + E).
        """
        if start_id not in self.adjacency_list:
            return []

        visited = {start_id}
        queue = deque([start_id])
        order = []

        while queue:
            current = queue.popleft()
            order.append(current)
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

    def dfs(self, start_id):
        """
        Depth-First Search: explores as far as possible down one path
        before backtracking, using a stack (implemented via
        recursion). Good for exploring "chains" of similarity.
        O(V + E).
        """
        visited = set()
        order = []

        def _dfs_visit(node_id):
            if node_id in visited or node_id not in self.adjacency_list:
                return
            visited.add(node_id)
            order.append(node_id)
            for neighbor in self.adjacency_list[node_id]:
                _dfs_visit(neighbor)

        _dfs_visit(start_id)
        return order
