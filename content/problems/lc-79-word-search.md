# Word Search

---
problem_name: Word Search
platform: LeetCode / NeetCode
difficulty: Medium
pattern: Backtracking + Matrix DFS
primary_tags:
  - Backtracking
  - DFS
  - Matrix
status: Not Started
last_updated: 2026-04-20
---

## Problem Statement

### Challenge

Given a 2D board of characters and a string `word`, return `True` if `word` can be formed by walking through adjacent cells.

- You may move only up, down, left, or right.
- A cell cannot be reused in the same path.
- Input: `board: List[List[str]]`, `word: str`
- Output: boolean (`True`/`False`)

### Examples

#### Example 1

- Input:
  - `board = [["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]]`
  - `word = "CAT"`
- Output: `True`
- Explanation: Path is `(0,2)='C' -> (1,2)='A' -> (1,3)='T'`.

#### Example 2

- Input:
  - `board = [["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]]`
  - `word = "BAT"`
- Output: `False`
- Explanation: You can start at `'B'`, but no valid adjacent path completes `'A' -> 'T'` without violating adjacency or reuse rules.

```python
from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        ROWS, COLS = len(board), len(board[0])

        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or c < 0 or r >= ROWS or c >= COLS:
                return False
            if board[r][c] != word[i] or board[r][c] == '#':
                return False

            temp = board[r][c]
            board[r][c] = '#'
            res = (dfs(r + 1, c, i + 1) or
                   dfs(r - 1, c, i + 1) or
                   dfs(r, c + 1, i + 1) or
                   dfs(r, c - 1, i + 1))
            board[r][c] = temp
            return res

        for r in range(ROWS):
            for c in range(COLS):
                if dfs(r, c, 0):
                    return True
        return False

sol = Solution()
board1 = [["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]]
board2 = [["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]]

assert sol.exist(board1, "CAT") is True
assert sol.exist(board2, "BAT") is False
print(True, False)
```

### Key Insight

This is a path-existence search in a grid with a no-reuse constraint, so backtracking DFS is a direct fit. From each cell, recursively try to match `word[i]`; if it matches, mark the cell as used, explore 4 neighbors for `word[i+1]`, then restore the cell on return.

```python
# Worst-case branching intuition: each character can branch up to 4 directions.
for n in range(1, 6):
    print(f"n={n}, max_paths_upper_bound={4**n}")
```

### Complexity Snapshot

- Time: `O(m * 4^n)`
  - `m = ROWS * COLS` cells as start points
  - `n = len(word)` recursive depth
- Space: `O(n)` recursion depth (excluding input board)
- Max recursion depth: `n`

---

## Core Concepts

### Concept 1: Pattern Definition

Backtracking DFS explores one path at a time, marks state as used, and undoes that change when returning.

```python
def dfs(r, c, i):
    if i == len(word):
        return True
    if out_of_bounds_or_mismatch_or_used(r, c, i):
        return False
    mark_used(r, c)
    found = dfs(r+1, c, i+1) or dfs(r-1, c, i+1) or dfs(r, c+1, i+1) or dfs(r, c-1, i+1)
    unmark_used(r, c)
    return found
```

### Concept 2: Decision Process / State View

State is `(r, c, i)`:

- `r, c`: current board position
- `i`: index in `word` we are trying to match

```python
def trace(board, word):
    ROWS, COLS = len(board), len(board[0])

    def dfs(r, c, i):
        print(f"state=(r={r}, c={c}, i={i}), action=enter")
        if i == len(word):
            print("state=matched_all, action=success")
            return True
        if r < 0 or c < 0 or r >= ROWS or c >= COLS:
            print("action=fail_out_of_bounds")
            return False
        if board[r][c] != word[i] or board[r][c] == '#':
            print("action=fail_mismatch_or_used")
            return False

        temp = board[r][c]
        board[r][c] = '#'
        print(f"action=mark, cell=({r},{c}), char={temp}")

        res = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
               dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))

        board[r][c] = temp
        print(f"action=unmark, cell=({r},{c}), result={res}")
        return res

    return dfs(0, 2, 0)

print(trace([["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]], "CAT"))
```

### Concept 3: When to Use This Pattern

Use this pattern when:

- You need to determine if a path exists in a grid.
- Movement is local (4-direction or 8-direction neighbors).
- Cells/nodes cannot be reused in the same path.
- Input sizes are small enough for exponential branching.

Related problems:

- LeetCode 212 Word Search II
- LeetCode 130 Surrounded Regions
- LeetCode 200 Number of Islands
- LeetCode 79 Word Search (this problem)

### Important Caveat

