# Subsets

---
problem_name: Subsets 1
platform: NeetCode
difficulty: Medium
pattern: Backtracking
primary_tags:
  - Backtracking
  - Recursion
  - Bit Manipulation
status: Not Started
last_updated: 2026-04-16
---

## Problem Statement

### Challenge

Given an array `nums` of unique integers, return all possible subsets (the power set).

- Input: array of unique integers.
- Output: list of all subsets, including the empty subset.
- No duplicate subsets allowed; order of subsets in the output does not matter.

### Examples

#### Example 1

- Input: `nums = [1, 2, 3]`
- Output: `[[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]`
- Explanation: Every combination of including or excluding each of the 3 elements produces 2³ = 8 subsets.

#### Example 2

- Input: `nums = [7]`
- Output: `[[], [7]]`
- Explanation: The only element can either be included or excluded, giving exactly 2 subsets.

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        subset = []

        def dfs(i):
            if i >= len(nums):
                res.append(subset.copy())
                return
            subset.append(nums[i])
            dfs(i + 1)
            subset.pop()
            dfs(i + 1)

        dfs(0)
        return res

sol = Solution()

result1 = sol.subsets([1, 2, 3])
assert sorted(map(tuple, result1)) == sorted(map(tuple, [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]))
print(result1)  # [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]

result2 = sol.subsets([7])
assert sorted(map(tuple, result2)) == sorted(map(tuple, [[], [7]]))
print(result2)  # [[], [7]]
```

### Key Insight

At each index there are exactly two choices: include the element or skip it. Traversing all such binary decisions from left to right produces every possible subset exactly once. For an array of length `n` this yields `2ⁿ` subsets, and copying each subset of average length `n/2` gives the `O(n · 2ⁿ)` time bound.

```python
# 2^n subsets for each array length n
for n in range(6):
    print(f"n={n}  subsets={2**n}  total_nodes={2**(n+1) - 1}")
# n=0  subsets=1   total_nodes=1
# n=1  subsets=2   total_nodes=3
# n=2  subsets=4   total_nodes=7
# n=3  subsets=8   total_nodes=15
# n=4  subsets=16  total_nodes=31
# n=5  subsets=32  total_nodes=63
```

### Complexity Snapshot

- Time: O(n · 2ⁿ) — 2ⁿ subsets, each copy costs up to O(n).
- Space: O(n) extra (recursion depth + `subset` buffer); O(2ⁿ) for the output list.
- Total states in decision tree: 2ⁿ leaf nodes, 2ⁿ⁺¹ − 1 total nodes.

---

## Core Concepts

### Concept 1: Pattern Definition

**Backtracking** is a depth-first search over a decision tree where each node represents a partial solution. At each step we make a choice, recurse, then *undo* that choice (backtrack) before trying the alternative. Here, the decision at every index is include/skip, and there is no pruning needed because every path to a leaf is valid.

```python
# Minimal skeleton — the backtracking pattern shape
def backtrack(i):
    if base_case(i):
        record()
        return
    make_choice()
    backtrack(i + 1)   # explore with choice
    undo_choice()
    backtrack(i + 1)   # explore without choice
```

### Concept 2: Decision Process / State View

State at each recursive call: `(i, subset)` where `i` is the current index and `subset` is the list of elements chosen so far.

```
dfs(i=0, subset=[])
├── include nums[0]  →  dfs(i=1, subset=[1])
│   ├── include nums[1]  →  dfs(i=2, subset=[1,2])
│   │   ├── include nums[2]  →  dfs(i=3)  → record [1,2,3]
│   │   └── skip    nums[2]  →  dfs(i=3)  → record [1,2]
│   └── skip    nums[1]  →  dfs(i=2, subset=[1])
│       ├── include nums[2]  →  dfs(i=3)  → record [1,3]
│       └── skip    nums[2]  →  dfs(i=3)  → record [1]
└── skip    nums[0]  →  dfs(i=1, subset=[])
    ...                                    → record [], [2], [3], [2,3]
```

The snippet below instruments the algorithm to print each `(i, subset, action)` state as it runs:

```python
from typing import List

