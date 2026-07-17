"""
decision_tree.py

Implements a rule-based Decision Tree (NOT machine learning).

WHY A DECISION TREE?
---------------------
Recommending a movie is naturally a series of yes/no or multiple-
choice questions: "What genre do you like?" -> "Do you want a
highly-rated movie or are you open to anything?" -> ... Each answer
narrows down the possibilities. A tree structure mirrors this
decision-making process exactly: each internal node is a question,
each branch is an answer, and each leaf is a final decision (a
recommendation rule). This is much clearer to follow and explain
than a single tangled if/elif block.

STRUCTURE
---------
- Root node        : "Which genre do you prefer?"
- Level 1 branches  : one per genre found in the catalog
- Level 2 branches  : "Rating >= 8?" -> Yes / No
- Leaves            : store the filter criteria (genre + min_rating)
                       used to pull matching movies from the
                       MovieDatabase (hash table).

TIME COMPLEXITY
----------------
- Building the tree : O(g) where g = number of distinct genres
- Traversing the tree (making a recommendation) : O(depth) = O(1),
  since the tree only ever has 2 fixed levels (genre, then rating).
  This is far faster than scanning every movie.
"""


class DecisionNode:
    """
    A single node in the Decision Tree.

    - If is_leaf is False, `question` describes what this node asks,
      and `branches` maps an answer (e.g. a genre name, or "yes"/"no")
      to a child DecisionNode.
    - If is_leaf is True, `criteria` holds the final filter rule to
      apply (used by main.py to query the MovieDatabase).
    """

    def __init__(self, question=None, is_leaf=False, criteria=None):
        self.question = question
        self.is_leaf = is_leaf
        self.criteria = criteria or {}
        self.branches = {}   # answer (str) -> DecisionNode

    def add_branch(self, answer, node):
        """Attach a child node for a given answer."""
        self.branches[answer] = node


class DecisionTree:
    """
    Builds and traverses a two-level rule-based decision tree:
    Genre -> Rating threshold -> Recommendation criteria.
    """

    def __init__(self):
        self.root = DecisionNode(question="Preferred Genre?")

    # ------------------------------------------------------------
    def build_tree(self, genres):
        """
        Builds one branch per genre, each splitting further on
        rating. O(g) where g = number of genres.
        """
        for genre in genres:
            genre_node = DecisionNode(question=f"For {genre}, minimum rating?")

            high_rating_leaf = DecisionNode(
                is_leaf=True,
                criteria={"genre": genre, "min_rating": 8.0}
            )
            low_rating_leaf = DecisionNode(
                is_leaf=True,
                criteria={"genre": genre, "min_rating": 0.0}
            )

            genre_node.add_branch("high", high_rating_leaf)   # Rating >= 8
            genre_node.add_branch("low", low_rating_leaf)     # Rating < 8 (no minimum)

            self.root.add_branch(genre.lower(), genre_node)

    # ------------------------------------------------------------
    def recommend(self, genre, wants_high_rating, min_year=None):
        """
        Traverses the tree using the user's answers and returns the
        leaf's filter criteria. O(1) -- fixed tree depth of 2.

        genre             : preferred genre (string)
        wants_high_rating : True -> only rating >= 8 movies
        min_year          : optional extra filter (not part of the
                             tree itself, applied after traversal)
        """
        genre_node = self.root.branches.get(genre.lower())
        if genre_node is None:
            return None   # genre not present in the tree/catalog

        branch_key = "high" if wants_high_rating else "low"
        leaf = genre_node.branches.get(branch_key)
        if leaf is None or not leaf.is_leaf:
            return None

        criteria = dict(leaf.criteria)   # copy so we don't mutate the tree
        if min_year is not None:
            criteria["min_year"] = min_year

        return criteria

    def print_tree(self):
        """Returns a printable string view of the tree structure."""
        lines = [self.root.question]
        for genre_key, genre_node in self.root.branches.items():
            lines.append(f"  |-- {genre_key}")
            lines.append(f"        {genre_node.question}")
            for answer, leaf in genre_node.branches.items():
                label = "Rating >= 8" if answer == "high" else "Rating < 8"
                lines.append(f"          |-- {label} -> "
                              f"Recommend {leaf.criteria.get('genre')} movies "
                              f"(min rating {leaf.criteria.get('min_rating')})")
        return "\n".join(lines)
