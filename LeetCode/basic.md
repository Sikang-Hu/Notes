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