def subsets_traced(nums: List[int]) -> List[List[int]]:
    res = []
    subset = []

    def dfs(i):
        if i >= len(nums):
            print(f"  record  i={i}  subset={subset}")
            res.append(subset.copy())
            return
        # include branch
        subset.append(nums[i])
        print(f"  include i={i}  val={nums[i]}  subset={subset}")
        dfs(i + 1)
        # backtrack
        subset.pop()
        print(f"  skip    i={i}  val={nums[i]}  subset={subset}")
        dfs(i + 1)

    dfs(0)
    return res

subsets_traced([1, 2, 3])
```

### Concept 3: When to Use This Pattern

Triggers:

- Problem asks to enumerate *all* combinations / subsets / permutations.
- Output size is exponential (2ⁿ, n!, etc.).
- Elements are unique and ordering within a subset does not matter.
- "Generate all..." or "find all possible..." phrasing.
- Problem involves choosing a subset of items from a set.

Related problems:

- Subsets II (duplicates allowed in input)
- Combination Sum
- Permutations
- Letter Combinations of a Phone Number
- Palindrome Partitioning

### Important Caveat

> **Always append a copy of `subset`, not the list itself.**
> `res.append(subset)` stores a reference. Backtracking will mutate that reference later, corrupting previously recorded subsets. Use `res.append(subset.copy())` or `res.append(subset[:])`.

```python
from typing import List

# ── WRONG: appending the reference ───────────────────────────────────────────
def subsets_wrong(nums: List[int]) -> List[List[int]]:
    res, subset = [], []
    def dfs(i):
        if i >= len(nums):
            res.append(subset)       # BUG — stores reference
            return
        subset.append(nums[i]); dfs(i + 1); subset.pop(); dfs(i + 1)
    dfs(0)
    return res

print(subsets_wrong([1, 2]))
# [[], [], [], []]  — all entries are the same mutated object

# ── CORRECT: appending a snapshot ────────────────────────────────────────────
def subsets_correct(nums: List[int]) -> List[List[int]]:
    res, subset = [], []
    def dfs(i):
        if i >= len(nums):
            res.append(subset.copy())  # snapshot — safe
            return
        subset.append(nums[i]); dfs(i + 1); subset.pop(); dfs(i + 1)
    dfs(0)
    return res

print(subsets_correct([1, 2]))
# [[1, 2], [1], [2], []]
```

---

## Step-by-Step Walkthrough

1. **Initialize result and buffer.**

   ```python
   res = []
   subset = []
   ```

   `res` collects finished subsets; `subset` is the mutable work buffer.

2. **Define the recursive helper `dfs(i)`.**

   ```python
   def dfs(i):
   ```

   `i` is the index of the element we are currently deciding on.

3. **Base case: index past the array → record the subset.**

   ```python
   if i >= len(nums):
       res.append(subset.copy())
       return
   ```

   Every path through the tree is valid, so we record at every leaf.

4. **Branch 1 — include `nums[i]`.**

   ```python
   subset.append(nums[i])
   dfs(i + 1)
   ```

   Add the current element and recurse on the remaining elements.

5. **Backtrack — remove `nums[i]`.**

   ```python
   subset.pop()
   ```

   Undo the inclusion so we can explore the exclusion branch with a clean state.

6. **Branch 2 — skip `nums[i]`.**

   ```python
   dfs(i + 1)
   ```

   Recurse without touching `subset`, representing exclusion of this element.

7. **Kick off the recursion.**

   ```python
   dfs(0)
   ```

   Start from index 0 with an empty subset.

8. **Return the accumulated result.**

   ```python
   return res
   ```

### Complete Solution (Primary)

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        subset = []

        def dfs(i):
            if i >= len(nums):
                res.append(subset.copy())
                return
            subset.append(nums[i])
            dfs(i + 1)
            subset.pop()
            dfs(i + 1)

        dfs(0)
        return res

print(Solution().subsets([1, 2, 3]))
# [[1,2,3],[1,2],[1,3],[1],[2,3],[2],[3],[]]
```

### Dry Run

Input: `nums = [1, 2, 3]`

