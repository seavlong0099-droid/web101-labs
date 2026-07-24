"""
main.py

Entry point for the Movie Recommendation System.

This file contains everything that isn't a core DSA structure:
console helpers (table/card printing), the Admin login, the Admin
menu/operations, and the User menu -- merged in here so the whole
project is just 4 files:

    hash_table.py    -> Movie, HashTable, MovieDatabase, sample data
    graph.py         -> Graph (similarity network)
    decision_tree.py -> DecisionTree (rule-based recommendations)
    main.py          -> console UI + Admin/User menus (this file)

ROLE FLOW
---------
    Role Menu
    ├── Admin -> quick login (username only, NO password) -> Admin menu
    │             (add/update/delete/search/view graph -- all reuse
    │              the existing MovieDatabase/Graph/DecisionTree)
    └── User  -> User menu (view, search, similar movies, recommendation)

SYSTEM WORKFLOW (per movie operation)
---------------------------------------
User/Admin -> Hash Table (fast search) -> Graph (find similar
              movies) -> Decision Tree (filter by genre/rating)
              -> Final Recommendation
"""

import textwrap

from hash_table import Movie, MovieDatabase, get_sample_movies
from graph import Graph
from decision_tree import DecisionTree


# ======================================================================
# Console helpers (formerly utils.py)
# ======================================================================
COL_ID = 4
COL_TITLE = 26
COL_GENRE = 10
COL_RATING = 8
COL_YEAR = 6
TABLE_WIDTH = COL_ID + COL_TITLE + COL_GENRE + COL_RATING + COL_YEAR + 4


def print_header(title):
    """Prints a consistent, centered section header."""
    width = max(TABLE_WIDTH, 40)
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_menu_options(title, options):
    """Generic menu renderer used by the Role, Admin, and User menus."""
    print_header(title)
    for opt in options:
        print(f"  {opt}")
    print("-" * max(TABLE_WIDTH, 40))


def print_section(text):
    """Prints a short labeled sub-section (e.g. a status message)."""
    print(f"\n>> {text}")


def _truncate(text, width):
    text = str(text)
    if len(text) <= width:
        return text
    return text[: width - 3] + "..."


def print_movie_table(movies, title=None):
    """Prints a list of movies as a clean, aligned table."""
    if title:
        print_header(title)

    if not movies:
        print("  No movies found.")
        return

    header = (
        f"{'ID':<{COL_ID}} "
        f"{'Title':<{COL_TITLE}} "
        f"{'Genre':<{COL_GENRE}} "
        f"{'Rating':<{COL_RATING}} "
        f"{'Year':<{COL_YEAR}}"
    )
    print(header)
    print("-" * TABLE_WIDTH)

    for movie in movies:
        row = (
            f"{movie.movie_id:<{COL_ID}} "
            f"{_truncate(movie.title, COL_TITLE):<{COL_TITLE}} "
            f"{_truncate(movie.genre, COL_GENRE):<{COL_GENRE}} "
            f"{str(movie.rating) + '/10':<{COL_RATING}} "
            f"{movie.year:<{COL_YEAR}}"
        )
        print(row)

    print("-" * TABLE_WIDTH)
    print(f"  {len(movies)} movie(s) shown.")


def print_movie_card(movie):
    """Prints a single movie's full details inside a clean bordered card."""
    width = max(TABLE_WIDTH, 40)
    print("\n+" + "-" * (width - 2) + "+")
    print("| " + movie.title.upper().ljust(width - 4) + " |")
    print("+" + "-" * (width - 2) + "+")

    fields = [
        ("Movie ID", movie.movie_id),
        ("Genre", movie.genre),
        ("Rating", f"{movie.rating}/10"),
        ("Release Year", movie.year),
    ]
    for label, value in fields:
        line = f"{label:<14}: {value}"
        print("| " + line.ljust(width - 4) + " |")

    print("| " + "-" * (width - 4) + " |")
    desc_width = width - 4
    words = movie.description.split()
    line = ""
    for word in words:
        candidate = (line + " " + word).strip()
        if len(candidate) > desc_width:
            print("| " + line.ljust(desc_width) + " |")
            line = word
        else:
            line = candidate
    if line:
        print("| " + line.ljust(desc_width) + " |")

    print("+" + "-" * (width - 2) + "+")


