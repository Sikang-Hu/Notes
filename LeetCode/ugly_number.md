# Q263 Ugly Number
An ugly number is a **positive integer** whose prime factors

Be careful about 0, which is not an ugly number

# Q264 Ugly Number II

```java
public int nthUglyNumber(int n) {
    int[] ugly = new int[n];
    int p2 = 0, p3 = 0, p5 = 0;
    ugly[0] = 1;
    int p = 1;
    while (p < n) {
        int prod2 = 2 * ugly[p2];
        int prod3 = 3 * ugly[p3];
        int prod5 = 5 * ugly[p5];
        int min = Math.min(prod2, Math.min(prod3, prod5));
        ugly[p++] = min;
        if (min == prod2) p2++;
        if (min == prod3) p3++;
        if (min == prod5) p5++;
    }
    return ugly[n - 1];
}
```

## Q313 Super Ugly Number

The complexity of the heap solution is not `O(nlogk)`, it should be `O(knlog(k))`, the easy solution is just `O(kn)`, so just go with the easier one.

## Q1201 Ugly Number III

Q: return the nth number divisible by integer a, b, c

Similar to previous question, we can applied the idea of merge sorted list, but its complexity will be O(n). While for this problem, we can have such problem, we can find such a function `f` where `f(k)` is the number of ugly numbers small or equals than `k`. And we know that `f(n)` should be monolithically increasing, and the smallest `k` such that `f(k) = n` is the nth ugly number.

If we can compute `f` in constant time, we can then binary search `k` in O(logn)

### How to compute `f` in constant time
We have this two key points:
* The number of integer divisible by `a` smaller or equal to `k` can be calculated by `k / a`
* Imaging there are three set A(number divisible by a), B(number divisible by b) and C(number divisible by c). The number of ugly number can be represent as `|A| + |B| + |C| - |A ^ B| - |B ^ C| - |A ^ C| + |A ^ B ^ C|`

To compute the `|A ^ B|`, i.e. the number of integers divisible by both a and b(not a * b, counter e.g. a = 4, b = 6, 12 is a valid number, should by least common multiple)

To compute least common multiple, we have formula: `lcm(a, b) = a * b / gcd(a, b)`

Then the code should be 
```java
public int nthUglyNumber(int n, int a, int b, int c) {
        long l = 1, long r = Long.MAX_VALUE;
        while (l < r) {
            long p = l + (r - l) / 2;
            if (f(p, a, b, c) < n) {
                l = p + 1;
            } else {
                r = p;
            }
        }
        return l;
}

private long f(long k, int a, int b, int c) {
    return k / a + k / b + k / c + k / lcw(a, b) + k / lcw(b, c) + k / lcw(a, c) + k / lcw(lcw(a, b), c);
}

private long lcw(long a, long b) {
    return a * b / gcd(a, b);
}

private long gcd(long a, long b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}

```