| Call        | Action               | `subset` after action | `res` after action          |
|-------------|----------------------|-----------------------|-----------------------------|
| dfs(0)      | include 1            | [1]                   |                             |
| dfs(1)      | include 2            | [1, 2]                |                             |
| dfs(2)      | include 3            | [1, 2, 3]             |                             |
| dfs(3)      | base case → copy     | [1, 2, 3]             | [[1,2,3]]                   |
| back to(2)  | pop 3 (backtrack)    | [1, 2]                |                             |
| dfs(3)      | base case → copy     | [1, 2]                | [[1,2,3],[1,2]]             |
| back to(1)  | pop 2 (backtrack)    | [1]                   |                             |
| dfs(2)      | include 3            | [1, 3]                |                             |
| dfs(3)      | base case → copy     | [1, 3]                | [[1,2,3],[1,2],[1,3]]       |
| back to(2)  | pop 3 (backtrack)    | [1]                   |                             |
| dfs(3)      | base case → copy     | [1]                   | [...,[1]]                   |
| back to(0)  | pop 1 (backtrack)    | []                    |                             |
| dfs(1)      | include 2            | [2]                   |                             |
| ...         | (symmetric)          | ...                   | [...,[2,3],[2]]             |
| back to(0)  | skip 1 → dfs(1)      | []                    |                             |
| dfs(2)      | include 3 → dfs(3)   | [3]                   | [...,[3]]                   |
| dfs(3)      | base case → copy     | []                    | [...,[]]                    |

Final `res`: `[[1,2,3],[1,2],[1,3],[1],[2,3],[2],[3],[]]`

The Python trace below reproduces the table automatically:

```python
from typing import List

def subsets_dry_run(nums: List[int]) -> List[List[int]]:
    res = []
    subset = []

    def dfs(i):
        if i >= len(nums):
            print(f"dfs({i})     base case → copy   subset={list(subset)}  res_len={len(res)+1}")
            res.append(subset.copy())
            return
        subset.append(nums[i])
        print(f"dfs({i})     include {nums[i]}          subset={list(subset)}")
        dfs(i + 1)
        subset.pop()
        print(f"back to({i}) pop {nums[i]} (backtrack)  subset={list(subset)}")
        print(f"dfs({i})     skip {nums[i]}             subset={list(subset)}")
        dfs(i + 1)

    dfs(0)
    return res

subsets_dry_run([1, 2, 3])
```

---

## Interactive Visualizer (Markdown-Compatible Spec)

### Visualizer Input

```python
nums = [1, 2, 3]
```

### State Fields to Track

- `i` — current index being decided (0-based).
- `subset` — current partial subset (list of integers).
- `action` — most recent operation (`include`, `skip`, `backtrack`, `record`).
- `res_count` — number of subsets recorded so far.

### Step Events

| Event       | Trigger                        | State Change                                |
|-------------|--------------------------------|---------------------------------------------|
| `include`   | Branch 1: append nums[i]       | `subset` grows by 1; `i` advances by 1      |
| `backtrack` | After include branch finishes  | `subset` shrinks by 1 (pop)                 |
| `skip`      | Branch 2: do not append        | `subset` unchanged; `i` advances by 1       |
| `record`    | Base case reached (i == n)     | Copy of `subset` appended to `res`; `res_count` += 1 |

The Python generator below yields each step as a dict, ready for any visualizer to consume:

```python
from typing import List, Iterator

def subsets_steps(nums: List[int]) -> Iterator[dict]:
    """Yield one event dict per visualizer step."""
    res = []
    subset = []

    def dfs(i):
        if i >= len(nums):
            yield {"action": "record",    "i": i, "subset": list(subset), "res_count": len(res) + 1}
            res.append(subset.copy())
            return
        yield {"action": "at_index",  "i": i, "subset": list(subset), "res_count": len(res)}
        subset.append(nums[i])
        yield {"action": "include",   "i": i, "subset": list(subset), "res_count": len(res)}
        yield from dfs(i + 1)
        subset.pop()
        yield {"action": "backtrack", "i": i, "subset": list(subset), "res_count": len(res)}
        yield {"action": "skip",      "i": i, "subset": list(subset), "res_count": len(res)}
        yield from dfs(i + 1)

    yield from dfs(0)

for step in subsets_steps([1, 2, 3]):
    print(step)
```

### Tree / Graph / Table Representation

Render a **binary decision tree**:

- Root node: `(i=0, subset=[])`
- Left edge labeled **include**, right edge labeled **skip**.
- Leaf nodes (depth = n) highlighted and labeled with the recorded subset.
- Backtrack edges shown as dashed return arrows.

---

