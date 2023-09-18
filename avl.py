class Tree:
    def __init__(self):
        self.root = None

    def insert(self, node):
        self.root, _ = insert_node(self.root, node)

    def delete(self, key):
        self.root, _ = delete_node(self.root, key)

class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.balance = 0

    def __str__(self):
        output = ''
        grid, _ = draw_node_grid(self)
        for row in grid:
            output += ''.join(row) + '\n'
        
        return output

def insert_node(root, node):
    if not root:
        node.balance = 0
        node.left = None
        node.right = None
        return node, True

    subtree_height_increased = False
    # Insert the node and update the balance factors
    if node.key < root.key:
        root.left, subtree_height_increased = insert_node(root.left, node)
        if subtree_height_increased:
            root.balance -= 1
    elif node.key > root.key:
        root.right, subtree_height_increased = insert_node(root.right, node)
        if subtree_height_increased:
            root.balance += 1
    else:
        raise Exception("No duplicates allowed")
    
    # If AVL variant is breached, then rotate and update balance
    root = balance(root)

    # If subtree_height didn't incrase, tree couldn't have increased
    # If rotated, then root.balance == 0
    # If root.balance != 0, then either 0 to -1, 1
    # Which means that the maximum of left subtree and right subtree height increased
    tree_height_increased = subtree_height_increased and (root.balance != 0)
    return root, tree_height_increased

def delete_node(root, key):
    if not root:
        return None, False

    init_balance = root.balance
    
    # Delete the current node
    if key == root.key:
        if not root.left:
            return root.right, True
        if not root.right:
            return root.left, True

        in_order_successor = root.right
        while (in_order_successor.left):
            in_order_successor = in_order_successor.left
        
        # Delete the in_order_successor from the right subtree
        root.right, subtree_height_decreased = delete_node(root.right, in_order_successor.key)
        if subtree_height_decreased:
            root.balance -= 1

        # Replace the root with the in_order_successor
        # (We want to avoid changing the key directly for application to malloc)
        in_order_successor.left = root.left
        in_order_successor.right = root.right
        in_order_successor.balance = root.balance
        root = in_order_successor
    else:
        # Delete the node in the subtrees
        if key < root.key:
            root.left, subtree_height_decreased = delete_node(root.left, key)
            if subtree_height_decreased:
                root.balance += 1
        elif key > root.key:
            root.right, subtree_height_decreased = delete_node(root.right, key)
            if subtree_height_decreased:
                root.balance -= 1
        
    # Rotate as necessary
    root = balance(root)

    tree_height_decreased = subtree_height_decreased and (abs(init_balance) > abs(root.balance))
    return root, tree_height_decreased

def balance(root):
    if root.balance > 1:
        # Assumption: got inserted to root.right, so root.right is non-null
        if root.right.balance < 0:
            root.right = right_rotate(root.right)
        root = left_rotate(root)
    elif root.balance < -1:
        # Assumption: got inserted to root.left, so root.left is non-null
        if root.left.balance > 0:
            root.left = left_rotate(root.left)
        root = right_rotate(root)

    return root

# https://cs.stackexchange.com/questions/48861/balance-factor-changes-after-local-rotations-in-avl-tree
def left_rotate(root):
    # left_rotate only gets called when root.balance > 0
    # For that to be the case, there needs to be a non-null right node
    assert(root.right)
    right_child = root.right

    # Rotate
    root.right = right_child.left
    right_child.left = root

    # Update balance factors
    # root.balance = root.balance - 1 - max(0, right_child.balance)
    # right_child.balance = right_child.balance - 1 + min(0, root.balance)
    root.balance -= right_child.balance * (right_child.balance > 0) + 1
    right_child.balance += root.balance * (root.balance <= 0) - 1

    # right_child.balance = height(right_child.right) - height(right_child.left)
    # root.balance = height(root.right) - height(root.left)
    return right_child

def right_rotate(root):
    # left_rotate only gets called when root.balance < 0
    # For that to be the case, there needs to be a non-null left node
    assert(root.left)
    left_child = root.left

    # Rotate
    root.left = left_child.right
    left_child.right = root

    # Update balance factors
    # root.balance = root.balance + 1 - min(0, left_child.balance)
    # left_child.balance = left_child.balance + 1 + max(0, root.balance)
    root.balance -= left_child.balance * (left_child.balance < 0) - 1
    left_child.balance += root.balance * (root.balance >= 0) + 1

    # left_child.balance = height(left_child.right) - height(left_child.left)
    # root.balance = height(root.right) - height(root.left)
    return left_child


# TODO: Fix alignment
# TODO: allow for keys of more than 1 length
# Returns a 2D grid of ASCII characters and an int node_col,
# Where the node itself is located on the first row at
# the i'th column
def draw_node_grid(node):
    if not node:
        return [], None

    left_grid, left_node_col = draw_node_grid(node.left)
    left_width = len(left_grid[0]) if left_grid else 0

    right_grid, right_node_col = draw_node_grid(node.right)
    right_width = len(right_grid[0]) if right_grid else 0
    
    total_width = left_width + 1 + right_width
    node_col = left_width
    node_line = [' ' for _ in range(total_width)]
    # For now, assume that len(key_str) = 1
    key_str = str(node.key)
    node_line[node_col] = key_str

    # Offset right_node_col to be right of node_col
    right_node_col = None if (right_node_col is None) else node_col + 1 + right_node_col
    left_edge_len = 0 if (left_node_col is None) else node_col - left_node_col
    right_edge_len = 0 if (right_node_col is None) else right_node_col - node_col

    child_edge_rows = [[' ' for _ in range(total_width)] for _ in range(max(left_edge_len, right_edge_len))]

    # Draw the edge to the left node
    if not left_node_col is None:
        for row_i in range(len(child_edge_rows)):
            if node_col - 1 - row_i > left_node_col:
                child_edge_rows[row_i][node_col - 1 - row_i] = '/'
            else:
                child_edge_rows[row_i][left_node_col] = '|' if row_i != 0 else '/'

    # Draw the edge to the right node
    if not right_node_col is None:
        for row_i in range(len(child_edge_rows)):
            if node_col + 1 + row_i < right_node_col:
                child_edge_rows[row_i][node_col + 1 + row_i] = '\\'
            else:
                child_edge_rows[row_i][right_node_col] = '|' if row_i != 0 else '\\'
    
    child_node_rows = []
    for row_i in range(max(len(left_grid), len(right_grid))):
        line = []
        if row_i < len(left_grid):
            line.extend([' '] * (left_width - len(left_grid[row_i])))
            line.extend(left_grid[row_i])
        else:
            line.extend([' ' for _ in range(left_width)])
        
        line.append(' ')

        if row_i < len(right_grid):
            line.extend(right_grid[row_i])
            line.extend([' '] * (right_width - len(right_grid[row_i])))
        else:
            line.extend([' ' for _ in range(right_width)])

        child_node_rows.append(line)
    
    return [node_line] + child_edge_rows + child_node_rows, node_col