Most common mistake: marking visited but not restoring during backtracking.

```python
# WRONG: never restores cell, so future paths are blocked incorrectly.
def wrong_exist(board, word):
    ROWS, COLS = len(board), len(board[0])

    def dfs(r, c, i):
        if i == len(word):
            return True
        if r < 0 or c < 0 or r >= ROWS or c >= COLS:
            return False
        if board[r][c] != word[i] or board[r][c] == '#':
            return False

        board[r][c] = '#'
        return (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
                dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))

    for r in range(ROWS):
        for c in range(COLS):
            if dfs(r, c, 0):
                return True
    return False

b = [["A","B"],["C","D"]]
print(wrong_exist(b, "AB"))
print(b)  # board mutated: contains '#'

# FIX: save temp, restore after exploring neighbors.
```

---

## Step-by-Step Walkthrough

1. Initialize dimensions.

```python
ROWS, COLS = len(board), len(board[0])
```

Why: bounds checking needs matrix dimensions.

2. Define recursive `dfs(r, c, i)`.

```python
def dfs(r, c, i):
    ...
```

Why: this state captures position and progress in the target word.

3. Base case: matched all letters.

```python
if i == len(word):
    return True
```

Why: this signals a complete valid path.

4. Reject invalid states.

```python
if r < 0 or c < 0 or r >= ROWS or c >= COLS:
    return False
if board[r][c] != word[i] or board[r][c] == '#':
    return False
```

Why: prevents out-of-range access, mismatches, and cell reuse.

5. Mark current cell as used.

```python
temp = board[r][c]
board[r][c] = '#'
```

Why: prevents revisiting this cell in the current path.

6. Explore 4 neighbors for the next character.

```python
res = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
       dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
```

Why: these are the only allowed moves.

7. Backtrack by restoring the cell.

```python
board[r][c] = temp
```

Why: other starting paths must see the original board.

8. Try every cell as a start.

```python
for r in range(ROWS):
    for c in range(COLS):
        if dfs(r, c, 0):
            return True
return False
```

Why: valid path can begin anywhere.

### Complete Solution (Primary)

```python
from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        ROWS, COLS = len(board), len(board[0])

        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or c < 0 or r >= ROWS or c >= COLS:
                return False
            if board[r][c] != word[i] or board[r][c] == '#':
                return False

            temp = board[r][c]
            board[r][c] = '#'
            res = (dfs(r + 1, c, i + 1) or
                   dfs(r - 1, c, i + 1) or
                   dfs(r, c + 1, i + 1) or
                   dfs(r, c - 1, i + 1))
            board[r][c] = temp
            return res

        for r in range(ROWS):
            for c in range(COLS):
                if dfs(r, c, 0):
                    return True
        return False

board = [["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]]
print(Solution().exist(board, "CAT"))
# True
```

### Dry Run

Input:

- `board = [["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]]`
- `word = "CAT"`

Key path found:

1. Start `(0,2)` with `i=0`, matches `'C'`.
2. Move to `(1,2)` with `i=1`, matches `'A'`.
3. Move to `(1,3)` with `i=2`, matches `'T'`.
4. `i=3 == len(word)`, return `True`.

```python
from typing import List

def exist_trace(board: List[List[str]], word: str) -> bool:
    ROWS, COLS = len(board), len(board[0])

    def dfs(r, c, i):
        print(f"enter r={r}, c={c}, i={i}")
        if i == len(word):
            print("matched all chars")
            return True
        if r < 0 or c < 0 or r >= ROWS or c >= COLS:
            return False
        if board[r][c] != word[i] or board[r][c] == '#':
            return False

        temp = board[r][c]
        board[r][c] = '#'
        print(f"mark ({r},{c}) as #")
        res = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
               dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
        board[r][c] = temp
        print(f"unmark ({r},{c}) restore {temp}, res={res}")
        return res

    for r in range(ROWS):
        for c in range(COLS):
            if dfs(r, c, 0):
                return True
    return False

print(exist_trace([["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]], "CAT"))
```

---

## Interactive Visualizer (Markdown-Compatible Spec)

### Visualizer Input

- Format:
  - `board: List[List[str]]`
  - `word: str`
- Sample input:
  - `board = [["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]]`
  - `word = "CAT"`

```python
board = [["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]]
word = "CAT"
```

### State Fields to Track

- `r`, `c`
- `i`
- `char_needed = word[i]` (if `i < len(word)`)
- `path` (list of coordinates)
- `action`
- `result_so_far` (boolean or `None` before completion)

### Step Events

Event types:

- `enter`
- `fail`
- `mark`
- `recurse`
- `unmark`
- `success`

