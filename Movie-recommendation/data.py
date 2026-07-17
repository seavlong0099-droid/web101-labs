"""
data.py

Sample movie catalog used to populate the system on startup.
18 movies across several genres so the Hash Table, Graph, and
Decision Tree all have enough data to demonstrate their behavior.
"""

from movie import Movie


def get_sample_movies():
    """Returns a list of Movie objects representing the sample catalog."""
    # Ratings and years are deliberately spread out (not bunched together)
    # so that the similarity Graph forms distinct clusters instead of
    # nearly connecting every movie to every other movie.
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
