"""
movie.py

Defines the Movie class.

A Movie object is the basic unit of data stored in our Hash Table
and represented as a node in our Graph.
"""


class Movie:
    """
    Represents a single movie with all of its attributes.

    Using a class (OOP) instead of a plain dictionary makes the code
    easier to read, keeps related data together, and lets us attach
    behavior (like __str__) directly to the object.
    """

    def __init__(self, movie_id, title, genre, rating, year, description):
        self.movie_id = movie_id          # Unique integer ID (used as Hash Table key)
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

    def to_dict(self):
        """Used by the Hash Table / update logic to easily rebuild a Movie."""
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "genre": self.genre,
            "rating": self.rating,
            "year": self.year,
            "description": self.description,
        }
