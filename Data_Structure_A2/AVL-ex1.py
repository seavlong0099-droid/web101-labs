# Node class
class Node:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


# BST class
class BST:
    def __init__(self):
        self.root = None

    # Insertion
    def insert(self, root, name):

        # Create new node if empty
        if root is None:
            return Node(name)

        # Insert on left side
        if name < root.name:
            root.left = self.insert(root.left, name)

        # Insert on right side
        else:
            root.right = self.insert(root.right, name)

        return root

    # Find Maximum value
    def findMax(self, root):

        # Go to the rightmost node
        while root.right:
            root = root.right

        return root.name

    # In-order Traversal
    def inorder(self, root):

        if root:
            self.inorder(root.left)
            print(root.name, end=" ")
            self.inorder(root.right)

    # Delete node
    def delete(self, root, name):

        if root is None:
            return root

        # Search left
        if name < root.name:
            root.left = self.delete(root.left, name)

        # Search right
        elif name > root.name:
            root.right = self.delete(root.right, name)

        else:

            # Case 1: No child
            if root.left is None and root.right is None:
                return None

            # Case 2: One child
            elif root.left is None:
                return root.right

            elif root.right is None:
                return root.left

            # Case 3: Two children
            temp = root.right

            while temp.left:
                temp = temp.left

            root.name = temp.name

            root.right = self.delete(root.right, temp.name)

        return root


# Create BST object
tree = BST()

# Insert values
names = ["Jane", "Bob", "Tom", "Alan", "Ellen", "Nancy", "Wendy"]

for name in names:
    tree.root = tree.insert(tree.root, name)

# In-order Traversal
print("In-order Traversal:")
tree.inorder(tree.root)

# Find Maximum
print("\n\nMaximum Value:", tree.findMax(tree.root))

# Delete a node
tree.root = tree.delete(tree.root, "Tom")

# Display after deletion
print("\nIn-order after deleting Tom:")
tree.inorder(tree.root)