```python
def event_stream(board, word):
    ROWS, COLS = len(board), len(board[0])
    path = []

    def dfs(r, c, i):
        yield {"type": "enter", "r": r, "c": c, "i": i, "path": path.copy()}
        if i == len(word):
            yield {"type": "success", "r": r, "c": c, "i": i, "path": path.copy()}
            return True
        if r < 0 or c < 0 or r >= ROWS or c >= COLS or board[r][c] != word[i] or board[r][c] == '#':
            yield {"type": "fail", "r": r, "c": c, "i": i, "path": path.copy()}
            return False

        temp = board[r][c]
        board[r][c] = '#'
        path.append((r, c))
        yield {"type": "mark", "r": r, "c": c, "i": i, "path": path.copy()}

        for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
            yield {"type": "recurse", "from": (r, c), "to": (nr, nc), "i": i + 1, "path": path.copy()}
            ok = yield from dfs(nr, nc, i + 1)
            if ok:
                board[r][c] = temp
                path.pop()
                yield {"type": "unmark", "r": r, "c": c, "i": i, "path": path.copy()}
                return True

        board[r][c] = temp
        path.pop()
        yield {"type": "unmark", "r": r, "c": c, "i": i, "path": path.copy()}
        return False

    for r in range(ROWS):
        for c in range(COLS):
            ok = yield from dfs(r, c, 0)
            if ok:
                return

for e in event_stream([["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]], "CAT"):
    print(e)
```

### Tree / Graph / Table Representation

Render as a DFS tree where each node is `(r,c,i)` and edges are directional moves. Also show a timeline table of events with columns: `step`, `event_type`, `state`, `path`.

---

## Knowledge Check (Quiz)

### Q1. Complexity

What is the recommended worst-case time complexity?

A. `O(m * n)`  
B. `O(m * 2^n)`  
C. `O(m * 4^n)`  
D. `O(4^m)`

Correct answer: **C**

Explanation: There are `m` starting cells and up to 4 branches per character for `n` characters.

```python
m = 15
n = 4
print(m * (4 ** n))  # illustrative upper bound
```

### Q2. Correctness Invariant

Which invariant must hold during DFS?

A. Same cell can be reused if character repeats in `word`  
B. Every recursive level must move diagonally once  
C. Path may contain duplicates if index increases  
D. Current path contains unique cells only

Correct answer: **D**

Explanation: Reusing a cell in one path violates problem constraints.

```python
path = [(0, 2), (1, 2), (1, 3)]
print(len(path) == len(set(path)))  # True means unique cells
```

### Q3. Edge Case

If `word` has length 1, what is enough to return `True`?

A. Any two adjacent equal letters  
B. At least one board cell equals `word[0]`  
C. Board must be square  
D. Start only at `(0,0)`

Correct answer: **B**

Explanation: A one-letter word needs only one matching cell.

```python
board = [["A","B"],["C","D"]]
word = "C"
print(any(board[r][c] == word[0] for r in range(len(board)) for c in range(len(board[0]))))
```

### Q4. Implementation Pitfall

What bug appears if you do not restore `board[r][c]` after recursion?

A. The algorithm becomes iterative  
B. Future starts see permanently blocked cells  
C. Time complexity improves incorrectly  
D. It only affects diagonal problems

Correct answer: **B**

Explanation: Mutation leaks across sibling branches and across start cells.

```python
board = [["A","B"],["C","D"]]
board[0][0] = '#'
print(board)  # future searches now see altered board
```

---

## Code Playground

### Starter Code

```python
from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        ROWS, COLS = len(board), len(board[0])

        def dfs(r, c, i):
            # TODO: base case for full word match
            # TODO: reject invalid states (bounds, mismatch, used)
            # TODO: mark used
            # TODO: recurse in 4 directions
            # TODO: unmark and return result
            return False

        # TODO: try starting dfs from every cell
        return False

board = [["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]]
print(Solution().exist(board, "CAT"))
# True
```

### Suggested Experiments

1. Constraint variant: allow 8 directions (including diagonals).

```python
from typing import List

def exist_8dir(board: List[List[str]], word: str) -> bool:
    # TODO: implement DFS with 8 neighbors
    return False

print(exist_8dir([["A","B"],["C","D"]], "AD"))  # expected True in 8-dir
```

2. Alternative paradigm: iterative DFS with explicit stack state.

```python
from typing import List

def exist_iterative(board: List[List[str]], word: str) -> bool:
    # TODO: simulate recursion using stack of (r, c, i, path_or_mark_info)
    return False

print(exist_iterative([["A","B"],["C","D"]], "AB"))  # expected True
```

