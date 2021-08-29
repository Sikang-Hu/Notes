# Binary Index Tree

A fenwick tree or binary indexed tree is a data structure that can efficiently update elements and calculate prefix sums in a table of numbers.

update(): Updates BI Tree for operation `arr[index] += val`
getSum(): Returns sum of `arr[0..index]`

## Implementation
```java
class BIT {
    int[] tree;
    public BIT(int[] nums) {
        tree = new int[nums.length + 1]; // 0 is a dummy node
        for (int i = 1; i < tree.length; i++) {
            int j = i + (i & -i);
            tree[i] += nums[i - 1];
            if (j < nums.length) tree[j] += tree[i];
        }
    }

    public void update(int x, int delta) {
        for (x++; x < tree.length; x += (x & -x)) tree[x] += delta;
    }

    public int sum(int x) {
        int sum = 0;
        for (x++; x > 0; x -= (x & -x)) sum += tree[x];
        return sum;
    }
}
```