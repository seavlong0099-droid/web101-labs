# Node class
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# BST class
class BST:
    def __init__(self):
        self.root = None

    # INSERTION
    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):

        if node is None:
            return Node(value)

        if value < node.value:
            node.left = self._insert(node.left, value)

        elif value > node.value:
            node.right = self._insert(node.right, value)

        return node

    # SEARCH
    def search(self, node, value):

        if node is None:
            return False

        if node.value == value:
            return True

        if value < node.value:
            return self.search(node.left, value)

        return self.search(node.right, value)

    # FIND MIN
    def findMin(self, node):

        while node.left is not None:
            node = node.left

        return node.value

    # DELETE
    def delete(self, node, value):

        if node is None:
            return node

        # Go left
        if value < node.value:
            node.left = self.delete(node.left, value)

        # Go right
        elif value > node.value:
            node.right = self.delete(node.right, value)

        # Node found
        else:

            # Case 1: No child
            if node.left is None and node.right is None:
                return None

            # Case 2: One child
            elif node.left is None:
                return node.right

            elif node.right is None:
                return node.left

            # Case 3: Two children
            temp = self.findMinNode(node.right)

            node.value = temp.value

            node.right = self.delete(node.right, temp.value)

        return node

    def findMinNode(self, node):

        while node.left is not None:
            node = node.left

        return node

    # INORDER TRAVERSAL
    def inorder(self, node):

        if node:
            self.inorder(node.left)
            print(node.value, end=" ")
            self.inorder(node.right)

    # PREORDER TRAVERSAL
    def preorder(self, node):

        if node:
            print(node.value, end=" ")
            self.preorder(node.left)
            self.preorder(node.right)

    # POSTORDER TRAVERSAL
    # Right -> Left -> Root
    def postorder(self, node):

        if node:
            self.postorder(node.right)
            self.postorder(node.left)
            print(node.value, end=" ")


# Create BST object
tree = BST()

# Insert values from Exercise 1
values = ["Jane", "Bob", "Tom", "Alan", "Ellen", "Nancy", "Wendy"]

for value in values:
    tree.insert(value)

# Inorder Traversal
print("Inorder Traversal:")
tree.inorder(tree.root)

# Preorder Traversal
print("\nPreorder Traversal:")
tree.preorder(tree.root)

# Postorder Traversal
print("\nPostorder Traversal:")
tree.postorder(tree.root)

# Search
print("\n\nSearch 8:")
print(tree.search(tree.root, 8))

# Find Minimum
print("\nMinimum Value:")
print(tree.findMin(tree.root))

# Delete node 10
tree.root = tree.delete(tree.root, 10)

# Display after deletion
print("\nInorder after deleting 10:")
tree.inorder(tree.root)