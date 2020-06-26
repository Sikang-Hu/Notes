# Parentheses Problem

## Q32 Longest Valid Parentheses

### Key Idea

1. A sequence of Parentheses is valid if every left parethesis can be closed by a right parenthesis.

2. Based on idea 1, we can record how many unclosed left parenthesis we have while we iterate the sequence from left to right.

3. Everytime the unclosed left parenthesis reached 0, we have covered a valid parentheses subarray, we need to consider this candidate(i.e. compare its length with the max we have). 

4. What if there are extra right parenthesis? It means that they will never be closed, so we need to move the start point to its right, then continue our iteration.

5. If we just go from left to right, there are some problem in cases such as "(()", where we will not consider the candidate because of those extra left parentheses. To prevent that, we run the symmetric algorithm from right to left to cover them, where we will cover cases with extra "(" but not ")";

### Implementation

```java
public int longestValidParentheses(String s) {
    int left = -1;
    int right = 0;
    int count = 0;
    int result = 0;

    // Here we make left the index before first parenthesis in the window, 
    // right the index of last parenthesis in the window, so that the length will simply be right - left.
    while (right < s.length()) {
        if (s.charAt(right) == '(') {
            count++
        } else {
            count--;
            if (count == 0) {
                result = Math.max(result, right - left);
            } else if (count < 0) {
                count = 0;
                left = right;
            }
        }
        right++;
    }

    int low = left;
    int left = s.length() - 1;
    count = 0;
    while (left > low) {
        if (s.charAt(left) == ')') {
            count++
        } else {
            count--;
            if (count == 0) {
                result = Math.max(result, right - left);
            } else if (count < 0) {
                count = 0;
                right = left;
            }
        }
        left--;
    }

    return result;
}
```

### Other solutions

#### 1. Dynamic Programming

The sub problem `dp[i]` can be defined as the longest parentheses ending at `i`. Then, we can know that, a valid substring must end with ')'. Then we only care about `s.charAt(i) == ')'`.

Suppose you are the given the optimal solution `dp[i]`, there are two cases:

   1. `s[i - 1] == '('`, then it can consist a new pair of parentheses, `dp[i] = 2 + dp[i - 2]`
   2. `s[i - 1] == ')'`, then the longest substring at `i` should be like `"( dp[i - 1] )"`, and the index of the first "(" is `i - 1 - dp[i - 1]`, then we have `dp[i] = s[i - 1 - dp[i - 1]] == '(' ? dp[i - 1] + 2 + dp[i - dp[i - 1] - 2] : 0;`


Implementation:
```java
public int longestValidParentheses(String s) {
        int maxans = 0;
        int dp[] = new int[s.length()];
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == ')') {
                if (s.charAt(i - 1) == '(') {
                    dp[i] = (i >= 2 ? dp[i - 2] : 0) + 2;
                } else if (i - dp[i - 1] > 0 && s.charAt(i - dp[i - 1] - 1) == '(') {
                    // use the condition to cope with invalid index.
                    dp[i] = dp[i - 1] + ((i - dp[i - 1]) >= 2 ? dp[i - dp[i - 1] - 2] : 0) + 2;
                }
                maxans = Math.max(maxans, dp[i]);
            }
        }
        return maxans;
    }
```