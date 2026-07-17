"""
utils.py

Small helper functions used by main.py to keep the menu/display code
clean and avoid repeating formatting logic everywhere.

This version renders movie lists as clean, aligned console tables
instead of raw one-line dumps.
"""

# Fixed column widths used by the movie table (kept in one place so
# the header and every row always line up).
COL_ID = 4
COL_TITLE = 26
COL_GENRE = 10
COL_RATING = 8
COL_YEAR = 6

TABLE_WIDTH = COL_ID + COL_TITLE + COL_GENRE + COL_RATING + COL_YEAR + 4  # + spacing


def print_header(title):
    """Prints a consistent, centered section header."""
    width = max(TABLE_WIDTH, 40)
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_menu_options(title, options):
    """
    Generic, reusable menu renderer: prints a header followed by a
    list of option strings. Used for the Role menu (Admin/User), the
    User menu, and the Admin menu so they all look consistent.
    """
    print_header(title)
    for opt in options:
        print(f"  {opt}")
    print("-" * max(TABLE_WIDTH, 40))


def print_menu():
    """Prints the (User-facing) main menu options."""
    print_menu_options("MOVIE RECOMMENDATION SYSTEM", [
        "1. View Movies",
        "2. Search by ID",
        "3. Search by Title",
        "4. Search by Genre",
        "5. Similar Movies",
        "6. Recommendation",
        "7. Exit",
    ])


def _truncate(text, width):
    """Shortens text to fit a column, adding '...' if it was cut off."""
    text = str(text)
    if len(text) <= width:
        return text
    return text[: width - 3] + "..."


def _table_border(char="-"):
    return char * TABLE_WIDTH


def print_movie_table(movies, title=None):
    """
    Prints a list of movies as a clean, aligned table:

    ID    Title                      Genre        Rating    Year
    ------------------------------------------------------------
    1     The Last Horizon           Sci-Fi        6.3/10   2005
    ...
    """
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
    print(_table_border())

    for movie in movies:
        row = (
            f"{movie.movie_id:<{COL_ID}} "
            f"{_truncate(movie.title, COL_TITLE):<{COL_TITLE}} "
            f"{_truncate(movie.genre, COL_GENRE):<{COL_GENRE}} "
            f"{str(movie.rating) + '/10':<{COL_RATING}} "
            f"{movie.year:<{COL_YEAR}}"
        )
        print(row)

    print(_table_border())
    print(f"  {len(movies)} movie(s) shown.")


# Kept as an alias so any older call sites still work; new code should
# prefer print_movie_table for the clean tabular view.
def print_movie_list(movies, title=None):
    print_movie_table(movies, title=title)


def print_movie_card(movie):
    """
    Prints a single movie's full details inside a clean bordered card.
    Used for "Search by ID" and "Search by Title" single-result views.
    """
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
    # Wrap the description across multiple lines so it stays inside the card
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


def print_section(text):
    """Prints a short labeled sub-section inside a menu flow (e.g. a note)."""
    print(f"\n>> {text}")


def get_int_input(prompt):
    """Reads an integer from the user, re-prompting on invalid input."""
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("  Please enter a valid whole number.")


def get_float_input(prompt):
    """Reads a float from the user, re-prompting on invalid input."""
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