## Knowledge Check (Quiz)

### Q1 — Complexity

What is the time complexity of the backtracking solution?

- A) O(n²)
- B) O(2ⁿ)
- C) O(n · 2ⁿ)
- D) O(n log n)

**Answer: C**
Explanation: There are 2ⁿ leaf nodes (subsets). At each leaf we copy `subset`, which takes O(n) in the worst case. Multiplying gives O(n · 2ⁿ).

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        subset = []
        copy_ops = [0]  # count O(n) copy operations

        def dfs(i):
            if i >= len(nums):
                copy_ops[0] += len(subset)  # each copy costs O(len(subset))
                res.append(subset.copy())
                return
            subset.append(nums[i])
            dfs(i + 1)
            subset.pop()
            dfs(i + 1)

        dfs(0)
        n = len(nums)
        print(f"n={n}  subsets=2^n={2**n}  copy_ops={copy_ops[0]}  n*2^n={n * 2**n}")
        return res

Solution().subsets([1, 2, 3])  # n=3  subsets=8  copy_ops=12  n*2^n=24
Solution().subsets([1, 2, 3, 4])  # n=4  subsets=16  copy_ops=32  n*2^n=64
```

---

### Q2 — Correctness Invariant

Which invariant guarantees no duplicate subsets are generated?

- A) We sort `nums` before recursing.
- B) We always recurse left-to-right (i → i+1), never revisiting earlier indices.
- C) We use a set to de-duplicate results.
- D) We prune branches when the current element has been seen before.

**Answer: B**
Explanation: Because we only advance the index forward (`dfs(i + 1)`), each element is decided at most once per path, preventing the same element from appearing twice or subsets from being generated in different orderings of the same elements.

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        subset = []

        def dfs(i):
            if i >= len(nums):
                res.append(subset.copy())
                return
            subset.append(nums[i])
            dfs(i + 1)   # always i+1 — never revisit earlier indices
            subset.pop()
            dfs(i + 1)   # always i+1 — skip also moves forward

        dfs(0)
        return res

result = Solution().subsets([1, 2, 3])
# Prove no duplicates: converting to sorted tuples and checking set size
as_tuples = [tuple(sorted(s)) for s in result]
assert len(as_tuples) == len(set(as_tuples)), "duplicates found!"
print(f"{len(result)} subsets, all unique")  # 8 subsets, all unique
```

---

### Q3 — Edge Case

What does the algorithm return for `nums = []`?

- A) `None`
- B) `[]`
- C) `[[]]`
- D) Raises an IndexError

**Answer: C**
Explanation: `dfs(0)` is called immediately and hits the base case `i >= len(nums)` (0 >= 0), so it records a copy of the empty `subset` — giving `[[]]`.

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        subset = []

        def dfs(i):
            if i >= len(nums):       # 0 >= 0 is True immediately for nums=[]
                res.append(subset.copy())
                return
            subset.append(nums[i])
            dfs(i + 1)
            subset.pop()
            dfs(i + 1)

        dfs(0)
        return res

result = Solution().subsets([])
print(result)           # [[]]
assert result == [[]]   # the empty subset is always valid
```

---

### Q4 — Implementation Pitfall

Why is `res.append(subset)` wrong in the base case?

- A) `subset` is a tuple and cannot be appended to a list.
- B) It stores a reference; later `pop()` calls mutate the stored object.
- C) It skips the empty subset.
- D) It causes infinite recursion.

**Answer: B**
Explanation: `subset` is a mutable list. Appending it directly stores a reference. Every subsequent `subset.pop()` during backtracking modifies the same object that is already in `res`, corrupting results. `subset.copy()` creates an independent snapshot.

```python
from typing import List

# ── WRONG: stores reference ──────────────────────────────────────────────────
class SolutionWrong:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        subset = []

        def dfs(i):
            if i >= len(nums):
                res.append(subset)   # BUG: reference — backtrack will mutate this
                return
            subset.append(nums[i])
            dfs(i + 1)
            subset.pop()
            dfs(i + 1)

        dfs(0)
        return res

print(SolutionWrong().subsets([1, 2, 3]))
# [[], [], [], [], [], [], [], []]  — all corrupted to empty by backtracking

