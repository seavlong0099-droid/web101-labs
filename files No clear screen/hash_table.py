"""
hash_table.py

Contains everything related to storing and fast-looking-up movies:

    - Movie             : the data model for a single movie
    - HashTable         : a Hash Table built from scratch (separate chaining)
    - MovieDatabase      : wraps 3 HashTables for O(1)-average lookup by
                            ID / Title / Genre
    - get_sample_movies(): the starting catalog of 18 sample movies

(Movie, and the sample data, used to live in their own files --
merged in here to keep the project to 4 files total: hash_table.py,
graph.py, decision_tree.py, main.py.)

WHY A HASH TABLE?
-----------------
A streaming platform may hold thousands of movies. Searching a plain
list for a movie by ID or title is O(n) -- every entry must be
checked. A Hash Table converts a key (ID, Title, or Genre) into an
array index using a hash function, letting us jump almost directly
to the data instead of scanning everything.

Average Case Complexity : O(1)  -> hash function spreads keys evenly.
Worst Case Complexity   : O(n)  -> if every key hashed to the same
                                    bucket, we'd degrade to a single
                                    linked list (a linear scan).
"""


# ======================================================================
# Movie
# ======================================================================
class Movie:
    """
    Represents a single movie with all of its attributes.

    Using a class (OOP) instead of a plain dictionary keeps related
    data together and lets us attach behavior (like __str__) to it.
    """

    def __init__(self, movie_id, title, genre, rating, year, description):
        self.movie_id = movie_id          # Unique integer ID (Hash Table key)
        self.title = title                # Movie title (string)
        self.genre = genre                # Genre, e.g. "Action", "Comedy"
        self.rating = rating              # Float rating out of 10
        self.year = year                  # Release year (int)
        self.description = description    # Short description (string)

    def __str__(self):
        """Readable one-line summary used when printing a movie."""
        return (f"[{self.movie_id}] {self.title} "
                f"({self.year}) - {self.genre} - Rating: {self.rating}/10")

    def full_details(self):
        """Multi-line detailed view used when a single movie is displayed."""
        return (
            f"Movie ID     : {self.movie_id}\n"
            f"Title        : {self.title}\n"
            f"Genre        : {self.genre}\n"
            f"Rating       : {self.rating}/10\n"
            f"Release Year : {self.year}\n"
            f"Description  : {self.description}"
        )


# ======================================================================
# Hash Table (built from scratch, separate chaining)
# ======================================================================
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
    """

    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity   # each bucket is a linked list head

    def _hash(self, key):
        """Converts a key (string or int) into a bucket index."""
        return hash(key) % self.capacity

    def insert(self, key, value):
        """Insert a key-value pair. O(1) average. Overwrites if key exists."""
        index = self._hash(key)
        node = self.buckets[index]

        while node:
            if node.key == key:
                node.value = value      # key exists -> update value
                return
            node = node.next

        new_node = _Node(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1

        if self.size / self.capacity > 0.75:
            self._resize()

    def search(self, key):
        """Search for a key. O(1) average, O(n) worst case."""
        index = self._hash(key)
        node = self.buckets[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def delete(self, key):
        """Delete a key-value pair. O(1) average, O(n) worst case."""
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
        """Return a list of all keys currently stored."""
        result = []
        for head in self.buckets:
            node = head
            while node:
                result.append(node.key)
                node = node.next
        return result

    def _resize(self):
        """Doubles capacity and re-hashes all entries (keeps O(1) average)."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0

        for head in old_buckets:
            node = head
            while node:
                self.insert(node.key, node.value)
                node = node.next


# ======================================================================
# MovieDatabase (3 Hash Tables -> fast lookup by ID / Title / Genre)
# ======================================================================
class MovieDatabase:
    """
        id_table    : movie_id (int)      -> Movie object
        title_table : title (lowercase)   -> movie_id
        genre_table : genre (lowercase)   -> list of movie_ids
    """

    def __init__(self):
        self.id_table = HashTable()
        self.title_table = HashTable()
        self.genre_table = HashTable()
        self._all_ids = []   # keeps insertion order for "View All Movies"

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
        """Update one or more fields; keeps title/genre indexes in sync."""
        movie = self.id_table.search(movie_id)
        if movie is None:
            return False

        old_title = movie.title.lower()
        old_genre = movie.genre.lower()

        for field, new_value in fields.items():
            if hasattr(movie, field):
                setattr(movie, field, new_value)

        if movie.title.lower() != old_title:
            self.title_table.delete(old_title)
            self.title_table.insert(movie.title.lower(), movie.movie_id)

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


# ======================================================================
# Sample data
# ======================================================================
def get_sample_movies():
    """Returns the starting catalog of 18 sample Movie objects."""
    # Ratings/years are deliberately spread out so the similarity Graph
    # forms distinct clusters instead of connecting almost every movie.
    raw_data = [
        (1, "The Last Horizon", "Sci-Fi", 6.3, 2005, "A crew searches for a new home planet."),
        (2, "Neon Skyline", "Sci-Fi", 8.9, 2014, "A hacker uncovers a conspiracy in a cyberpunk city."),
        (3, "Galaxy Runners", "Sci-Fi", 8.1, 2023, "Smugglers race across the galaxy to deliver cargo."),
        (4, "Silent Protocol", "Action", 7.0, 2000, "An agent must stop a rogue AI from launching missiles."),
        (5, "Steel Fists", "Action", 8.6, 2011, "Two rival fighters team up to take down a crime syndicate."),
        (6, "Midnight Chase", "Action", 7.9, 2022, "A detective races against time to catch a serial thief."),
        (7, "Laugh Track", "Comedy", 6.1, 2003, "A struggling comedian gets an unexpected shot at fame."),
        (8, "Office Chaos", "Comedy", 7.3, 2012, "A new intern turns an ordinary office upside down."),
        (9, "Road Trip Rules", "Comedy", 8.8, 2020, "Three friends learn life lessons on a cross-country trip."),
        (10, "Autumn Letters", "Drama", 8.0, 1999, "A writer reconnects with her estranged family."),
        (11, "The Quiet Room", "Drama", 6.7, 2009, "A therapist confronts her own past while helping a patient."),
        (12, "Broken Bridges", "Drama", 9.0, 2021, "A family struggles to reconcile after a tragedy."),
        (13, "The Haunting Hour", "Horror", 7.8, 2006, "A family moves into a house with a dark history."),
        (14, "Whispers Below", "Horror", 6.0, 2015, "Researchers uncover something ancient beneath the ice."),
        (15, "Echoes in the Dark", "Horror", 8.4, 2024, "A group of friends is stalked during a camping trip."),
        (16, "Paris in Spring", "Romance", 8.2, 2002, "Two strangers fall in love during a chance encounter."),
        (17, "Letters Unsent", "Romance", 7.0, 2013, "A woman discovers old love letters that change her life."),
        (18, "Second Chances", "Romance", 9.1, 2019, "Former sweethearts reunite years after a painful breakup."),
    ]

    movies = []
    for movie_id, title, genre, rating, year, description in raw_data:
        movies.append(Movie(movie_id, title, genre, rating, year, description))

    return movies