def print_similarity_graph(graph, db):
    """
    Prints the similarity Graph as a clean, readable block per movie
    instead of one giant wrapped Python-list line per node:

        [1] The Last Horizon                        (10 connections)
            -> Neon Skyline, Galaxy Runners, Silent Protocol,
               Laugh Track, Office Chaos, ...
        --------------------------------------------------------
    """
    width = max(TABLE_WIDTH, 60)
    movie_ids = sorted(graph.adjacency_list.keys())

    if not movie_ids:
        print("  Graph is empty.")
        return

    for movie_id in movie_ids:
        movie = db.search_by_id(movie_id)
        neighbor_ids = sorted(graph.adjacency_list[movie_id])
        neighbor_names = [db.search_by_id(nid).title for nid in neighbor_ids]

        print(f"\n[{movie_id}] {movie.title}  ({len(neighbor_names)} connections)")

        if neighbor_names:
            wrapped = textwrap.fill(
                ", ".join(neighbor_names),
                width=width - 8,
                initial_indent="    -> ",
                subsequent_indent="       ",
            )
            print(wrapped)
        else:
            print("    -> (no connections)")

        print("-" * width)


def get_int_input(prompt):
    """Reads an integer, re-prompting on invalid input."""
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("  Please enter a valid whole number.")


def get_float_input(prompt):
    """Reads a float, re-prompting on invalid input."""
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("  Please enter a valid number (e.g. 7.5).")


def get_yes_no(prompt):
    """Reads a yes/no answer and returns True/False."""
    while True:
        value = input(prompt).strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("  Please answer 'y' or 'n'.")


# ======================================================================
# Admin login (formerly auth.py) -- NO PASSWORD, username only
# ======================================================================
class Authentication:
    """
    Very lightweight Admin "login" -- just asks for a username so the
    flow still reads as a login step, but does NOT check a password.
    (No database / hashing here on purpose: this project's focus is
    the Hash Table, Graph, and Decision Tree, not security.)
    """

    def login(self):
        """Prompts for a username and always lets the Admin in."""
        print_header("Admin Login")
        username = input("Username: ").strip()
        if not username:
            username = "Admin"
        print(f"Welcome, {username}!")
        return True


