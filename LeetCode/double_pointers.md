# Double Pointers

## Q287 Find the Duplicate Number

For this problem, we have two interesting solutions, both of which are related to double pointers. 

### Solution 1: Binary Search

First we have Lemma for this problem

> Given array of size n + 1, which contains only number from i to i + n - 1 exclusively, there must be at least one duplicate number. (Pigeonhole Principle)

Then this problem can be reduced to narrow the search space `[i, i + n - 1]`.

We begin with interval `[1, n]`, where we have `n + 1` number. And then we pick the `mid = (1 + n) / 2` and count how many number is less or equal than `mid`, if `count` is larger than `mid`, meaning the duplicate must fall in `[1, mid]`, in that way, we narrow down the interval to half. Then we just repeat until the size of the interval become 1, that number must be the result.

The complexity will be `O(nlogn)`.

```java
public int findDuplicate(int[] nums) {
    int lo = 1;
    int hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int count = 0;
        for (int i : nums) {
            if (i >= lo && i <= mid) {
                count++;
            }
        }
        if (count > mid - lo + 1) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}
```

### Solution 2: Floyd's Tortoise and Hare(Fast and Slow Pointers)

From the question we know that, all the value in the array is from 1 to n meaning **the value under each index could still be an index**, then we can exploit in two way:
1. Use the array as index map, `arr[arr[i]]`. For example, if this map is not read-only, we can iterate through the array and negate `arr[arr[i]]` if it is positive. If we found a negative number, meaning we have already seen it, it is duplicate. However, above approach has a lot of limitation: 
   1. It cannot handle both negative and positive, but this is not vital, we can simply find the smallest non-positive number and add `offset` to it to make it 1. Then we add the `offset` to every other numbers.
   2. The vitalest part: we must modify the array, which is forbbiden in this problem.
2. The value under each index can be regarded as a pointer to another slot, then the array can be reconstructed into a single linked list. Then the problem is reduced to finding the entrance of cycle in a single linked list. To solve this problem we applied Floyd;s Tortoise and Hare Algorithm, basically we will have two pointers, a fast one at speed of 2 (hare) and a slow one at speed of 1(tortoise). And there are two phase for this algorithm:
   1. Start the race, for hare `fast = nums[nums[fast]]`, and for tortoise `slow = nums[slow]` until they meet. In the problem of linked list, this phase can decide whether there is a cycle.
   2. Move the tortoise to the start point, and slow down the hare, let them run at the same speed, then there will meet at the entrance. Alternative: or we can calculate the length of the cycle by continue the race and stop when they meet again, and then move both of them to the start point and let hare first run for length of the cycle, and then they both run at the speed of 1. Then then will meet at the entrance.(This implementation will be slower)

#### Correctness

We only illustrate the correctness of phase two here, i.e. why the meeting point is the the entrance: 

From the phase 1, we have 

$$d(hare) = 2 \cdot d(tortoise)$$

Also, 
$$d(tortoise) = F + a$$
Let `C` be the length of the cycle, the 

$$d(hare) = F + a + nC$$

Combine them together:

$$2(F + a) = F + a + nC => F + a = nC$$

```java
public int findDuplicate(int[] nums) {
    int slow = 0;
    int fast = 0;
    while (true) {
        fast = nums[nums[fast]];
        slow = nums[slow];
        if (fast == slow) break;
    }
    slow = 0;
    while(slow != fast) {
        slow = nums[slow];
        fast = nums[fast];
    }
    return slow;
}
```

## Q42 Trapping Rain Water

The main is to fill each bin individually. For each bin, the water it can trapped is bounded by the smaller max height of its left and right. So, if there is a larger bar at one end(say right), all the water trapped can be decided by the max height of the bar at the other side(left). So, once we found the bar at one end is larger, we can iterate from the other end, and the water current position can trap will be decided by the max at the other end.


```java
public int trap(int[] height) {
    int n = height.length;
    int lmax = 0, rmax = 0;
    int l = 0, r = n - 1;
    int ret = 0;
    while (l < r) {
        if (height[l] < height[r]) { // this implies height[r] is no smaller than lmax
            if (height[l] < lmax) ret += lmax - height[l];
            else lmax = height[l];
            l++;
        } else {
            if (height[r] < rmax) ret += rmax - height[r];
            else rmax = height[r];
            r--;
        }
    }
    return ret;
}
```