# ── CORRECT: stores a snapshot ───────────────────────────────────────────────
class SolutionCorrect:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        subset = []

        def dfs(i):
            if i >= len(nums):
                res.append(subset.copy())  # snapshot — immune to future pops
                return
            subset.append(nums[i])
            dfs(i + 1)
            subset.pop()
            dfs(i + 1)

        dfs(0)
        return res

print(SolutionCorrect().subsets([1, 2, 3]))
# [[1,2,3],[1,2],[1,3],[1],[2,3],[2],[3],[]]
```

---

## Code Playground

### Starter Code

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        subset = []

        def dfs(i):
            # TODO: add base case

            # TODO: include branch

            # TODO: backtrack

            # TODO: skip branch
            pass

        dfs(0)
        return res

# Default test
sol = Solution()
print(sol.subsets([1, 2, 3]))
# Expected: [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
```

### Suggested Experiments

1. **Constraint variant — subsets of exactly size k:**

   ```python
   from typing import List

   def subsets_of_size_k(nums: List[int], k: int) -> List[List[int]]:
       res = []
       subset = []

       def dfs(i):
           # TODO: record only when len(subset) == k
           # TODO: include branch
           # TODO: backtrack
           # TODO: skip branch
           pass

       dfs(0)
       return res

   print(subsets_of_size_k([1, 2, 3, 4], 2))
   # Expected: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
   ```

2. **Alternative paradigm — iterative building:**

   ```python
   from typing import List

   def subsets_iterative(nums: List[int]) -> List[List[int]]:
       res = [[]]  # TODO: extend res for each num
       for num in nums:
           pass    # TODO: duplicate existing subsets, append num to each
       return res

   # Verify matches the backtracking output
   from solution import Solution  # replace with your backtracking class
   bt = Solution().subsets([1, 2, 3])
   it = subsets_iterative([1, 2, 3])
   assert sorted(map(tuple, bt)) == sorted(map(tuple, it))
   print(it)
   ```

3. **Optimization / proof task — bitmask approach:**

   ```python
   from typing import List

   def subsets_bitmask(nums: List[int]) -> List[List[int]]:
       n = len(nums)
       res = []
       for mask in range(1 << n):
           # TODO: build subset from bits of mask
           pass
       return res

   print(subsets_bitmask([1, 2, 3]))
   # Prove: each integer 0..2^n-1 maps to exactly one unique subset
   # Hint: two different masks differ in at least one bit → different subsets
   ```

---

## Alternative Approaches

### Alternative 1: Iterative Building

**Intuition:** Start with `[[]]`. For each number, duplicate every existing subset and append the number to each duplicate. This doubles the list with each element.

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = [[]]

        for num in nums:
            res += [subset + [num] for subset in res]

        return res

print(Solution().subsets([1, 2, 3]))
# [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
```

- Time: O(n · 2ⁿ)
- Space: O(n) extra; O(2ⁿ) for output.
- **When to prefer:** Avoids recursion overhead; useful when stack depth is a concern or in languages with limited recursion.

---

### Alternative 2: Bit Manipulation

**Intuition:** There are `2ⁿ` integers from `0` to `2ⁿ − 1`. Each bit `j` of integer `i` encodes whether `nums[j]` is included in the subset for mask `i`.

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        res = []
        for i in range(1 << n):
            subset = [nums[j] for j in range(n) if (i & (1 << j))]
            res.append(subset)
        return res

print(Solution().subsets([1, 2, 3]))
# [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]

# Visualise which bits map to which subset
nums = [1, 2, 3]
for mask in range(1 << len(nums)):
    subset = [nums[j] for j in range(len(nums)) if (mask & (1 << j))]
    print(f"mask={mask:03b}  subset={subset}")
# mask=000  subset=[]
# mask=001  subset=[1]
# mask=010  subset=[2]
# mask=011  subset=[1, 2]
# mask=100  subset=[3]
# ...
```

- Time: O(n · 2ⁿ)
- Space: O(n) extra; O(2ⁿ) for output.
- **When to prefer:** Elegant one-liner logic; great for interviews when you want to show multiple approaches. Note: limited to ~30 elements before integer overflow in some languages.

---

### Comparison Table

