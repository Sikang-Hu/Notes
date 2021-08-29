# Matrix Problem

A note for 2D or higher dimonsion array problem

## Q73 Set Matrix Zeros

The key idea is to decide which rows and cols should be set to zero. So, we can simply have two arrays to record that. If `matrix[i][j] == 0`, we just set both `row[i]`, `col[j]` to true, meaning we are going to set all element at ith row and jth col to zero later.

However, the trick comes when it required a constant space. How can we leverage the space of the given matrix to simulating the two arrays we have? 

We can use the first row and col to do that:

 >If `matrix[i][j] == 0`, set `matrix[i][0]`(use the first col to mimic `row`), `matrix[0][j]`(first row to mimic `col`) to 0. However, `matrix[0][0]` will be shared by the first row and the first col. We can assign it to `row`, and have another boolean to `col`.

We need to be careful about the condition to set those flag:
```java
if (matrix[i][j] == 0) {
    // handle the first col and other cols separately
    if (j == 0) isCol = true;
    else {
        matrix[0][j] = 0;
    }
    matrix[i][0] = 0;
}
```

After setting all the flag, we iterate the matrix, and set elements to 0 accrodingly.

```java
public void setZero(int[][] matrix) {
    if (matrix == null || matrix.length == 0 || matrix[0].length == 0) return;

    boolean isCol = false;
    // Set flag
    for (int i = 0; i < matrix.length; i++) {
        for (int j = 0; j < matrix[0].length; j++) {
            if (matrix[i][j] == 0) {
                if (j == 0) isCol = true;
                else {
                    matrix[0][j] = 0;
                }
                matrix[i][0] = 0;
            }
        }
    }

    // Set zero for elements not in the first row or the first col
    for (int i = 1; i < matrix.length; i++) {
        for (int j = 1; j < matrix[0].length; j++) {
            if (matrix[i][0] == 0 || matrix[0][j] == 0) {
                matrix[i][j] = 0;
            }
        }
    }

    // Set the first row
    if (matrix[0][0] == 0) {
        for (int j = 0; j < matrix[0].length; j++) {
            matrix[0][j] = 0;
        }
    }

    // set the first col
    if (isCol) {
        for (int i = 0; i < matrix.length; i++) {
            matrix[i][0] = 0;
        }
    }
}
```

## Q566 Reshape the Matrix

This is a easy problem, but the key idea is that how to use division and modulus to map the index of a 2D matrix:

Given a `m * n` matrix, it can be shaped to a `r * c` matrix, if `m * n = r * c`. We can think this by a auxilary 1D array. The element in M1 can be put into that array with `a[i * n + j] = m1[i][j]`(0-index). Then, we have `m2[i / c][i % c] = a[i]`. 


