# Math Problem

## Q149 Max Point on a Line

### Math Knowledge
There are several points we know learned from this question:

1. How to represent a line:
   * Slope and Cut
    $$
    y = k\cdot x + b
    $$
   * Two points
    $$ 
    \dfrac{x - x_{1}}{x_{1} - x_{2}} - \dfrac{y - y_{1}}{y_{1} - y_{2}} = 0
    $$
In the program, if we want to store a line, we need its slope and cut, but storing slope as double is not feasiable for the sake of how the float is represented in the computer. Since the slope are always rational, we can use **a pair of co-prime int** to store it as a fraction to represent unique slope.
2. Calculate Greatest Common Divisor(Euclid's Algorithm)
   * Proof: Suppose we have two integer $A >= B$, let `X` be their GCD, which can be written as:
        $$ 
        A = aX
        $$
        $$
        B = bX
        $$
        Then for $R = A \mod B$, we have
        $$
        R = aX - k\cdot bX = (a - k \cdot b)X \Rightarrow R | X
        $$
        Hence, `X` is GCD of `A`, `B`, `R`, then we have
        $$
        GCD(A, B) = GCD(B, A \mod B)
        $$
* Implementation
   ```java
   public int gcd(int a, int b) {
       // The gcd of a and 0 will be a
       // This gcd implementation also applies on negative integer, cause we need reminder here, not modulo
       if (b == 0) return a;
       return gcd(b, a % b);
   }
   ```

### Main Idea
For this problem, we can find the line with maximum point passing `i`. And for each point, `i`, we don't check whether points before it. For example `i - 2`, since the line passing these two point has been consider when we look at `i - 2`. In this way, we can only compare the slope, since the line will always pass `i`. Also, we need to take care of the duplicate node and case where there is no slope. The complexity will be $O(n^{2})$

### Implementation
```java
public int maxPoints(int[][] points) {
    if (points == null) return 0;
    if (points.length < 3) return points.length;
    
    Map<Pair<Integer, Integer>, Integer> map = new HashMap<>();
    int re = 0;
    for (int i = 0; i < points.length; i++) {
        map.clear();
        int x1 = points[i][0];
        int y1 = points[i][1];
        int duplicate = 1;
        int maxPoints = 0;
        for (int j = i + 1; j < points.length; j++) {
            int x2 = points[j][0];
            int y2 = points[j][1];
            if (x1 == x2 && y1 == y2) {
                duplicate++;
                continue;
            }
            int dx = x1 - x2;
            int dy = y1 - y2;
            int gcd = gcd(dx, dy);
            Pair<Integer, Integer> slope = new Pair<>(dx / gcd, dy / gcd);
            if (map.containsKey(slope)) {
                map.put(slope, map.get(slope) + 1);
            } else {
                map.put(slope, 1);
            }
        }
        for (Integer p : map.values()) {
            maxPoints = Math.max(maxPoints, p);
        }
        re = Math.max(re, duplicate + maxPoints);
    }
    return re;
}

private int gcd(int x, int y) {
    if (y == 0) return x;
    else return gcd(y, x % y);
}
```

## Q166 Fraction to Recurring Decimal

First we need to know that the result is a rational number, which means there must be a repeat pattern if it is not an integer. Then, we can just follow how we perform dividing by hand.

### Key Trick

1. How to check whether the result is 