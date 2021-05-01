# Trie

## Code to construct a Trie
Given a list of word, how to constuct a list of Trie, and search on it. Remember when we work with suffix, we should insert and search in reverse order,
```java
public class Trie {
    private Node root = new Node();

    public Trie(String[] words) {
        Node iter = root;
        for (String w : words) {
            for (char c : w.toCharArray()) {
                if (iter.children[c - 'a'] == null) {
                    iter.children[c - 'a'] = new Node();
                }
                iter = iter.children[c - 'a'];
            }
            iter.end = true;
        }
    }

    public boolean search(String word) {
        Node iter = root;
        for (char c : word.toCharArray()) {
            if (iter.children[c - 'a'] != null) {
                iter = iter.children[c - 'a'];
            } else
                return false;
        }
        return iter.end;
    }

    public boolean delete(String word) {

    }

    static class Node {
        private Node[] children = new Node[26]; // take the lower case as example
        private boolean end;
    }
}
```

## Q745 Prefix and Suffix Search
This question requires the method to return the largest of the item. When solved using two tries and set(or list), we need to search in the finally result sets to find the largest index appear in two collections. However, if we can **combine the prefix and suffix requirement, and construct only one trie**, the word at larger index will always override smaller satisfied index at the trie node. Hence, the requirement is satisfied automatically.

### Trie of Suffix Wrapped Words
For each word, we **append all the possible suffix** to the beginning to form a new key for search. E.g. "apple" `->` "#apple", "e#apple", "le#apple", "ple#apple", "pple#apple", "apple#apple". Then searching prefix "ap", suffix "le" is to search word "le#ap". 

Wrap with suffix is a great thought.

```java
class WordFilter {
    private Trie root = new Trie();

    public WordFilter(String[] words) {
        for (int i = 0; i < words.length; i++) {
            String w = words[i] + "{"; // '{' is the next char to 'z', if don't know, use (char)('z' + 1);
            for (int j = 0; j < w.length(); j++) { // for each suffix wrapped word, insert into trie.
                Trie iter = root;
                for (int k = j; k < 2 * w.length() - 1; k++) { 
                    int c = w.charAt(k % w.length()) - 'a';
                    if (iter.children[c] == null) {
                        iter.children[c] = new Trie();
                    }
                    iter = iter.children[c];
                    iter.idx = i; // important: for each suffix wrapped word, we assign its idx to current trie
                }
                iter.idx = i;
            }
        }
    }
    
    public int f(String prefix, String suffix) {
        String w = suffix + "{" + prefix;
        Trie iter = root;
        for (char c : w.toCharArray()) {
            if (iter.children[c - 'a'] == null) return -1;
            iter = iter.children[c - 'a'];
        }
        return iter.idx;
    }
}

class Trie {
    Trie[] children = new Trie[27]; // not private, cause in different class.
    int idx = -1;
}
```