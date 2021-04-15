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

In undirected graph, articulation points are 

### Bridge

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