3. Optimization/proof task: prune with frequency counts.

```python
from collections import Counter

def can_pass_frequency_check(board, word):
    board_count = Counter(ch for row in board for ch in row)
    word_count = Counter(word)
    # TODO: return False if any char needed more than available
    return True

print(can_pass_frequency_check([["A","B"],["C","D"]], "AAB"))  # expected False
```

---

## Alternative Approaches

### Alternative 1: Backtracking with `visited` matrix

Intuition: Instead of mutating `board`, use `visited[r][c]` to block reuse in current path.

```python
from typing import List

class SolutionVisited:
    def exist(self, board: List[List[str]], word: str) -> bool:
        ROWS, COLS = len(board), len(board[0])
        visited = [[False] * COLS for _ in range(ROWS)]

        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or c < 0 or r >= ROWS or c >= COLS:
                return False
            if board[r][c] != word[i] or visited[r][c]:
                return False

            visited[r][c] = True
            res = (dfs(r + 1, c, i + 1) or
                   dfs(r - 1, c, i + 1) or
                   dfs(r, c + 1, i + 1) or
                   dfs(r, c - 1, i + 1))
            visited[r][c] = False
            return res

        for r in range(ROWS):
            for c in range(COLS):
                if dfs(r, c, 0):
                    return True
        return False

print(SolutionVisited().exist([["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]], "CAT"))
# True
```

- Time: `O(m * 4^n)`
- Space: `O(n + m)` where `m` here includes visited matrix storage (`ROWS*COLS`)
- Prefer when mutating input board is not allowed.

### Alternative 2: Backtracking with `path` set

Intuition: Track visited cells as `(r, c)` in a set during current recursion path.

```python
from typing import List

class SolutionSet:
    def exist(self, board: List[List[str]], word: str) -> bool:
        ROWS, COLS = len(board), len(board[0])
        path = set()

        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or c < 0 or r >= ROWS or c >= COLS:
                return False
            if board[r][c] != word[i] or (r, c) in path:
                return False

            path.add((r, c))
            res = (dfs(r + 1, c, i + 1) or
                   dfs(r - 1, c, i + 1) or
                   dfs(r, c + 1, i + 1) or
                   dfs(r, c - 1, i + 1))
            path.remove((r, c))
            return res

        for r in range(ROWS):
            for c in range(COLS):
                if dfs(r, c, 0):
                    return True
        return False

print(SolutionSet().exist([["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]], "BAT"))
# False
```

- Time: `O(m * 4^n)`
- Space: `O(n)` for path set + recursion stack
- Prefer when you want explicit path membership semantics.

### Comparison Table

| Approach | Pros | Cons | Time | Space | Best Use Case |
|---|---|---|---|---|---|
| In-place mark (`'#'`) | Lowest auxiliary space, fast in practice | Mutates input temporarily | `O(m * 4^n)` | `O(n)` | Typical interview implementation |
| Visited matrix | Clear separation of data/state | Extra `ROWS*COLS` memory | `O(m * 4^n)` | `O(ROWS*COLS + n)` | Input must remain untouched |
| Path set | Very explicit constraints | Hash overhead each step | `O(m * 4^n)` | `O(n)` | Teaching/debugging path states |

---

## Common Mistakes

### Mistake 1: Forgetting to restore board cell

Wrong snippet:

```python
def wrong_restore(board, word):
    ROWS, COLS = len(board), len(board[0])
    def dfs(r, c, i):
        if i == len(word):
            return True
        if r < 0 or c < 0 or r >= ROWS or c >= COLS or board[r][c] != word[i] or board[r][c] == '#':
            return False
        board[r][c] = '#'
        return dfs(r, c + 1, i + 1)  # no restore
    return dfs(0, 0, 0)

b = [["A","B"]]
print(wrong_restore(b, "AB"))
print(b)  # mutated permanently
```

Correct snippet:

```python
def right_restore(board, word):
    ROWS, COLS = len(board), len(board[0])
    def dfs(r, c, i):
        if i == len(word):
            return True
        if r < 0 or c < 0 or r >= ROWS or c >= COLS or board[r][c] != word[i] or board[r][c] == '#':
            return False
        temp = board[r][c]
        board[r][c] = '#'
        res = dfs(r, c + 1, i + 1)
        board[r][c] = temp
        return res
    return dfs(0, 0, 0)

b = [["A","B"]]
print(right_restore(b, "AB"))
print(b)  # original board preserved
```

Why wrong fails: state leaks into other branches.

Quick check: print board before and after call; they should match.

### Mistake 2: Missing bounds checks before board access

Wrong snippet:

