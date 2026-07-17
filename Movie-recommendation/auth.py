"""
auth.py

A small Authentication class that handles Admin login only (the User
role requires no login, per the requirements).

This is intentionally simple -- hardcoded credentials, no database,
no hashing -- because the goal of this project is to demonstrate
Hash Table / Graph / Decision Tree usage, not a security system.
"""


class Authentication:
    """Handles the Admin login flow using hardcoded credentials."""

    # Hardcoded Admin credentials (no database required, as specified).
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"

    MAX_ATTEMPTS = 3

    def login(self):
        """
        Prompts for a username and password up to MAX_ATTEMPTS times.
        Returns True if the credentials match, False otherwise.
        """
        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            print(f"\n-- Admin Login (attempt {attempt}/{self.MAX_ATTEMPTS}) --")
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            if username == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD:
                print("Login successful.\n")
                return True

            print("Incorrect username or password.")

        print("Too many failed attempts. Returning to the main menu.\n")
        return False
