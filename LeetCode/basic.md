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

Here is a template in Java:

```java
class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> res = new ArrayList<>();
        dfs(res,new ArrayList<Integer>(),candidates,target,0);
        return res;
    }
    private void dfs(List<List<Integer>> res, List<Integer> cur, int [] candidates, int target, int index){
        if(target == 0){
            res.add(new ArrayList<>(cur));
        }
        for(int i = index; i < candidates.length; i++){
            if(target >= candidates[i]) {
            cur.add(candidates[i]);
            dfs(res, cur, candidates, target - candidates[i], i);
            cur.remove(cur.size() - 1);
            }
        }
    }
}
```