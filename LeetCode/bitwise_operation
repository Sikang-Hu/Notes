# Bitwise Operations

## Q476 Number Complement

For a bit x:

* x xor 0 = x
* x xor 1 = 1 - x

The common strategy will be construct a bitmask, we can use the built in function:

```java
public int findComplement(int num) {
    return (Integer.highestOneBit(num) << 1) - num - 1;
}
```

The built-in function will return the highest one bit of num, and we shift it one more bit and - 1 to get the bitmast. Remember, bitwise operator has low priority, so always wrap them with parentheses.

```java
public int findComplement(int num) {
    int bitmask = num;
    bitmask |= num >> 1;
    bitmask |= num >> 2;
    bitmask |= num >> 4;
    bitmask |= num >> 8;
    bitmast |= num >> 16;
    return num ^ bitmask;
}
```