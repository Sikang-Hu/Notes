# Graph

## Strongly Connected Component

In directed Graph, the connectivity can be defined as

> Two nodes `u` and `v` of a directed graph are connected if there is a path from `u` to `v` and a path from `v` to `u`.

This relation partitions `V` into disjoint set that we called `Strongly Connected Components`.

Shrink each strongly connected component down to a single meta-node, and draw an edge from one to another if there is an edge between their components. The resulting `meta-graph` must be a DAG, otherwise it could be shrink to a larger single meta-node.

### Kosaraju-Sharir Algorithm

#### Properties: 

1. For node `u`, dfs(`u`) terminate precisely when all nodes reachable from `u` have been visited. 
   This implies that if we dfs a node in a sink SCC, it will terminate after explore all nodes in that SCC. But, how can we find that node in sink.

2. The Node with highest post number in dfs (the last one to terminate) must lie in souce SCC. One more step further, if `C` and `C'` are both SCC and there is an edge `C -> C'`, then the highest post number in `C` must be bigger than highest post number in `C'`.
   This helps us find a node in source SCC, but we need one in sink SCC. Consider the reverse graph, it has the same SCC, but with exactly reversed topological order of SCC. Hence, the node in source SCC in reversed graph is exactly a node in sink SCC in original graph.

#### Strategy

1. Run dfs on reversed graph, sort the nodes by descending post number
2. Run dfs on original graph according to the order in step 1.

#### Implementation in Java

```java
public class SCC {
    private boolean marked[];
    private int[] id;
    private int count;


    public void findSCC(List<List<Integer>> graph) {
        List<List<Integer>> rev = reverse(graph);
        Deque<Integer> stack = new ArrayDeque<>();
        marked = new boolean[graph.size()];
        for (int i = 0; i < graph.size(); i++) {
            if (!marked[i]) {
                dfs1(i, rev, postorder);
            }
        }
        int curr = 0;
        marked = new boolean[graph.size()];
        while (!postorder.isEmpty()) {
            curr = postorder.removeLast(0);
            if (!marked[curr]) {
                dfs2(int i, List<List<Integer>> graph);
                count++;
            }
        }
    }

    private void dfs1(int node, List<List<Integer>> rev, Deque<Integer> postorder) {
        marked[node] = true;
        for (int i : rev.get(node)) {
            if (!marked[i]) {
                dfs(i, rev, postorder);
            }
        }
        postorder.add(node);
    }

    private void dfs2(int node; List<List<Integer>> graph) {
        marked[node] = true;
        id[node] = count;
        for (int i ： graph.get(node)) {
            if (!marked[i]) {
                dfs2(i, graph);
            }
        }
    }

    private List<List<Integer>> reverse(List<List<Integer>> graph) {
        List<List<Integer>> result = new ArrayList<>();
        for (int i = 0; i < graph.size(); i++) {
            result.add(new ArrayList<>());
        }
        for (int i = 0; i < graph.size(); i++) {
            for (int j : graph.get(i)) {
                result.get(j).add(i);
            }
        }
        return result;
    }
}
```

### Articulation Points

In undirected graph, articulation points are 

### Bridge

### Biconnected Graph