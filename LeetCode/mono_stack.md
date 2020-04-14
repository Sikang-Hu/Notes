# Monotonic Stack

Monotonic stack is a stack where the elements keeps monotonic order. For simplicity, here we take monotonic increasing stack as an example.

## Properties

Monotonic Stack can help find the next less number & previous less number (increasing stack), or next larger number & previous larger number(decreasing stack). And it can find for all the element in **linear** time. 

The increasing stack will remove the peak, while decreasing stack will remove the ridge. For example, let `arr[] = {1, 4, 7, 5, 6, 3}`, and we traverse it with increasing stack. First, it will push 1, 4 ,7 into the stack, while it come to 5, it will pop 7(peak) and push 5.

## Typical Paradigm for Monotonic Stack

```java
for (int i = 0; i < arr.size(); i++) {
    while(!stack.empty() && arr[i] < stack.peek()) {
        stack.pop(); 
        // do something with the popped value, while arr[i] is
        // the next less number of it.
    }
    // at this point, arr[stack.peek()] is the previous less number of arr[i]
    stack.push(i); // we can retrieve data with index easily. 
}
```

We still need to take care of the duplicate elements: set strict less and non-strict less for NLE and PLE respectively. For the example above, the condition for NLE is strict(in the loop), the condition for PLE is non-strict(outside the loop).

## Related Question

### Q42 Trapping Rain Water

### Q84 Largest Rectangle in Histogram

```java
public int largestRectangleArea(int[] heights) {
        Stack<Integer> stack = new Stack<>();
        int max = 0;
        
        
        for (int i = 0; i < heights.length; i++) {
            while (!stack.empty() && heights[i] < heights[stack.peek()]) {
                int hi = stack.pop();
                int prev = stack.empty() ? -1 : stack.peek();
                max = Math.max(max, heights[hi] * (i - prev - 1));
            }
            stack.push(i);
        }
        
        while (!stack.empty()) {
            int hi = stack.pop();
            int prev = stack.empty() ? -1 : stack.peek();
            max = Math.max(max, heights[hi] * (heights.length - prev - 1));
        }
        return max;
    }
```

### Q85 Maximal Rectangle

