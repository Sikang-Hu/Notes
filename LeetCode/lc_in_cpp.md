# LeetCode in CPP

# 876 Middle of the Linked List

For this question, we are required to output the second middle node, if there are two middle node(even number of node). If you are asked to return the first middle node. You need to avoid use the last node:

```cpp
ListNode* middleNode(ListNode* head) {
    ListNode* s = head;
    ListNode* f = head;
    while (f != nullptr && f->next != nullptr && f->next->next != nullptr) {
        s = s->next;
        f = f->next->next;
    }
    return s;
}
```