# Binary Search

Binary search is not just finding out the target in a sorted list(with random access), the core idea behind this algorithm is to utilize the order to halve the search space. Hence, the conditions for shrinking the search space is not limited to compare the target with the number at the middle, there are actually a lot of generalizations.

## Variant of Standard BST

Ceil and floor are two most important extension of binary search. Ceil means find the smallest number that is larger or equal than target. Floor is to find the largest number that is smaller or equal than target. 

### Ceil
```java
public int ceil(int[] arr, int target) {
    int lo = 0;
    int hi = arr.length - 1;
    while (lo < hi) {
        int p = lo + (hi - lo) / 2;
        if (arr[p] < target) lo = p + 1;
        else hi = p; 
    }
    return arr[lo] < target ? arr.length : lo;
}
```

### Floor
```java
public int floor(int[] arr, int target) {
    int lo = 0;
    int hi = arr.length - 1;
    while (lo < hi) {
        int p = hi - (hi - lo) / 2;
        if (arr[p] > target) right = p - 1;
        else left = p; 
    }
    return arr[hi] > target ? -1 : hi;
}
```

The reason why we choose the pivot in different way is to break the tie according to the condition. Image when you have only two element, choose a wrong pivot will get yourself stuck in the loop.

## Q33 Search in Rotated Sorted Array
When rotated on the index 0, the array does not change.

### Sol 1, find the pivot and applied virtual index
The main idea is to find the pivot by binary search
```java
public int search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int p = lo + (hi - lo) / 2;
        if (nums[p] > nums[hi]) lo = p + 1;
        else hi = p;
    }
    int pivot = lo;
    lo = 0, hi = nums.length - 1;
    // here we do the bs on a virtual index, but convert it to real when access the physical array.
    while (lo < hi) {
        int p = lo + (hi - lo) / 2;
        int real = (p + pivot) % nums.length;
        if (nums[real] < target) lo = p + 1;
        else hi = p;
    }
    int idx = (lo + pivot) % nums.length;
    return nums[idx] == target ? idx : -1;
}
```

Note: when applied the virtual index, the logical index should be virtual, and we have a converter that convert the virtual index to the real index when manipulate on the underlying array.

### One-pass Binary Search

Still binary search, when halve the array, the pivot can eith be larger or equal than the first element, or smaller than it, corresponding to two cases where the rotated array (may rotated at the first element, i.e. a normal array) is at the right/left, then two array are not rotated). For both cases, we can check whether the target is in the normal array, then we can narrow the search space by half.
```java
public int search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int p = lo + (hi - lo) / 2;
        if (nums[p] == target) return p;
        if (nums[p] >= nums[lo]) {
            if (nums[p] > target && target >= nums[lo]) hi = p - 1; // equals is import!
            else lo = p + 1;
        } else {
            if (nums[p] < target && target <= nums[hi]) lo = p + 1; // equals is import!
            else hi = p - 1;
        }
    }
    return nums[lo] == target ? lo : - 1;
}
```

## Q162 Find Peak Element

## Q436 Find Right Interval

## Q287 Find the Duplicate Number
