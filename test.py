from avl import *

def is_avl(root):
    if not root:
        return True, 0

    is_avl_left, height_left = is_avl(root.left)
    is_avl_right, height_right = is_avl(root.right)
    root_height = 1 + max(height_left, height_right)

    assert(root.balance == height_right - height_left)

    return (abs(root.balance) <= 1), root_height

def simple():
    tree = Tree()

    node_list = [1,6,2,3,7,4,9]
    for key in node_list:
        tree.insert(Node(key))
        assert(is_avl(tree.root))

    for key in node_list:
        tree.delete(key)
        assert(is_avl(tree.root))

all_tests = [simple]

if __name__ == '__main__':
    for test in all_tests:
        test()
    print("Everything passed")