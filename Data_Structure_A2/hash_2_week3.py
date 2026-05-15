import hashlib

# Hash table using dictionary
users = {}

# Division hash function
def hash_function(password):
    total = 0

    # Convert password characters to ASCII values
    for char in password:
        total += ord(char)

    # Division method
    return total % 10


# Function to hash password
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Main program
while True:
    print("\nPassword Hash Table System")
    print("\n1. Register User")
    print("\n2. Login User")
    print("\n3. Display Users (Hashed)")
    print("\n4. Exit")

    choice = input("\nChoose an option (1-4): ")

    # Register User
    if choice == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Division hash index
        index = hash_function(password)

        # Encrypt password
        hashed_password = encrypt_password(password)

        # Store in hash table
        users[username] = hashed_password

        print("User registered successfully!")
        print("Hash Index:", index)

    # Login User
    elif choice == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")

        hashed_password = encrypt_password(password)

        if username in users and users[username] == hashed_password:
            print("Login successful!")
        else:
            print("Invalid username or password!")

    # Display Users
    elif choice == "3":
        print("\nStored Users (Hashed Passwords)\n")

        for username, hashed in users.items():
            print(username, hashed)

    # Exit
    elif choice == "4":
        print("Exiting program...")
        break

    else:
        print("Invalid option!")