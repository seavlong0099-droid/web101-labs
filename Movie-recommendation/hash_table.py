"""
hash_table.py

Implements a Hash Table from scratch (no built-in dict used for the
core storage) using separate chaining for collision handling, and a
MovieDatabase class that uses three such hash tables to give
fast (average O(1)) lookup by ID, by Title, and by Genre.

WHY A HASH TABLE?
-----------------
A streaming platform may hold thousands of movies. If we stored them
in a plain list, searching for a movie by ID or title would require
scanning every element -> O(n) per search.

A Hash Table converts a key (ID, Title, or Genre) into an array index
using a hash function. This lets us jump almost directly to the
data instead of scanning everything.

Average Case Complexity : O(1)  -> hash function spreads keys evenly,
                                    each bucket holds very few items.
Worst Case Complexity   : O(n)  -> if every key hashes to the same
                                    bucket (a bad hash function or an
                                    adversarial input), we degrade to
                                    a single linked list, i.e. a
                                    linear scan.
"""


class _Node:
    """A single link in a bucket's chain (used internally)."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """
    A general-purpose Hash Table supporting insert, search, update,
    and delete, using separate chaining to resolve collisions.

    Keys can map to a single value (e.g. ID -> Movie) or to a list of
    values (e.g. Genre -> [Movie IDs]) depending on how the caller
    uses it; the table itself just stores whatever value is given.
    """

    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity   # each bucket is a linked list head

    # ------------------------------------------------------------
    # Hash function
    # ------------------------------------------------------------
    def _hash(self, key):
        """
        Converts a key (string or int) into a bucket index.

        Python's built-in hash() gives a large integer; we take it
        modulo the table capacity to fit inside our bucket array.
        """
        return hash(key) % self.capacity

    # ------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------
    def insert(self, key, value):
        """
        Insert a key-value pair. O(1) average.
        If the key already exists, its value is overwritten.
        """
        index = self._hash(key)
        node = self.buckets[index]

        # Walk the chain at this bucket to check for an existing key
        while node:
            if node.key == key:
                node.value = value      # key exists -> update value
                return
            node = node.next

        # Key not found -> insert new node at the head of the chain
        new_node = _Node(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1

        # Resize if the table is getting too full (keeps O(1) average)
        if self.size / self.capacity > 0.75:
            self._resize()

    def search(self, key):
        """
        Search for a key. O(1) average, O(n) worst case.
        Returns the value, or None if not found.
        """
        index = self._hash(key)
        node = self.buckets[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def delete(self, key):
        """
        Delete a key-value pair. O(1) average, O(n) worst case.
        Returns True if deleted, False if the key wasn't found.
        """
        index = self._hash(key)
        node = self.buckets[index]
        prev = None
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[index] = node.next
                self.size -= 1
                return True
            prev = node
            node = node.next
        return False

    def keys(self):
        """Return a list of all keys currently stored (used for iteration)."""
        result = []
        for head in self.buckets:
            node = head
            while node:
                result.append(node.key)
                node = node.next
        return result

    def values(self):
        """Return a list of all values currently stored."""
        result = []
        for head in self.buckets:
            node = head
            while node:
                result.append(node.value)
                node = node.next
        return result

    def _resize(self):
        """
        Doubles the table capacity and re-hashes all existing entries.
        This is what keeps average-case operations close to O(1) even
        as more movies are added.
        """
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0

        for head in old_buckets:
            node = head
            while node:
                self.insert(node.key, node.value)
                node = node.next


class MovieDatabase:
    """
    Wraps three Hash Tables to give fast average O(1) lookup of movies
    by ID, Title, and Genre -- exactly the kind of fast search a
    streaming platform needs before doing any heavier graph/tree work.

        id_table    : movie_id (int)      -> Movie object
        title_table : title (lowercase)   -> movie_id
        genre_table : genre (lowercase)   -> list of movie_ids
    """

    def __init__(self):
        self.id_table = HashTable()
        self.title_table = HashTable()
        self.genre_table = HashTable()
        self._all_ids = []   # keeps insertion order for "View All Movies"

    # ------------------------------------------------------------
    def insert_movie(self, movie):
        """Insert a movie into all three hash tables. O(1) average."""
        self.id_table.insert(movie.movie_id, movie)
        self.title_table.insert(movie.title.lower(), movie.movie_id)

        genre_key = movie.genre.lower()
        genre_list = self.genre_table.search(genre_key)
        if genre_list is None:
            genre_list = []
        genre_list.append(movie.movie_id)
        self.genre_table.insert(genre_key, genre_list)

        self._all_ids.append(movie.movie_id)

    def search_by_id(self, movie_id):
        """O(1) average lookup by ID."""
        return self.id_table.search(movie_id)

    def search_by_title(self, title):
        """O(1) average lookup by exact title."""
        movie_id = self.title_table.search(title.lower())
        if movie_id is None:
            return None
        return self.id_table.search(movie_id)

    def search_by_genre(self, genre):
        """O(1) average lookup of the ID list for a genre, then O(k) to fetch k movies."""
        ids = self.genre_table.search(genre.lower())
        if not ids:
            return []
        return [self.id_table.search(mid) for mid in ids]

    def update_movie(self, movie_id, **fields):
        """
        Update one or more fields of an existing movie.
        Rebuilds title/genre index entries if those fields changed.
        """
        movie = self.id_table.search(movie_id)
        if movie is None:
            return False

        old_title = movie.title.lower()
        old_genre = movie.genre.lower()

        for field, new_value in fields.items():
            if hasattr(movie, field):
                setattr(movie, field, new_value)

        # Keep the title index in sync
        if movie.title.lower() != old_title:
            self.title_table.delete(old_title)
            self.title_table.insert(movie.title.lower(), movie.movie_id)

        # Keep the genre index in sync
        if movie.genre.lower() != old_genre:
            old_list = self.genre_table.search(old_genre) or []
            if movie_id in old_list:
                old_list.remove(movie_id)
            self.genre_table.insert(old_genre, old_list)

            new_list = self.genre_table.search(movie.genre.lower()) or []
            new_list.append(movie_id)
            self.genre_table.insert(movie.genre.lower(), new_list)

        return True

    def delete_movie(self, movie_id):
        """Remove a movie from all three hash tables."""
        movie = self.id_table.search(movie_id)
        if movie is None:
            return False

        self.id_table.delete(movie_id)
        self.title_table.delete(movie.title.lower())

        genre_list = self.genre_table.search(movie.genre.lower()) or []
        if movie_id in genre_list:
            genre_list.remove(movie_id)
        self.genre_table.insert(movie.genre.lower(), genre_list)

        if movie_id in self._all_ids:
            self._all_ids.remove(movie_id)

        return True

    def get_all_movies(self):
        """Return all movies in the order they were inserted."""
        return [self.id_table.search(mid) for mid in self._all_ids]

    def all_genres(self):
        """Return the list of distinct genres currently in the database."""
        seen = set()
        genres = []
        for movie in self.get_all_movies():
            if movie.genre not in seen:
                seen.add(movie.genre)
                genres.append(movie.genre)
        return genres
