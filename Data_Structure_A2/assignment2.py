class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# --- Setup ---
cart = []

print("Welcome to the Python Shop!")

while True:
    print("\n1. Add Item")
    print("2. View Cart & Total")
    print("3. Remove Last Item")
    print("4. Checkout & Exit")
    
    choice = input("\nSelect an option (1-4): ")

    # Conditionals for menu selection
    if choice == "1":
        item_name = input("Enter product name: ")
        item_price = float(input("Enter product price: "))
        
        # Create a Product object and add to List
        new_item = Product(item_name, item_price)
        cart.append(new_item)
        print(f"Added {item_name} to cart.")

    elif choice == "2":
        if not cart:
            print("Your cart is empty!")
        else:
            print("\n--- Your Cart ---")
            total = 0
            for item in cart:
                print(f"- {item.name}: ${item.price:.2f}")
                total += item.price
            print(f"Total Cost: ${total:.2f}")

    elif choice == "3":
        if cart:
            removed = cart.pop() # Removes the last item added
            print(f"Removed {removed.name} from cart.")
        else:
            print("Nothing to remove!")

    elif choice == "4":
        print("Thank you for shopping!")
        break

    else:
        print("Invalid choice, please try again.")