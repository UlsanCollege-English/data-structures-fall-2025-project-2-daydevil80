# src/trie.py
"""
Trie data structure for autocomplete.

Public surface expected by tests:
- class Trie
  - insert(word: str, freq: float) -> None
  - remove(word: str) -> bool
  - contains(word: str) -> bool
  - complete(prefix: str, k: int) -> list[str]
  - stats() -> tuple[int, int, int]  # (words, height, nodes)

Complexity target (justify in docstrings):
- insert/remove/contains: O(len(word))
- complete(prefix, k): roughly O(m + k log k')
"""
import heapq


class TrieNode:
    __slots__ = ("children", "is_word", "freq")

    def __init__(self):
        self.children = {}
        self.is_word = False
        self.freq = 0.0


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self._words = 0
        self._nodes = 1

    # -------------------------------
    # Insert a word with frequency
    # -------------------------------
    def insert(self, word: str, freq: float):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
                self._nodes += 1
            node = node.children[c]
        if not node.is_word:
            self._words += 1
        node.is_word = True
        node.freq = freq

    # -------------------------------
    # Check if word exists
    # -------------------------------
    def contains(self, word: str) -> bool:
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_word

    # -------------------------------
    # Remove word from trie
    # -------------------------------
    def remove(self, word: str) -> bool:
        removed = False

        def _remove(node, i):
            nonlocal removed
            if i == len(word):
                if not node.is_word:
                    return False
                node.is_word = False
                node.freq = 0.0
                self._words -= 1
                removed = True
                return len(node.children) == 0
            ch = word[i]
            if ch not in node.children:
                return False
            should_delete = _remove(node.children[ch], i + 1)
            if should_delete:
                del node.children[ch]
                self._nodes -= 1
                return not node.is_word and not node.children
            return False

        _remove(self.root, 0)
        return removed

    # -------------------------------
    # Autocomplete top-k by frequency
    # -------------------------------
    def complete(self, prefix: str, k: int) -> list[str]:
        node = self.root
        for c in prefix:
            if c not in node.children:
                return []
            node = node.children[c]

        heap = []  # max-heap by freq, then lexicographically

        def dfs(n, path):
            if n.is_word:
                heap.append((-n.freq, path))
            for ch in n.children:
                dfs(n.children[ch], path + ch)

        dfs(node, prefix)

        # Sort by freq descending, then lex ascending
        heap.sort()
        return [word for _, word in heap[:k]]

    # -------------------------------
    # Return number of words, height, nodes
    # -------------------------------
    def stats(self):
        def height(node):
            if not node.children:
                return 1
            return 1 + max(height(c) for c in node.children.values())

        h = height(self.root)
        return (self._words, h, self._nodes)

    # -------------------------------
    # Return list of all (word, freq)
    # -------------------------------
    def items(self):
        result = []

        def dfs(node, path):
            if node.is_word:
                result.append((path, node.freq))
            for ch, nxt in node.children.items():
                dfs(nxt, path + ch)

        dfs(self.root, "")
        return result