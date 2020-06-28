# Basic Knowledge
Note from leetcode, some useful snippets and lemma.

## Expend subarray


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

In Java, modulus and reminders are different. Modulus are always positive, while the reminders can be negative. And in Java, the binary operator `%` are defined to produce a result such that `(a / b) * b + (a % b) is equal to a`. `abs((a / b) * b)` must be less that `abs(a)`, so in the case `a` is negative, the result of `%` will be negative.

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

The detail for this implementation is pretty important. That is when to pop and push the stack, and how to move the pointer. Every outer while loop can be regarded as a function call(exclude the right subtree). If curr is null, this call will just return, and if there is nothing in the call stack, the traversal just terminate. If there is a node in the stack, meaning we return from left side call, we can do something for current node, and begin to traversal the right subtree. 

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

## Q102 Symmetric Tree

## Key Point
A tree is symmetric if its left subtree is mirror symmetric to its right subtree. Obviously, it should be mirror symetric to itself.

Hence, we can solve this problem using recursively, compare the key of two trees, and one's left subtree to the other's right subtree and one's right to the other's left.

This problem can also be solved iteratively with a queue and tuning the order of offering node.

```java
public boolean symmetric(TreeNode root) {
    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);
    q.offer(root);

    TreeNode t1;
    TreeNode t2;
    while(!q.empty()) {
        t1 = q.poll();
        t2 = q.poll();
        if (t1 == null && t2 == null) continue;
        if (t1 == null || t2 == null || t1.val != t2.val) return false;

        // The order are important, it guarantees that you actually poll()
        // two node should be compared(to be symetric).
        q.offer(t1.left);
        q.offer(t2.right);
        q.offer(t1.right);
        q.offer(t2.left);
    }
    return true;
}
```


## Q105 Construct Binary Tree from Preorder and Inorder Traversal

### Iterative Implementation
```java
public TreeNode buildTree(int[] preorder, int[] inorder) {
    if (preorder == null || inorder == null || preorder.length == 0 || preorder.length != inorder.length) return null;
    Deque<TreeNode> s = new LinkedList<>();
    int i = 0;
    TreeNode root = new TreeNode(preorder[0]);
    s.push(root);
    TreeNode cur;
    for (int j = 1; j < preorder.length; j++) {
        cur = s.peek();
        if (cur.val != inorder[i]) {
            cur.left = new TreeNode(preorder[j]);
            cur = cur.left;
            s.push(cur);
        }
        else {
            while (!s.isEmpty() && inorder[i] == s.peek().val) {
                cur = s.pop();
                i++;
            }
            cur.right = new TreeNode(preorder[j]);
            cur = cur.right;
            s.push(cur);
        }
    }
    return root;
}
```

## Q1008 Construct Binary Search Tree from Preorder Traversal

Similar to the problem above, this is another problem to construct Binary Tree. It can be reduced to previous problem, which takes `O(n^2)` at worst, or `O(nlogn)` for a balance tree. (Sort the preorder to get inorder then it can be guaranteed to be `O(nlogn)` with HashMap).

```java
 public TreeNode bstFromPreorder(int[] preorder) {
    return help(preorder, 0, preorder.length - 1);
}
    
private TreeNode help(int[] pre, int left, int right) {
    if (left > right) return null;
    if (left == right) return new TreeNode(pre[left]);
    
    TreeNode re = new TreeNode(pre[left]);
    int i = left;
    while (i <= right) {
        if (pre[i] > pre[left]) break;
        i++;
    }
    re.left = help(pre, left + 1, i - 1);
    re.right = help(pre, i, right);
    return re;
}
```

However, there are still faster solution that only takes `O(n)`. The basic idea is to imitate how preorder traverse the tree. Given the preorder array, if you iterate through the array, you are actually traverse the underlying tree in preorder. Hence, at `preorder[i]`, you can first constuct the TreeNode, then construct the left and right node recursively. And `preorder[i]` is not only the value of current node, but also a **seperate** for its left subtree can right subtree int later array.

For example, `[8, 5, 1, 7, 10, 12]`, when you are at the first node, you don't need to find the next larger value 10 explicitly (like implementation above), you just tell the left subtree it should never go beyond 8. Then, only element before 10 will be used to construct left subtree.

Note: Using a global variable can help us to locate in the array.

```java
class Solution {
    int idx;
    public TreeNode bstFromPreorder(int[] preorder) {
        this.idx = 0;
        return help(preorder, Integer.MIN_VALUE, Integer.MAX_VALUE);
    }
    
    private TreeNode help(int[] pre, int low, int high) {
        if (this.idx == pre.length) return null;
        int val = pre[this.idx];
        
        if (val < low || val > high) return null;
        
        TreeNode re = new TreeNode(val);
        this.idx++;
        re.left = help(pre, low, val);
        re.right = help(pre, val, high);
        return re;
    }
}
```

### Iterative Impelementation 

Use stack to convert recursion into iteration. The stack containing nodes are similar to the call stack in resursion. When finished construct left subtree, we will push another call into the stack. And we can intimate that explicitly in stack: when the next value is larger than a node's val but less than its parent's, we know that the next value must be the right child of this node. 

