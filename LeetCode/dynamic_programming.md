# Dynamic Programming

## Longgest Common Substring

## Q312 Burst Ballon

## Q689 Maximum Sum of 3 Non-Overlapping Subarrays

## Q42 Trapping Rain Water

## Q239 Sliding Window Maximum

## Q152 Maximum Product Subarray

### Main Idea
Similar to maximum sum subarray, we can see a sub-optimal feature if we define the subproblem as maximum subarray ended at `i`. However, unlike the sum problem, negative number can flip the sign making a small negative number a large positive number. So we maintain two number max/min subarray ended at previous element. At `i`, the answer must come from `max * i` or `min * i`.

### Implementation

```java
public int maxProduct(int[] nums) {
    // Cope with the empty array, so we can pick the head as initial values.
    if (nums == null || nums.length == 0) return 0;
    int max = nums[0], min = nums[0], re = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int a = max * nums[i];
        int b = min * nums[i];
        max = Math.max(nums[i], Math.max(a, b));
        min = Math.min(nums[i], Math.min(a, b));
        re = Math.max(re, max);
    }
    return re;
}
```

### Another cool solution
Compute the prefix prod and suffix subarray prod, restart at each zero, and pick the maximum as result. First of all, if there is any zero, it can divide the array into several subarrays. If there is no zero, the answer must either start from the head or end at the end.

```java
public int maxProduct(int[] nums) {
    // Cope with the empty array, so we can pick the head as initial values.
    if (nums == null || nums.length == 0) return 0;
    int l = 0, r = 0, re = nums[0];
    for (int i = 0; i < nums.length; i++) {
        l = (l == 0 ? 1 : l) * nums[i];
        r = (r == 0 ? 1 : r) * nums[nums.length - 1 - i];
        re = Math.max(re, Math.max(l ,r));
    }
    return re;
}
```

### Retrospect 
This problem has some caveats, so I failed to be accepted for many times every time I tried on this problem. I first tried to maintained two records, max positive subarray so far, minimum negative subarray so far, which is really awkward, for two simple reason: 
1. How to pick the initial value for these two variables.
2. How to update them, and if there is a zero, what should we do.

After failed following cases:
* \[0,2\] How to update
* \[-1\] About the initial value and update, I pick 0 for nega, so Math.max(-1, nega * -1) = 0, led to a wrong answer.
* \[7,-2,-4\] How to update the two variables to take the flipping into consideration


## Q1494 Parallel Courses II
2^n, n < 15 or 20
### State compression Dynamic Programming
```java
int A,B; long C;
int c;
A |= 1 << c; // insert c (c = 0 ~ 31);
A &= ~(1 << c) // erase c (c = 0 ~ 31); ~(1 << c) to obtain a set exclude c, and then & with A to remove c.
A^= 1<< c // erase c if (A >> c & 1 == 1) A contains c
a & (-a) // lowbit of A
A = 0 // empty set
A | B // union
A & B // intersection
int si = 15; // size of set
int ALL = (1 << si) - 1;
ALL ^ A // complementary set of A
(A & B) == B // B is A's subset

// enumerate the subset of ALL
for (int i = 0; i <= ALL; i++) ;

// enumerate a set A 
for (int i = A; i != A; i = (i - 1) & A) ;

// lowbit
-a : ~a + 1
01100100 -> 10011011 -> 10011100
a&(-a) = 100

//cnt
private int count(x) {
    int cnt = 0;
    for (int i = 0; i < si; i++)
        if (x&(1<<i)) cnt++;
    return cnt;
    // or
    for (int i = x;i; i >>= 1)
        cnt += i & 1;
}


// cnt[i]
int[] cnt = new int[ALL];
for (int i = 1; i < ALL - 1; i++) {
    cnt[i] = cnt[i >> 1] + (cnt & 1);
}

// high bit
private int highbit(int x) {
    int p = lowBit(x);
    while (p != x) {
        x -= p;
        p = lowBit(x);
    }
    return p;
}

private int isPowerOf2(int x) {
    return x && x & (x - 1);
}
```

