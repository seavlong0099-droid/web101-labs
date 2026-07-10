# Node class
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


# AVL Tree class
class AVLTree:

    # Get height
    def get_height(self, root):
        if not root:
            return 0
        return root.height

    # Get balance factor
    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    # Right rotation
    def right_rotate(self, z):

        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))

        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        return y

    # Left rotation
    def left_rotate(self, z):

        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))

        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        return y

    # Insert node
    def insert(self, root, val):

        if not root:
            return Node(val)

        if val < root.key:
            root.left = self.insert(root.left, val)

        else:
            root.right = self.insert(root.right, val)

        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and val < root.left.key:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and val > root.right.key:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and val > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and val < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # Find minimum value node
    def find_min(self, root):

        if root is None or root.left is None:
            return root

        return self.find_min(root.left)

    # Delete node
    def delete(self, root, val):

        if not root:
            return root

        # Find node to delete
        if val < root.key:
            root.left = self.delete(root.left, val)

        elif val > root.key:
            root.right = self.delete(root.right, val)

        else:

            # Node with one child or no child
            if root.left is None:
                return root.right

            elif root.right is None:
                return root.left

            # Node with two children
            temp = self.find_min(root.right)

            root.key = temp.key

            root.right = self.delete(root.right, temp.key)

        # Update height
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        # Check balance
        balance = self.get_balance(root)

        # Left Left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Left Right
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Right Left
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # Search node
    def search(self, root, val):

        if root is None:
            return False

        if root.key == val:
            return True

        if val < root.key:
            return self.search(root.left, val)

        return self.search(root.right, val)

    # Display inorder traversal
    def inorder(self, root):

        if root:
            self.inorder(root.left)
            print(root.key, end=" ")
            self.inorder(root.right)


# Main program
tree = AVLTree()
root = None

values = [15, 18, 25, 22, 19, 13, 10]

# Insert values
for v in values:
    root = tree.insert(root, v)

# Display inorder
print("Inorder Traversal:")
tree.inorder(root)

# Search value
print("\n\nSearch 22:")
print(tree.search(root, 22))

# Delete value
root = tree.delete(root, 18)

# Display after delete
print("\nInorder After Deleting 18:")
tree.inorder(root)