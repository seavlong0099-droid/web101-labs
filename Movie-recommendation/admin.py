"""
admin.py

Defines the Admin class, which provides movie-management features on
top of the EXISTING MovieDatabase (Hash Table), Graph, and
DecisionTree -- none of those classes are modified in how they work;
Admin just calls their existing methods (plus the new Graph.reset()
helper) to keep everything in sync after a change.

Why a separate Admin class instead of adding these functions to
main.py directly?
- Keeps the "who can do what" boundary explicit and easy to explain.
- main.py stays focused on menu routing / login, not business logic.
"""

from movie import Movie
from utils import (
    print_header,
    print_menu_options,
    print_movie_table,
    print_movie_card,
    print_section,
    get_int_input,
    get_float_input,
    get_yes_no,
)


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

    # ------------------------------------------------------------
    # Keeping the Graph and Decision Tree in sync
    # ------------------------------------------------------------
    def _resync_structures(self):
        """
        Rebuilds the Graph and Decision Tree from the current contents
        of the Hash Table (MovieDatabase). Called after any add,
        update, or delete so similarity edges and recommendation
        rules never go stale.

        This reuses the EXISTING build_graph()/build_tree() methods --
        it just re-runs them against the updated movie list, which is
        simple and safe for a catalog of this size.
        """
        self.graph.reset()
        self.graph.build_graph(self.db.get_all_movies())
        self.tree.build_tree(self.db.all_genres())

    def _next_id(self):
        """Generates a new unique movie ID (existing max ID + 1)."""
        existing_ids = [m.movie_id for m in self.db.get_all_movies()]
        return max(existing_ids, default=0) + 1

    # ------------------------------------------------------------
    # Admin operations (1-8 in the menu)
    # ------------------------------------------------------------
    def add_movie(self):
        """Prompts for movie details and inserts a new Movie via the Hash Table."""
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
        """
        Prompts for a movie ID, then lets the Admin update one or more
        fields (blank input keeps the current value).
        """
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
        """Prompts for a movie ID and removes it after confirmation."""
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
        """Displays every movie in the catalog (Hash Table -> table view)."""
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
        """
        Shows the raw adjacency list of the similarity Graph -- useful
        for an Admin to inspect how movies are currently clustered.
        """
        print_header("Movie Similarity Graph (Adjacency List)")
        listing = self.graph.show_adjacency_list(movie_lookup=self.db.search_by_id)
        print(listing if listing else "  Graph is empty.")

    # ------------------------------------------------------------
    # Admin menu loop
    # ------------------------------------------------------------
    def run_menu(self):
        """
        Runs the Admin menu loop until the Admin chooses to return to
        the main menu or logs out. Returns nothing -- control just
        goes back to main.py's role selection afterward.
        """
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
                "9. Return to main menu",
                "10. Logout",
            ])
            choice = input("Choose an option (1-10): ").strip()

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
                print_section("Returning to main menu.")
                return
            elif choice == "10":
                print_section("Admin logged out.")
                return
            else:
                print_section("Invalid option. Please choose a number from 1 to 10.")