```java
public TreeNode bstFromPreorder(int[] preorder) {
        if (preorder.length == 0) return null;
        TreeNode root = new TreeNode(preorder[0]);
        Deque<TreeNode> s = new ArrayDeque<>();
        s.push(root);

        TreeNode parent;
        for (int i = 1; i < preorder.length; i++) {
            parent = s.peek();
            while(!s.empty() && parent.val < preorder[i]) parent = s.pop();

            TreeNode child = new TreeNode(preorder[i]);
            if (parent.val < child.val) parent.right = child;
            else parent.left = child;
            s.push(parent.right);
        }
    }
```

## Q146 LRU Cache


Change `Node` from the inner class to outer class, the runtime change from 29ms to 13 ms.

## Q152 Maximum Product Subarray

The key idea for this problem is that if there is no zero, the maximum product either start with the first element or the last element or both. That is to say, the result should never be a inner subrray of the original one.

### Proof

Suppose there is such a subarray, if its product is negative, if its left side or right side is negative, it can always expend one more element to get a positive result. If both the left and right are positive, it can just disregard this subarray, to pick the bigger positive number.

If the subarray is positive. If its left or right is positive, it can always expand one more element to get a larger product. If both left and right are negative, it can expand in two side to get a larger product.

Therefore, in whatever case, it can always expand to the start or the end. 

However, what if there are zeros. The answer is to split the array, every time we have a zero, we split at this point and start from the next number. The reason is the result will never span across arrays split by 0. (If we have a zero, we still regard it as a candidate for the final result)

### Implementation

```java
public int maxProduct(int[] nums) {
    if (nums.length == 0) return 0;
    int re = nums[0];
    int l = 0;
    int r = 0;
    for (int i = 0; i < nums.length; i++) {
        // prefix array
        l = (l ? l : 1) * nums[i];
        // subffix array
        r = (r ? r : 1) * nums[nums.length - 1 - i];
        // We will still consider 0
        re = Math.max(re, Math.max(l ,r));
    }
    return re;
}
```

## Q206 Reverse Single LinkedList

Iterative version is obvious, but the idea behind recursive solution is interesting.

### Normal Recursion

```java
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode temp = reverseList(head.next);
    head.next.next = head;
    head.next = null;
    return temp;
}
```

The basic idea for this implementation is the reverse of current list is to put the head after the reverse of the list after the head. However, the tricky part is how can you get the tail of the reverse of list after head. We can know that the tail is just the node after head, and its reference is still kept by head. So, we can just leverage it to finish the task.

### Tail Recursion

```java
public ListNode reverseList(ListNode head) {
    return reverseList(head, null);
}

public ListNode help(ListNode head, ListNode re) {
    if (head == null) return re;
    ListNode temp = head.next;
    head.next = re;
    return help(temp, head);
}
```

## Q295 Find Median from Data Stream

The key of this problem is to main two heaps.

## Q300 Longest Increasing Subsequence

Patience sort

## Q348 Design Tic-Tac-Toe

## Q50 Fast Power Algorithm

1. Binary Decomposition
   
   Any integer can be represented in binary, e.g: \
$10 = 1010_{2}$, $15 = 1111_{2}$ \
To calculate `power(a, x)`, we can also convert the `x` into binary, and it can be decomposed as: $x = \sum b_{i} \cdot 2^{i}$. Hence, $a^{x} = \prod a^{b_{i} \cdot 2^{i}}$. Take $3^{10}$ as an example: \
$3^{10} = 3^{1010_{2}} = 3^{0 \cdot 2^{0}} \cdot 3^{1 \cdot 2^{1}} \cdot 3^{0 \cdot 2^{2}} \cdot 3^{1 \cdot 2^{3}}$ \
And we have $a^{2^{i + 1}} = a^{2^{i}} \cdot a^{2^{i}}$. So we can keep calculate $a^{2^{i}}$, and include the result if $b_{i} = 1$.

    ```java
    public double power(double x, int n) {

        // convert n to long cause - Integer.MIN_VALUE will overflow.
        long k = n;
        if (k < 0) {
            k = -k;
            x = 1.0 / x;
        }
        double ans = 1;
        // Initially curr = x ^(2 ^ 0)
        double curr = x;
        // here we are actually perform binary decomposition to k
        while (k > 0) {
            if (k % 2 == 1) {
                ans *= curr;
            }
            curr *= curr;
            //right shift k 1 bit
            k /= 2;
        }
        return ans;
    }
    ```
2. Power with Modular
   We have a theory for this problem:\
   $(a \cdot b) \mod c = (a \mod c \cdot b \mod c) \mod c$
    ```java
    public int powerWithMod(int x, int n, int m) {
        // here we can not handle n < 0
        int ans = 1;
        int cur = n;
        while (n > 0) {
            if (n % 2 == 1) {
                ans = (int)((long)cur * ans % m);
            }
            cur = (int)((long)cur * cur % m);
            n /= 2;
        }
        return ans;
    }
    ```

## Q134 Gas Station



