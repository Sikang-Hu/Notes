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
## Articulation Points

In undirected graph, articulation points are the vertice if removing it disconncets the graph. The articulation points demonstrates the vulnerabilities in a connected network. Suppose there is a vertex `V` which can be reached by `U`, and also can be reached by `U`'s ancestor `A`. For `U` to be a articulation point, there should be two conditions hold:
1. If all paths from A to V require U to be in the graph
2. If U is the root of the DFS traversal with at least two children subgraphs dis connected from each other.

```java
class Solution {
    private int tt = 1;
    private boolean[] ap;
    public Set<Integer> articulationPoint(int n, List<List<Integer>> connections) {
        List<List<Integer>> g = new ArrayList<>();
        for (int i = 0; i < n; i++) g.add(new ArrayList<>());
        for (List<Integer> e : connections) {
            g.get(e.get(0)).add(e.get(1));
            g.get(e.get(1)).add(e.get(0));
        }
        int[] disc = new int[n];
        int[] low = new int[n];
        ap = new boolean[n];
        for (int i = 0; i < n; i++) {
            if (disc[i] == 0) 
                ap[i] = dfs(g, 0, 0, disc, low) > 1; // check condition 2 for the root.
        }
        Set<Integer> re = new HashSet<>();
        for (int i = 0; i < n; i++) {
            if (ap[i]) re.add(i);
        }
        return re;
    }

    private int dfs(List<List<Integer>> g, int node, int prev, int[] disc, int[] low) {
        if (disc[node] != 0) return 0;
        disc[node] = tt++;
        low[node] = disc[node];
        int children = 0;
        for (int next : g.get(node)) {
            if (disc[next] == 0) {
                children++;
                dfs(g, next, node, disc, low);
                if (low[next] >= disc[node]) 
                    ap[node] = true; // equals means the root of the circle, which is also ap, this may count the root, while it will be check when the dfs finished by condition 2.
                low[node] = Math.min(low[node], low[next]);
            } else if (next != prev) {
                // for ap, we can only use disc
                low[node] = Math.min(low[node], disc[next]); 
            }
        }
        return children;
    }
}
```

There are several points to note:
* When dfs on a neighbor finished, check the lowest timestamp it has seen with the discover time of the current node using `low[next] >= disc[node]`. If equal holds, node is the root of this circle it should be a articulation node if it is not root. So at the end, we will use condition 2 to check whether the root is ap.
* When reached at a visited node(ancestor), we use `low[node] = Math.min(low[node], disc[next])` to update the lowest timestamp instead of using `low[node] = Math.min(low[node], low[next])`. The intuition behind is to avoid cases where the route to the ancestor require a node on the route to the current node.

### Bridge
```java
class Solution {
    private int t = 1;
    public List<List<Integer>> criticalConnections(int n, List<List<Integer>> connections) {
        List<List<Integer>> g = new ArrayList<>();
        for (int i = 0; i < n; i++) g.add(new ArrayList<>());
        for (List<Integer> e : connections) {
            g.get(e.get(0)).add(e.get(1));
            g.get(e.get(1)).add(e.get(0));
        }
        List<List<Integer>> re = new ArrayList<>();
        int[] timeStamp = new int[n];
        dfs(g, re, 0, -1, timeStamp); // can use for loop if the graph is not connected
        return re;
    }

    private int dfs(List<List<Integer>> g, List<List<Integer>> re, int node, int prev, int[] time) {
        if (time[node] != 0) return time[node];
        time[node] = t++;
        int min = Integer.MAX_VALUE;
        for (int next : g.get(node)) {
            if (time[next] == 0) {
                int l = dfs(g, re, next, node, time);
                if (l > time[node])
                    re.add(List.of(node, next));
                min = Math.min(l, min);
            } else if (next != prev) {
                // this is a previous visited node, use its discover time as a candidate for the earliest 
                // node. you can also use the low value if you have it.
                min = Math.min(min, time[next]); 
            }
        }
        return Math.min(min, time[node]);
    }
}
```

### Biconnected Graph

## Eulerian Path

> An **Eulerian Path** in a graph G is a path that passes through every edge of G exactly once.
> An **Eulerian cycle** is an Eulerian path that starts and ends at the same vertex.

### Existance of Eulerian Tour

|                   | Eulerian Circuit | Eulerian Path |
|-------------------|------------------|---------------|
| Undirected Graph  | Every vertex has <br> an even degree |Either every vertex has even degree or <br >exactly two vertices have odd degree|
| Directed Graph    | Every vertex has equal indegree and outdegree | At most one vertext has (outdegree) - (indegree) = 1 and at most one vertex has (indegree) - (outdegree) = 1 and all other vertices have equal in and out degrees.|

Also, all the nodes with non-zero degree should be in the same connected component.

### Find the Eulerian Path: Hierholzer's Algorithm

First of all, we have if a graph has a eulerian circuit, the circuit is also a eulerian path, which can also be found by the algorithm for Eulerian path. The complexity of this algorithm is $O(E)$.

The main idea of Hierholzer is:
1. First check whether there is an Eulerian path by degree
2. find the start node
3. Begin from the start node to perform dfs: for each unused outgoing edge enter the destination node, after exhausted all outgoing edge, add current node to the beginning of the path
4. Finally, check whether the length of the path equals $|E| + 1$. This can prevent the case where there are multiple connected components.

```java
public List<String> findEulerianPath(List<List<String>> edges) {
    // construct the graph and calculate the degree
    Map<String, List<String>> graph = new HashMap<>();
    Map<String, Integer> indegree = new HashMap<>();
    for (List<String> edge : edges) {
        graph.putIfAbsent(edge.get(0), new ArrayList<>());
        graph.get(edge.get(0)).add(edge.get(1));
        indegree.put(edge.get(1)
            , indegree.getOrDefault(edge.get(1), 0) + 1);
    }

    // Check whether there is a Eulerian path, and find the start node
    String start = "";
    String end = "";
    String temp = "";
    for (String node : graph.keySet()) {
        // in - out
        int diff = indegree.get(node) - graph.get(node).size();
        if (Math.abs(diff) > 1) return null; // No Eulerian path
        else if (diff = -1) {
            if (start.equals("")) start = node;
            else return null;
        }
        else if (diff = 1) {
            if (end.equals("")) end = node
            else return null;
        } else if (indegree.get(node) > 0) {
            // Prevent starting from a singleton node
            temp = node;
        }
    }
    List<String> re = new ArrayList<>();
    if (temp.equals("")) return re; // Nodes are all separated, no Eulerian path
    if (start.equals("")) start = temp; // There is a Eulerian circuit
    // DFS from start then
    dfs(start, graph, re);
    if (re.size() == edges.size() + 1) return re;
    else return null; // Multiple Connected Components.
}

private void dfs(String node, Map<String, List<String>> graph, List<String> res) {
    List<String> edges = graph.get(node);
    while (edges.size() > 0) {
        String next = edges.remove(edges.size() - 1);
        dfs(next, graph, res);
    }
    res.add(0, node);
}
```