# ======================================================================
# Admin (formerly admin.py) -- reuses the existing Hash Table/Graph/Tree
# ======================================================================
class Admin:
    """
    Wraps all Admin-only operations. Holds references to the SAME
    MovieDatabase (Hash Table), Graph, and DecisionTree instances used
    by the User menu, so any change an Admin makes is immediately
    visible to Users too.
    """

    def __init__(self, db, graph, tree):
        self.db = db          # existing MovieDatabase (Hash Table wrapper)
        self.graph = graph    # existing Graph
        self.tree = tree      # existing DecisionTree

    def _resync_structures(self):
        """
        Rebuilds the Graph and Decision Tree from the current Hash
        Table contents. Called after any add/update/delete so
        similarity edges and recommendation rules never go stale.
        """
        self.graph.reset()
        self.graph.build_graph(self.db.get_all_movies())
        self.tree.build_tree(self.db.all_genres())

    def _next_id(self):
        """Generates a new unique movie ID (existing max ID + 1)."""
        existing_ids = [m.movie_id for m in self.db.get_all_movies()]
        return max(existing_ids, default=0) + 1

    def add_movie(self):
        print_header("Add a New Movie")

        title = input("Title: ").strip()
        genre = input("Genre: ").strip()
        rating = get_float_input("Rating (0-10): ")
        year = get_int_input("Release Year: ")
        description = input("Description: ").strip()

        movie = Movie(self._next_id(), title, genre, rating, year, description)
        self.db.insert_movie(movie)   # Hash Table insert: O(1) average
        self._resync_structures()

        print_section(f"Added '{movie.title}' with ID {movie.movie_id}.")

    def update_movie(self):
        print_header("Update Movie Information")
        movie_id = get_int_input("Enter Movie ID to update: ")
        movie = self.db.search_by_id(movie_id)   # Hash Table lookup: O(1) average

        if not movie:
            print_section("Movie not found.")
            return

        print_movie_card(movie)
        print("Press Enter to keep the current value for any field.\n")

        new_title = input(f"Title [{movie.title}]: ").strip()
        new_genre = input(f"Genre [{movie.genre}]: ").strip()
        new_rating = input(f"Rating [{movie.rating}]: ").strip()
        new_year = input(f"Year [{movie.year}]: ").strip()
        new_description = input(f"Description [{movie.description}]: ").strip()

        fields = {}
        if new_title:
            fields["title"] = new_title
        if new_genre:
            fields["genre"] = new_genre
        if new_rating:
            fields["rating"] = float(new_rating)
        if new_year:
            fields["year"] = int(new_year)
        if new_description:
            fields["description"] = new_description

        if not fields:
            print_section("No changes made.")
            return

        self.db.update_movie(movie_id, **fields)   # Hash Table update
        self._resync_structures()
        print_section(f"Movie {movie_id} updated.")

    def delete_movie(self):
        print_header("Delete a Movie")
        movie_id = get_int_input("Enter Movie ID to delete: ")
        movie = self.db.search_by_id(movie_id)   # Hash Table lookup: O(1) average

        if not movie:
            print_section("Movie not found.")
            return

        print_movie_card(movie)
        if not get_yes_no("Are you sure you want to delete this movie? (y/n): "):
            print_section("Delete cancelled.")
            return

        self.db.delete_movie(movie_id)   # Hash Table delete
        self._resync_structures()
        print_section(f"Movie {movie_id} deleted.")

    def display_all_movies(self):
        print_movie_table(self.db.get_all_movies(), title="All Movies (Admin View)")

    def search_by_id(self):
        print_header("Search by ID")
        movie_id = get_int_input("Enter Movie ID: ")
        movie = self.db.search_by_id(movie_id)   # Hash Table lookup: O(1) average
        if movie:
            print_movie_card(movie)
        else:
            print_section("Movie not found.")

    def search_by_title(self):
        print_header("Search by Title")
        title = input("Enter Movie Title: ").strip()
        movie = self.db.search_by_title(title)   # Hash Table lookup: O(1) average
        if movie:
            print_movie_card(movie)
        else:
            print_section("Movie not found.")

    def search_by_genre(self):
        print_header("Search by Genre")
        genre = input("Enter Genre: ").strip()
        movies = self.db.search_by_genre(genre)   # Hash Table lookup: O(1) average
        print_movie_table(movies)

    def view_similarity_graph(self):
        """Shows the similarity Graph in a clean, readable block format."""
        print_header("Movie Similarity Graph")
        print_similarity_graph(self.graph, self.db)

    def run_menu(self):
        """Runs the Admin menu loop until Admin returns to main or logs out."""
        while True:
            print_menu_options("ADMIN MENU", [
                "1. Add a new movie",
                "2. Update movie information",
                "3. Delete a movie",
                "4. Display all movies",
                "5. Search movie by ID",
                "6. Search movie by Title",
                "7. Search movie by Genre",
                "8. View the movie similarity graph",
                "9. Exit",
            ])
            choice = input("Choose an option (1-9): ").strip()

            if choice == "1":
                self.add_movie()
            elif choice == "2":
                self.update_movie()
            elif choice == "3":
                self.delete_movie()
            elif choice == "4":
                self.display_all_movies()
            elif choice == "5":
                self.search_by_id()
            elif choice == "6":
                self.search_by_title()
            elif choice == "7":
                self.search_by_genre()
            elif choice == "8":
                self.view_similarity_graph()
            elif choice == "9":
                print_section("Exiting admin menu.")
                return
            else:
                print_section("Invalid option. Please choose a number from 1 to 9.")


# ======================================================================
# System setup
# ======================================================================
def build_system():
    """Loads sample data and builds MovieDatabase (Hash Table), Graph, DecisionTree."""
    movies = get_sample_movies()

    db = MovieDatabase()
    for movie in movies:
        db.insert_movie(movie)

    graph = Graph()
    graph.build_graph(movies)

    tree = DecisionTree()
    tree.build_tree(db.all_genres())

    return db, graph, tree


# ======================================================================
# User menu (no login required)
# ======================================================================
def handle_view_all(db):
    print_movie_table(db.get_all_movies(), title="All Movies")


def handle_search_by_id(db):
    movie_id = get_int_input("Enter Movie ID: ")
    movie = db.search_by_id(movie_id)   # Hash Table lookup: O(1) average
    if movie:
        print_movie_card(movie)
    else:
        print_section("Movie not found.")


