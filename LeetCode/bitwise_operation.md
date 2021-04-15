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

The built-in function will return the highest one bit of num, and we shift it one more bit and - 1 to get the bitmask. Remember, bitwise operator has low priority, so always wrap them with parentheses.

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

## Q191 Number of 1 Bits

* Get the last bit of a by `a & 1`. 
* `n&(n - 1)` to filp the least-significant 1-bit in `n` to 0
* Distinguish the differences between `>>`(signed) and `>>>`(unsigned). When use `>>>`, the number is treated as an unsigned int and a zero will always be shifted to the leftmost position. In constrast, `>>` treats the int as signed int, the leftmost position after `>>` depends on sign extension: `1` for negative, `0` for position. E.g. right shift Integer.MIN_VALUE(1000.....000) to -1 (11111...1111).
* Output an int as binary string: `Integer.toBinaryString()`, parse an binary String to integer: `Integer.parseInt(1001, 2)`;

```java
public int hammingWeight(int n) {
    int re = 0;
    while (n != 0) {
        re += (n & 1);
        n >>> 1;
    }
    return re;
}
```

## Q371 Sum of Two Integers

How to bit operation to perform addition:

* XOR give the sum of two integer with out carry `01 ^ 11 = 10`
* The carry can be represented as `(x & y) << 1`, since only both `x` and `y` are 1 there is a carry at left bit: `(01 & 10) << 1 = 10`
* XOR can also give the difference between two int without borrow `01 ^ 10 = 10`
* The borrow can be represented as `((~x) & y) << 1)`, since only `x = 0` and `y = 1` results to a borrow at left bit.

### Main Idea

In this problem, `a` or `b` can be either positive or negative and either side can have a larger absolute value. Hence, we can first reduce these possibility into two problems for two positive integer where `x > y`:
  1. `x + y`
  2. `x - y`
Then we can calculate based on 4 points above.

### Implementation

```java
public int getSum(int a, int b) {
    int x = Math.abs(a);
    int y = Math.abs(b);
    if (a < b) return getSum(b, a);
    int sign = a > 0 ? 1 : -1;

    if (a * b >=0 ) {
        while (y != 0) {
            int sum = x ^ y;
            int carry = (x & y) << 1;
            x = sum;
            y = carry;
        }
    } else {
        while (y != 0) {
            int diff = x ^ y;
            int borrow = ((~x) ^ y) << 1
            x = diff;
            y = borrow;
        }
    }
    return sign * x;
}
```

### Java Specific Impl

Java represent a negative number by strategy called "two's complement":
`(-x + x) & (0xFFFFFFFF) = 0`
How does Java compute "2's complement" and manage 32-bits limit?:
1. After each operation we have an invisible `& mask`, where `mask = 0xFFFFFFFF`
2. The overflow, i.e. the situation of `x > 0x7FFFFFFF`, is managed as `x --> ~(x ^ 0xFFFFFFFF)` 

```java
public int getSum(int a, int b) {
    while (b != 0) {
        int sum = a ^ b;
        int carry = (a & b) << 1;
        a = sum;
        b = carry;
    }
    return a;
}
```
