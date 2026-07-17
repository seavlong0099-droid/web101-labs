"""
main.py

Entry point for the Movie Recommendation System.

This now starts with a ROLE selection (Admin / User) instead of going
straight into the movie menu:

    Role Menu
    ├── Admin -> Authentication.login() -> Admin(...).run_menu()
    │             (add/update/delete/search/view graph -- all reuse
    │              the existing MovieDatabase/Graph/DecisionTree)
    └── User  -> run_user_menu(...)  (unchanged from before: view,
                 search, similar movies, recommendation)

SYSTEM WORKFLOW (per movie operation, same as before)
-------------------------------------------------------
User/Admin -> Hash Table (fast search) -> Graph (find similar
              movies) -> Decision Tree (filter by genre/rating)
              -> Final Recommendation

All DSA logic still lives only in hash_table.py, graph.py, and
decision_tree.py -- main.py only routes between the Admin and User
menus, and Admin operations live in admin.py.
"""

from data import get_sample_movies
from hash_table import MovieDatabase
from graph import Graph
from decision_tree import DecisionTree
from auth import Authentication
from admin import Admin
from utils import (
    print_menu_options,
    print_movie_table,
    print_movie_card,
    print_section,
    get_int_input,
    get_yes_no,
)


def build_system():
    """
    Loads sample data and builds the three core structures:
    MovieDatabase (Hash Table), Graph, and DecisionTree.
    """
    movies = get_sample_movies()

    db = MovieDatabase()
    for movie in movies:
        db.insert_movie(movie)

    graph = Graph()
    graph.build_graph(movies)

    tree = DecisionTree()
    tree.build_tree(db.all_genres())

    return db, graph, tree


# ------------------------------------------------------------------
# User menu handlers (unchanged behavior from the original project)
# ------------------------------------------------------------------
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


# ------------------------------------------------------------------
# Role menu / main loop
# ------------------------------------------------------------------
def run_admin_flow(db, graph, tree):
    """Handles Admin login, then hands off to Admin.run_menu() on success."""
    if Authentication().login():
        Admin(db, graph, tree).run_menu()
    else:
        print_section("Returning to main menu.")


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
