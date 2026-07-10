# Hash Table for Contact Management System
# Using Multiplication Method

class ContactHashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    # Multiplication hash function
    def hash_function(self, number):
        A = 0.618033
        index = int(self.size * ((number * A) % 1))
        return index

    # Insert contact
    def insert(self, number, name):
        index = self.hash_function(number)
        self.table[index].append((number, name))
        print("Contact added successfully!")

    # Search contact
    def search(self, number):
        index = self.hash_function(number)

        for contact in self.table[index]:
            if contact[0] == number:
                return contact[1]

        return "Contact not found"

    # Delete contact
    def delete(self, number):
        index = self.hash_function(number)

        for contact in self.table[index]:
            if contact[0] == number:
                self.table[index].remove(contact)
                print("Contact deleted successfully!")
                return

        print("Contact not found")

    # Display contacts
    def display(self):
        print("\nContact List:")
        for i in range(self.size):
            print(f"Index {i}: {self.table[i]}")


# Main Program
contacts = ContactHashTable(10)

# Insert contacts
contacts.insert(12345678, "John")
contacts.insert(87654321, "Alice")
contacts.insert(11223344, "Bob")
contacts.insert(92845374, "Josh")

# Display contacts
contacts.display()

# Search contact
print("\nSearch:", contacts.search(87654321))

# Delete contact
contacts.delete(92845374)

# Display again
contacts.display()
