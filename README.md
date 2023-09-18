# AVL Trees
An implementation of an AVL tree which only uses 2 extra bits per node for balance factor, with simpler branching for rotations. 

Background: I needed to implement an AVL tree for a dynamic memory allocator with a garbage collector in C for a course assignment. Most examples online of an AVL tree implementations either required storing the height at each node (which is not optimal for space-efficiency in a memory allocator). The Wikipedia pseudocode only used balance-factors (which requires 2 extra bits per node), but it was a bit non-intuitive to follow, with a lot of branching cases.

For my own learning purposes, I thought I'd write up an AVL tree using only balance factors as the additional information per node, as well as handling the rotation/balance-restoring more simply. (And also test/learn more quickly by implementing some simple visualisation for trees - this is still WIP.)
