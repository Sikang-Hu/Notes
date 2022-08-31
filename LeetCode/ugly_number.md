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