class TreeNode:

    def __init__(self, val, left: 'TreeNode'=None, right: 'TreeNode'= None):
        self.val = val
        self.left = left
        self.right = right
    
    def __str__(self):
        return f"TreeNode({self.val})"

class BinaryTreeIterator:

    def __init__(self, root: TreeNode, reverse=False):
        self.stack = []
        self.reverse = reverse
        self._pushAll(root)

    def hasNext(self):
        return len(self.stack) > 0
    
    def next(self):
        if not self.hasNext():
            raise StopIteration("No more elements in the tree")
        
        node = self.stack[-1]
        
        return node.val
    
    def moveToNext(self):
        if not self.hasNext():
            raise StopIteration("No more elements in the tree")
        
        node = self.stack.pop()
        if not self.reverse:
            self._pushAll(node.right)
        else:
            self._pushAll(node.left)
        
        return node.val
    
    def _pushAll(self, node: TreeNode):
        while node:
            self.stack.append(node)
            if not self.reverse:
                node = node.left
            else:
                node = node.right

    

# Example usage
if __name__ == "__main__":
    # Constructing a binary tree
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    # In-order traversal (left to right)
    print("In-order traversal:")
    iterator = BinaryTreeIterator(root)
    while iterator.hasNext():
        print(iterator.moveToNext())

    # Reverse in-order traversal (right to left)
    print("\nReverse in-order traversal:")
    reverse_iterator = BinaryTreeIterator(root, reverse=True)
    while reverse_iterator.hasNext():
        print(reverse_iterator.moveToNext())
    

    # Two Pointer approach in bst to find if there is a pair with given sum
    target = 25
    rootNode = TreeNode(10)
    rootNode.left = TreeNode(5)
    rootNode.right = TreeNode(15)
    rootNode.left.left = TreeNode(3)
    rootNode.left.right = TreeNode(7)
    rootNode.right.right = TreeNode(18)

    left_iterator = BinaryTreeIterator(rootNode)
    right_iterator = BinaryTreeIterator(rootNode, reverse=True)
    found_pair = False

    while left_iterator.hasNext() and right_iterator.hasNext():
        left_val = left_iterator.next()
        right_val = right_iterator.next()

        if left_val >= right_val:
            break  # No more pairs to check

        current_sum = left_val + right_val
        if current_sum == target:
            print(f"Pair found: ({left_val}, {right_val})")
            found_pair = True
            left_iterator.moveToNext()  # Move left pointer forward
            right_iterator.moveToNext()  # Move right pointer backward
        elif current_sum < target:
            left_iterator.moveToNext()  # Move left pointer forward
        else:
            right_iterator.moveToNext()  # Move right pointer backward
        
    if not found_pair:
        print("No pair found with the given sum.")
    