```python
def wrong_bounds(board):
    r, c = -1, 0
    return board[r][c]  # accidental negative index semantics in Python

print(wrong_bounds([["A"],["B"]]))  # returns 'B', usually unintended
```

Correct snippet:

```python
def right_bounds(board):
    r, c = -1, 0
    if r < 0 or c < 0 or r >= len(board) or c >= len(board[0]):
        return None
    return board[r][c]

print(right_bounds([["A"],["B"]]))  # None
```

Why wrong fails: Python negative indexes can silently read last row/col.

Quick check: always gate with explicit `r < 0 or c < 0` first.

### Mistake 3: Reusing cell in same path

Wrong snippet:

```python
def wrong_reuse(board, word):
    # Pretends "AA" exists in single-cell board because no visited protection.
    ROWS, COLS = len(board), len(board[0])
    def dfs(r, c, i):
        if i == len(word):
            return True
        if r < 0 or c < 0 or r >= ROWS or c >= COLS or board[r][c] != word[i]:
            return False
        return dfs(r, c, i + 1)  # reuses same cell
    return dfs(0, 0, 0)

print(wrong_reuse([["A"]], "AA"))  # incorrect True
```

Correct snippet:

```python
def right_reuse(board, word):
    ROWS, COLS = len(board), len(board[0])
    def dfs(r, c, i):
        if i == len(word):
            return True
        if r < 0 or c < 0 or r >= ROWS or c >= COLS or board[r][c] != word[i] or board[r][c] == '#':
            return False
        temp = board[r][c]
        board[r][c] = '#'
        res = dfs(r, c, i + 1)
        board[r][c] = temp
        return res
    return dfs(0, 0, 0)

print(right_reuse([["A"]], "AA"))  # False
```

Why wrong fails: violates no-reuse constraint.

Quick check: single-cell board with `word` length 2 should be `False`.

### Mistake 4: Starting DFS from only one cell

Wrong snippet:

```python
def wrong_single_start(board, word):
    # only starts from (0,0)
    return board[0][0] == word[0]

print(wrong_single_start([["X","A"]], "A"))  # False (incorrect)
```

Correct snippet:

```python
def right_all_starts(board, word):
    return any(board[r][c] == word[0] for r in range(len(board)) for c in range(len(board[0])))

print(right_all_starts([["X","A"]], "A"))  # True
```

Why wrong fails: valid path may start at any cell.

Quick check: verify nested loop over every `(r, c)` start point.

---

## Flashcards

- **Front:** What is the base case in Word Search DFS?
- **Back:** When `i == len(word)`, every character has been matched, so return `True`.
  ```python
  def base(i, word):
      return i == len(word)
  print(base(3, "CAT"))
  ```

- **Front:** Why is time complexity `O(m * 4^n)`?
- **Back:** Try DFS from `m` cells, and each level can branch up to 4 directions for `n` characters.
  ```python
  m, n = 12, 5
  print(m * (4 ** n))
  ```

- **Front:** What is the core backtracking intuition here?
- **Back:** Mark current cell, explore neighbors, then unmark so other paths can reuse it later.
  ```python
  cell = "A"
  used = '#'
  print(cell, "->", used, "->", cell)
  ```

---

## Quick Reference

### Template Code

```python
from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        ROWS, COLS = len(board), len(board[0])

        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or c < 0 or r >= ROWS or c >= COLS or board[r][c] != word[i] or board[r][c] == '#':
                return False

            temp = board[r][c]
            board[r][c] = '#'
            res = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
                   dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
            board[r][c] = temp
            return res

        for r in range(ROWS):
            for c in range(COLS):
                if dfs(r, c, 0):
                    return True
        return False

print(Solution().exist([["A","B","C","D"],["S","A","A","T"],["A","C","A","E"]], "CAT"))
# True
```

### Pattern Mnemonic

`Match -> Mark -> Explore 4 -> Unmark -> Repeat from next start`

### Key Metrics

- Number of key steps: 8
- Dominant growth term: `4^n`
- Max recursion depth / memory driver: `n = len(word)`

---

## Next Steps

### Next Challenges

- LeetCode 200 Number of Islands (Easy-Medium)
- LeetCode 130 Surrounded Regions (Medium)
- LeetCode 212 Word Search II (Hard)
- LeetCode 489 Robot Room Cleaner (Hard)

### Study Tips

- Re-implement this from scratch using all 3 visited styles: in-place mark, visited matrix, set.
- Trace one successful and one failing path manually on paper.
- Practice writing the failure guard line from memory (`bounds + mismatch + used`).
- Spaced repetition: review after 1 day, 3 days, 7 days, and 14 days.
