# Binary Tree

## Predecessor & Successor

> Predecessor is the "before node", i.e. the previous node in the inorder traversal, or the **largest** node before the current node.

> Successor is the "after node", i.e. the next node in the inorder traversal, or the **smallest** node after the current node.

Let's use successor as an example:

There are two possible situations here:

1. Node has a right child, then the successor is somewhere lower in the tree. To find the successor, go to right once and then find the leftmost child.
2. Node doesn't right child, then the successor is somewhere upper in the tree. Then go up until **the node is the left child of its parent**(this condition is better than parent's val larger than current node's val, since it also cover the equal case), if no such node, there is no successor.

### Implementation

```java
public Node inorderSuccessor(Node n) {
    if (n == null) return null;
    if (n.right != null) {
        n = n.right;
        while (n.left != null) n = n.left;
        return n;
    }
    while (n.parent != null && n.parent.right == n) n = n.parent;
    return n.parent;
}
```

## Inorder Traverse Iteratively
To traverse a binary tree iteratively, we always need a stack. Here are the steps:

1. Initialize a stack, make current node as a root
2. Push current node to stack, and set its left as current node until current node is null
3. If current is NULL and stack is not empty
   1. Pop the top item from the stack
   2. process the item
   3. make its right as current node
4. If current node is NULL and stack is empty, then we are done
```java

public void inorder(TreeNode root) {
    // mimic hte call stack
    Deque<Integer> stack = new ArrayDeque<>();
    TreeNode curr = root;
    // This condition is pretty important, if missing the first condition, it will not traverse the right subtree of the root
    while (curr != null || !stack.isEmpty()) {
        while (curr != null) {
            stack.push(curr);
            curr = curr.left;
        }
        curr = stack.pop();
        process(curr);
        curr = curr.right;
    }
}

private void process(TreeNode root) {
    // do some thing with the node
    System.out.println(root.val);
}

```

## Inorder Traversal with Morris Traversal

The basic idea of Morris Traversal is to find the predecessor and make current root its right children. Then go look at the left subtree of current root. After the left subtree, the program will go back to the root from the rightmost node of its left subtree(which is his predecessor you just linked). This time we need to break this link, and begin to look at the right child of the current root since we have iterate throught the left subtree.

Here are the steps:

1. Make current node as a root
2. If current node has left child
   1. Locate the rightmost node of its left subtree
      1. If reach a leaf, make current root as its right children(successor), then go the left.
      2. If reach it self, meaning the left subtree has been traversed, restore the tree by breaking the link, then go the right.
   2. Make its left child current root
3. If current root has no left child
   1. process current root
   2. Make its right child current root

```java
public void inorder(TreeNode root) {
    TreeNode predecessor = null;
    TreeNode curr = root;

    while (curr != null) {
        if (curr.left != null) {
            predecessor = curr.left;
            while (predecessor.right != null && predecessor.right != curr) predecessor = predecessor.right;
            if (predecessor.right == null) {
                predecessor.right = curr;
                curr = curr.left;
            } else {
                process(curr);
                predecessor.right = null;
                curr = curr.right;
            }
        } else {
            process(curr);
            curr = curr.right;
        }
    }
}
```

## Q114 Flatten Binary Tree to Linked List

### Preorder iterative traversal
```java
class Solution {
    public void flatten(TreeNode root) {
        List<TreeNode> list = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode iter = root;
        while (iter != null || !stack.isEmpty()) {
            if (iter != null) {
                stack.push(iter);
                list.add(iter);
                iter = iter.left;
            } else {
                iter = stack.pop().right;
            }
        }
        for (int i = 0; i < list.size() - 1; i++) {
            list.get(i).left = null;
            list.get(i).right = list.get(i + 1);
        }
    }
}
```

### Constant Space
Look at the relationship between predecessor and successor.
```java
class Solution {
    public void flatten(TreeNode root) {
        TreeNode iter = root;
        while (iter != null) {
            if (iter.left != null) {
                TreeNode temp = iter.left;
                while (temp.right != null) {
                    temp = temp.right;
                }
                temp.right = iter.right;
                iter.right = iter.left;
                iter.left = null;
            } else
                iter = iter.right;
        }
    }
}
```

