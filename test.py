from avl import *
import numpy as np

def is_avl(root):
    if not root:
        return True, 0

    is_avl_left, height_left = is_avl(root.left)
    is_avl_right, height_right = is_avl(root.right)
    root_height = 1 + max(height_left, height_right)

    if root.balance != height_right - height_left:
        return False, root_height

    return is_avl_left and is_avl_right and (abs(root.balance) <= 1), root_height

def simple():
    tree = Tree()

    node_list = [1,6,2,3,7,4,9]
    for key in node_list:
        tree.insert(Node(key))
        assert(is_avl(tree.root)[0])

    for key in node_list:
        tree.delete(key)
        assert(is_avl(tree.root)[0])

def random():
    tree = Tree()

    # Random numbers from 0 to 99 without duplicates
    node_list = np.random.choice(100, 100, replace=False)
    for key in node_list:
        tree.insert(Node(key))
        assert(is_avl(tree.root)[0])

    for i, key in enumerate(node_list):
        tree.delete(key)
        assert(is_avl(tree.root)[0])

all_tests = [simple, random]

if __name__ == '__main__':
    for test in all_tests:
        test()
    print("Everything passed")