| Approach         | Pros                              | Cons                                     | Time       | Space  | Best Use Case                        |
|------------------|-----------------------------------|------------------------------------------|------------|--------|--------------------------------------|
| Backtracking     | General, extends to pruned search | Recursion overhead, `.copy()` easy to forget | O(n·2ⁿ) | O(n)   | Base pattern; extends to Subsets II  |
| Iterative        | No recursion, simple loop         | Less intuitive for pruning variants      | O(n·2ⁿ)   | O(n)   | Stack-depth concerns                 |
| Bit Manipulation | Compact; shows binary intuition   | Hard to extend to duplicates/pruning     | O(n·2ⁿ)   | O(n)   | Demonstrating alternative thinking   |

---

## Common Mistakes

### Mistake 1: Appending a reference instead of a copy

**Wrong:**

```python
from typing import List

def subsets_wrong(nums: List[int]) -> List[List[int]]:
    res, subset = [], []
    def dfs(i):
        if i >= len(nums):
            res.append(subset)   # stores reference — backtracking will mutate it
            return
        subset.append(nums[i]); dfs(i + 1); subset.pop(); dfs(i + 1)
    dfs(0)
    return res

print(subsets_wrong([1, 2]))  # [[], [], [], []]  — all corrupted
```

**Correct:**

```python
from typing import List

def subsets_correct(nums: List[int]) -> List[List[int]]:
    res, subset = [], []
    def dfs(i):
        if i >= len(nums):
            res.append(subset.copy())  # snapshot of current state
            return
        subset.append(nums[i]); dfs(i + 1); subset.pop(); dfs(i + 1)
    dfs(0)
    return res

print(subsets_correct([1, 2]))  # [[1, 2], [1], [2], []]
```

**Why it fails:** `subset` is mutated by every `pop()` call during backtracking. All entries in `res` that point to the same object get corrupted.
**Quick check:** `assert all(id(a) != id(b) for a in res for b in res if a is not b)` — all objects should be distinct.

---

### Mistake 2: Forgetting the empty subset in the iterative approach

**Wrong:**

```python
from typing import List

def subsets_wrong(nums: List[int]) -> List[List[int]]:
    res = []   # missing the seed
    for num in nums:
        res += [subset + [num] for subset in res]
    return res

print(subsets_wrong([1, 2, 3]))  # []  — produces nothing
```

**Correct:**

```python
from typing import List

def subsets_correct(nums: List[int]) -> List[List[int]]:
    res = [[]]  # seed with empty subset
    for num in nums:
        res += [subset + [num] for subset in res]
    return res

print(subsets_correct([1, 2, 3]))
# [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
```

**Why it fails:** Without `[[]]` as the seed, the first iteration produces nothing and all subsequent iterations remain empty.
**Quick check:** `assert [] in result` — confirm `[]` appears in the final output.

---

### Mistake 3: Re-using the current index instead of advancing

**Wrong:**

```python
from typing import List

def subsets_wrong(nums: List[int]) -> List[List[int]]:
    res, subset = [], []
    def dfs(i):
        if i >= len(nums):
            res.append(subset.copy())
            return
        for j in range(i, len(nums)):   # starts at i — reuses current element
            subset.append(nums[j])
            dfs(j)                       # passes j, not j+1 — causes duplicates
            subset.pop()
    dfs(0)
    return res

print(subsets_wrong([1, 2, 3]))  # contains duplicates like [1,1,...] and infinite recursion
```

**Correct:**

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res, subset = [], []
        def dfs(i):
            if i >= len(nums):
                res.append(subset.copy())
                return
            subset.append(nums[i])
            dfs(i + 1)   # advance to next index
            subset.pop()
            dfs(i + 1)
        dfs(0)
        return res

result = Solution().subsets([1, 2, 3])
# Verify no element appears twice in any subset
assert all(len(s) == len(set(s)) for s in result)
print(result)  # [[1,2,3],[1,2],[1,3],[1],[2,3],[2],[3],[]]
```

**Why it fails:** Passing `j` instead of `j + 1` allows the same index to be picked again, generating duplicates like `[1, 1]`.
**Quick check:** Verify no subset has repeated elements when the input has no duplicates.

---

### Mistake 4: Integer overflow in bitmask for large n

**Wrong (C/Java pattern, illustrated in Python for clarity):**

```python
# In C/Java: `1 << 31` overflows a 32-bit int — silently wrong
# Simulated here to show the conceptual issue:
n = 31
mask = 1 << n   # Python handles this fine, but C/Java would overflow
print(f"n={n}  1<<n={mask}")  # Python: 2147483648 (correct)
# In C: (int)(1 << 31) == -2147483648 (wrong — undefined behaviour)
```

**Correct (Python is safe; note for other languages):**

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        res = []
        for i in range(1 << n):   # Python ints are arbitrary precision — always safe
            subset = [nums[j] for j in range(n) if (i & (1 << j))]
            res.append(subset)
        return res

# Confirm correct count for n=4
result = Solution().subsets([1, 2, 3, 4])
assert len(result) == 2**4
print(f"{len(result)} subsets")  # 16 subsets
# In C++/Java use: 1LL << n   or   (long)(1 << n)
```

