# Basic Knowledge
Note from leetcode, some useful snippets and lemma.

## Expend subarray


## Binary Search


## Maximum Subarray


## Backtrack
Begin with Q39 Combination Sum

> Backtracking is a general algorithm for finding all solutions to some computational problems, notably constranit satisfaction problems. It incrementally builds candidates to the solutions, and abandons a candidate (**"backtrack"**) as soon as it determines the candidates are unlikely to form a valid solutions.

There are several core points in a backtracking algorithm:

 * Result set: store all feasible solutions
 * Track: an ordered collection. When the algorithm traverse down a branch, the trace will be stored in this collection.
 * Extension: possible next step extending current path.
 * Accepted: the track satisfies constraint, and will be stored into Restult set
 * Reject: the track can be proved to be infeasible, unnecessary to traverse down any more.

Here is the psedocode, P is the data, c is the partial candidate:

```
procedure bt(c)
    if reject(P, c) then return
    if accept(P, c) then output(P, c)

    s <- first(P, c)
    while s != NULL
        bt(s)
        s <- next(P, s)
```

Here is a example in Java:

```java
class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        // Construct the result set
        List<List<Integer>> res = new ArrayList<>();
        // initialize the algorithm, bt(root(P)), initialize a empty track
        // which can be reused, the result set will be populated after the 
        // method returning
        dfs(res,new ArrayList<Integer>(),candidates,target,0);
        return res;
    }

    /*
    Given current partial solution candidate, extend it with all posibility. If  
    */
    private void dfs(List<List<Integer>> res, List<Integer> cur, int [] candidates, int target, int index){
        // accepted
        if(target == 0){
            res.add(new ArrayList<>(cur));
        }

        for(int i = index; i < candidates.length; i++){
            // prune the infeasible candidate (reject)
            if(target >= candidates[i]) {
                // extend current path
                cur.add(candidates[i]);
                // traverse down
                dfs(res, cur, candidates, target - candidates[i], i);
                // !!!key: backtrack after reject or accpet: restore the
                // track so that we can try next extension.
                cur.remove(cur.size() - 1);
            }
        }
    }
}
```

Note: for the problem above, sorting ahead helps pruning the tree, i.e. when target is less than a candidates, it can break from the iteration directly.

A key point for backtrack is that: you need to **restore the state** before trying the next extension. For example, remove the last step from the track; restore the candidates to the state before recursion: 

```java
// Q46 Permutation Snippet
private void backTrack(int[] nums, List<Integer> track, int first) {
        if (first == nums.length) result.add(new ArrayList<>(track));
        
        for (int i = first; i < nums.length; i++) {
            track.add(nums[i]);
            swap(nums, first, i);
            backTrack(nums, track, first + 1);
            // must perform completed restore, otherwise the candidate nums will
            // be mess up
            swap(nums, first, i);
            track.remove(track.size() - 1);
        }
    }
```

## Q884 Backspace String Compare

For this problem, we can first know that future backspace will delete character that has been 
seen, so we cannot decide which character is in the finally string. Since the string is immutable we cannot swap the char to get the finally string.

However, the key trick is that if we go **reversely**, every time there is a backspace, we can skip the next non-backspace character. So every character left must be in the fianlly String.


## Q48 Rotate Image
* **Clockwise**: transpose and then reverse each row
* **Anticlockwise**: transpose and then reverse each column

## Q155 Min Stack

It is pretty important to the find the invariants when solving problem. For a stack after a element *x* being inserted, the part below it will never change as long as *x* remains in the stack. 

Having observed that, we can record the minimum value so far along with each element, then we can always learn the minimum of the stack by definition of the value stored with the actual data.

## Q62 Unique Path

While this problem can be down by dynamic programming, it is actually a combinatorial problem: pick h going downs from h+v steps(h = m - 1, v = n - 1).

## Negative Modulos in Java

In Java, modulus and reminders are different. Modulus are always positive, while the reminders can be negative. And in Java, the binary operator `%` are defined to produce a result such that `(a / b) * b + (a % b) is equal to a`. `abs((a / b) * b)` must be less that a, so in the case `a` is negative, the result of `%` will be negative.

To get the modulus, there are two cases: 

  1. If `a > 0`, modulus equals to reminder `a % b`
  2. If `a < 0`, modulus equals to `(a % b) + abs(b)`

## Q94 Inorder Traversal

The most straightforward method is recursion. We can also mimic the call stack with a actual stack, to avoid recursion:

```java

public List<Integer> inorder(TreeNode root) {
    List<Integer> l = new ArrayList<>();
    Stack<TreeNode> s = new Stack<>();
    TreeNode curr = root;
    while (!s.empty() || curr != null) {
        while (curr != null) {
            s.push(curr);
            curr = curr.left;
        }
        curr = s.pop();
        l.add(curr.val);
        curr = curr.right;
    }
}
```

The detail for this implementation is pretty important. That is when to pop and push the stack, and how to move the pointer. Every outer while loop can be regarded as a function call(exclude the right subtree). If curr is null, this call will just return, and if there is nothing in the call stack, the traversal just terminate. If there is a node in the stack, meaning we reach the leftmost, we can do something for current node, and begin to traversal the right subtree. 

Another approach is **Morris Traversal**:

### Morris Traversal:

Threaded Binary Tree can be traversed without **extra space**.

#### Definition
> "A binary tree is threaded by making all **right** child pointers that would normally be null point to the in-order **successor** of the node (if it exists), and all **left** child pointers that would normally be null point to the in-order **predecessor** of the node."

#### Strategy

If current node has no left child, 

  1. Do something for its data
  2. Go to its right child

Else,

  1. Look at its left subtree, its rightmost node will be the predecessor of current node. (Threading)
  2. Go to the left child.

#### Implementation

```java
public List<Integer> inorder(TreeNode root) {
    TreeNode curr = root;
    List<Integer> re = new ArrayList<>();
    TreeNode re;
    while (curr != null) {
        if (curr.left == null) {
            re.add(curr.val);
            curr = curr.right;
        } else {
            pre = curr.left;
            while (pre.right != null) {
                pre = pre.right;
            }
            pre.right = curr;
            curr = curr.left;
            pre.right.left = null; // This is essential, it actually move the left subtree to the top, which prevents cycle.
        }
    }
    return re;
}
```

####  Complexity

For this implementation, the time complexity is actually `O(n)`. The reason is a binary tree with `n` nodes has `n - 1` edges. During the whole process, each eage will be touched at most twice: 1. locate the node downside; 2. Find the predecessor(rightmost node of left subtree). 

To prove the second reason, we can think this way: after been used for find predecessor, the left subtree `curr.left` will be the new top of the binary tree, `curr` will be put below the rightmost node. In the later process, the edges between `curr` and `curr.left` will never be used for find predecessor, since they have no chance to in the left subtree of any new root. 