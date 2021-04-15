# Binary Search

Binary search is not just finding out the target in a sorted list(with random access), the core idea behind this algorithm is to utilize the order to halve the search space. Hence, the conditions for shrinking the search space is not limited to compare the target with the number at the middle, there are actually a lot of genralization.

## Variant of Standard BST

Ceil and floor are two most important extension of binary search. Ceil means find the smallest number that is larger or equal than target. Floor is to find the largest number that is smaller or equal than target. 

### Ceil
```java
public int ceil(int[] arr, int target) {
    int lo = 0;
    int hi = arr.length - 1;
    while (lo < hi) {
        int p = left + (right - left) / 2;
        if (arr[p] < target) left = p + 1;
        else right = p; 
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
        int p = right - (right - left) / 2;
        if (arr[p] > target) right = p - 1;
        else left = p; 
    }
    return arr[hi] > target ? -1 : hi;
}
```

## Q162 Find Peak Element

## Q436 Find Right Interval

## Q287 Find the Duplicate Number
