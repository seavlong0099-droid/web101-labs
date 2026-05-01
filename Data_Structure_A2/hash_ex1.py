class HashTable:
    def __init__(self, size=10):
        self.size = size
        # Create a list of 'None' to act as our storage buckets
        self.table = [None] * self.size

    def hash_function(self, key):
        
        return key % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        
        #If the spot is taken, move to the next one
        while self.table[index] is not None:
            # If the key already exists, update the value and return
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.size
            
        self.table[index] = (key, value)

    def search(self, key):
        
        index = self.hash_function(key)
        start_index = index
        
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.size
            if index == start_index: # We've looped back to the start
                break
        return "Not Found"

    def delete(self, key):
        
        index = self.hash_function(key)
        start_index = index
        
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = None
                print(f"Key {key} deleted.")
                return
            index = (index + 1) % self.size
            if index == start_index:
                break
        print("Key not found.")

    def display(self):
        
        print("\n--- Current Hash Table ---")
        for i, item in enumerate(self.table):
            print(f"Index {i}: {item}")
        print("--------------------------\n")

# --- Example Usage ---
my_table = HashTable(10)

# Inserting data
my_table.insert(855, "Cambodia")
my_table.insert(32, "Belgium")
my_table.insert(1, "USA")
my_table.insert(81, "Japan")
my_table.insert(82, "South Korea")
my_table.insert(33, "France")

my_table.display()

# Searching
print(f"Searching for code 855: {my_table.search(855)}") 

# Deleting
my_table.delete(32)
my_table.delete(1)
my_table.display()