**Why it fails:** In statically-typed languages `1 << 31` overflows a 32-bit int. Python is exempt but the mistake surfaces when translating code.
**Quick check:** Confirm `n` satisfies problem constraints (here n ≤ 10, so no risk).

---

## Flashcards

### Card 1

**Front:** What is the base case for the backtracking solution to Subsets?

**Back:** When `i >= len(nums)` — we have made a decision for every element, so we append a copy of `subset` to `res` and return.

```python
def dfs(i):
    if i >= len(nums):          # base case: all decisions made
        res.append(subset.copy())
        return
    # ... recurse ...
```

### Card 2

**Front:** Why is the time complexity O(n · 2ⁿ) and not just O(2ⁿ)?

**Back:** There are 2ⁿ subsets (leaves in the decision tree). Recording each one requires copying `subset`, which takes O(n) time in the worst case. The copy cost gives the extra factor of n.

```python
# Cost breakdown: 2^n leaves × O(n) copy each = O(n·2^n)
n = 4
print(f"leaves={2**n}  max_copy_cost={n}  total≈{n * 2**n}")
# leaves=16  max_copy_cost=4  total≈64
```

### Card 3

**Front:** What is the core backtracking pattern for subset generation?

**Back:** Include the element → recurse → pop (backtrack) → recurse again without the element. Two recursive calls per index, advancing `i` by 1 each time, covering all 2ⁿ combinations.

```python
def dfs(i):
    if i >= len(nums):
        res.append(subset.copy()); return
    subset.append(nums[i]); dfs(i + 1)  # include + recurse
    subset.pop();           dfs(i + 1)  # backtrack + skip
```

---

## Quick Reference

### Template Code

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        subset = []

        def dfs(i):
            if i >= len(nums):
                res.append(subset.copy())
                return
            subset.append(nums[i])
            dfs(i + 1)
            subset.pop()
            dfs(i + 1)

        dfs(0)
        return res

print(Solution().subsets([1, 2, 3]))
# [[1,2,3],[1,2],[1,3],[1],[2,3],[2],[3],[]]
```

### Pattern Mnemonic

`Initialize res/subset → Define dfs(i) → Base case: record copy → Include + Recurse → Backtrack (pop) → Skip + Recurse → Start dfs(0) → Return res`

### Key Metrics

- Key decision steps: 2 per index (include / skip).
- Dominant growth term: 2ⁿ subsets.
- Max recursion depth: n (one frame per index).
- Memory driver: `subset` buffer of depth n; output list of 2ⁿ entries.

---

## Next Steps

### Next Challenges

1. **Subsets II** (Medium) — same problem but `nums` may contain duplicates; requires sorting and skip-duplicate logic.
2. **Combination Sum** (Medium) — generate subsets that sum to a target; adds pruning to the backtracking.
3. **Permutations** (Medium) — generate all orderings; decision at each step is which unused element to place next.
4. **Palindrome Partitioning** (Medium) — partition a string into palindromic substrings; backtracking with a validity check at each branch.

### Study Tips

1. **Code from memory first:** Close this guide and re-implement `subsets` using only the mnemonic. Check correctness against the dry run.
2. **Draw the decision tree:** For `nums = [1, 2]`, sketch the full tree on paper. Label each edge include/skip and each leaf with its subset.
3. **Spaced repetition schedule:** Review today, then again in 1 day, 3 days, 7 days, and 14 days. At each session, implement from scratch before re-reading.
4. **Extend the template:** After mastering the base version, solve Subsets II using the same template — this forces you to understand where duplicate-skipping logic slots in.