def handle_search_by_title(db):
    title = input("Enter Movie Title: ").strip()
    movie = db.search_by_title(title)   # Hash Table lookup: O(1) average
    if movie:
        print_movie_card(movie)
    else:
        print_section("Movie not found.")


def handle_search_by_genre(db):
    genre = input("Enter Genre: ").strip()
    movies = db.search_by_genre(genre)   # Hash Table lookup: O(1) average
    print_movie_table(movies)


def handle_similar_movies(db, graph):
    movie_id = get_int_input("Enter Movie ID: ")
    movie = db.search_by_id(movie_id)
    if not movie:
        print_section("Movie not found.")
        return

    similar_ids = graph.find_similar_movies(movie_id)   # Graph adjacency lookup
    if not similar_ids:
        print_section(f"No similar movies found for '{movie.title}'.")
        return

    similar_movies = [db.search_by_id(mid) for mid in similar_ids]
    print_movie_table(similar_movies, title=f"Similar to: {movie.title}")

    if get_yes_no("\nShow full similarity network (BFS traversal)? (y/n): "):
        bfs_order = graph.bfs(movie_id)
        print_movie_table(
            [db.search_by_id(mid) for mid in bfs_order],
            title="BFS Order (closest similarity first)",
        )


def handle_recommendation(db, graph, tree):
    available_genres = db.all_genres()
    print("  Available genres: " + ", ".join(available_genres))
    genre = input("Enter your preferred genre: ").strip()

    if genre.lower() not in [g.lower() for g in available_genres]:
        print_section("That genre isn't in the catalog.")
        return

    wants_high_rating = get_yes_no("Do you want highly-rated movies only (rating >= 8)? (y/n): ")

    # Traverse the Decision Tree to get filter criteria
    criteria = tree.recommend(genre, wants_high_rating)
    if criteria is None:
        print_section("No recommendation rule found for that genre.")
        return

    # Apply the criteria using the Hash Table (fast genre lookup)
    candidates = db.search_by_genre(criteria["genre"])
    results = [m for m in candidates if m.rating >= criteria["min_rating"]]
    results.sort(key=lambda m: m.rating, reverse=True)

    print_movie_table(
        results,
        title=f"Recommended: {criteria['genre']} (min rating {criteria['min_rating']})",
    )

    # Use the Graph to also suggest movies related to the top pick,
    # completing the Hash Table -> Graph -> Decision Tree pipeline.
    if results:
        top_pick = results[0]
        related_ids = graph.find_similar_movies(top_pick.movie_id)
        if related_ids:
            result_ids = [m.movie_id for m in results]
            related_movies = [db.search_by_id(mid) for mid in related_ids
                               if mid not in result_ids]
            if related_movies:
                print_movie_table(
                    related_movies[:5],
                    title=f"Because you liked: {top_pick.title}",
                )


def run_user_menu(db, graph, tree):
    """User menu loop -- no login required."""
    while True:
        print_menu_options("USER MENU", [
            "1. View Movies",
            "2. Search by ID",
            "3. Search by Title",
            "4. Search by Genre",
            "5. Similar Movies",
            "6. Recommendation",
            "7. Exit",
        ])
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            handle_view_all(db)
        elif choice == "2":
            handle_search_by_id(db)
        elif choice == "3":
            handle_search_by_title(db)
        elif choice == "4":
            handle_search_by_genre(db)
        elif choice == "5":
            handle_similar_movies(db, graph)
        elif choice == "6":
            handle_recommendation(db, graph, tree)
        elif choice == "7":
            print_section("Returning to main menu.")
            return
        else:
            print_section("Invalid option. Please choose a number from 1 to 7.")


# ======================================================================
# Role menu / main loop
# ======================================================================
def run_admin_flow(db, graph, tree):
    """Directly opens the Admin menu when the user selects Admin."""
    Admin(db, graph, tree).run_menu()


def main():
    db, graph, tree = build_system()

    while True:
        print_menu_options("MOVIE RECOMMENDATION SYSTEM", [
            "1. Admin",
            "2. User",
            "3. Exit",
        ])
        choice = input("Choose a role (1-3): ").strip()

        if choice == "1":
            run_admin_flow(db, graph, tree)
        elif choice == "2":
            run_user_menu(db, graph, tree)
        elif choice == "3":
            print("\nThank you for using the Movie Recommendation System!")
            break
        else:
            print_section("Invalid option. Please choose a number from 1 to 3.")


if __name__ == "__main__":
    main()

