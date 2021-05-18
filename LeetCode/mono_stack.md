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
The main idea is to maintain a decreasing stack when iterating through the array, the previous larger bar is the left bound and the next larger bar is the right bound. Every time we find the next larger, we can close a interval by add the rain water into the ret: `ret += distance * height`, where `height` is the minimum of left bound and right bound minus current height(lower water must have been added before).
```java
public int trap(int[] height) {
    Deque<Integer> s = new ArrayDeque<>();
    int ret = 0;
    for (int i = 0; i < height.length; i++) {
        while (!s.isEmpty() && height[i] > height[s.peek()]) {
            // find the right bound(next larger in the descreasing stack)
            int top = s.pop();
            if (s.isEmpty()) break; // if there is no left bound, cannot trap rain
            int dis = i - s.peek() - 1; // dis between left bound and right bound
            int h = Math.min(height[i], height[s.peek()]) - height[top];
            ret += dis * h;
        }
        s.push(i);
    }
    return ret;
}
```

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

## Monotonic Queue

### Q239 Sliding Window Maximum

The key idea is that, suppose we maintain a deque for only elements in the window. If we slide the window, all the elements in the queue that are less than the next element will never be the maximum in later windows, so we can just disregard it.

Another key point is maintain the index instead of the actual number so that we can locate the element, to remove elements that are not in the window.

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    ArrayDeque<Integer> dq = new ArrayDeque<>();
    int[] re = new int[nums.length - k + 1];
    dq.add(0);
    for (int i = 1; i < k; i++) {
        while (!dq.isEmpty() && nums[dq.getLast()] < nums[i]) dq.removeLast();
        dq.addLast(i);
    }
    re[0] = nums[dq.peekFirst()];
    
    for (int i = k ; i < nums.length; i++) {
        if (dq.peekFirst() == i - k) {
            dq.removeFirst();
        }
        while (!dq.isEmpty() && nums[dq.getLast()] < nums[i]) dq.removeLast();
        dq.addLast(i);
        re[i - k + 1] = nums[dq.getFirst()];
    }
    return re;
}
```

This problem can also solved by dynamic programming. Divide the array into segemnts of size k.


