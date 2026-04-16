# Combination Sum

---
problem_name: Combination Sum
platform: LeetCode / NeetCode
difficulty: Medium
pattern: Backtracking
primary_tags:
  - Backtracking
  - Recursion
  - DFS
status: Not Started
last_updated: 2026-04-16
---

## Problem Statement

### Challenge

Given a list of **distinct** integers `nums` and an integer `target`, return all unique combinations where chosen numbers sum to `target`.

- You can use each value in `nums` **unlimited times**.
- Two combinations are the same if they contain the same values with the same frequencies.
- Output order does not matter.

### Examples

#### Example 1

- Input: `nums = [2, 5, 6, 9], target = 9`
- Output: `[[2, 2, 5], [9]]`
- Explanation: `2 + 2 + 5 = 9` and `9 = 9`.

#### Example 2

- Input: `nums = [3, 4, 5], target = 16`
- Output: `[[3,3,3,3,4], [3,3,5,5], [3,4,4,5], [4,4,4,4]]`
- Explanation: These are all unique frequency combinations that sum to 16.

```python
from typing import List

class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        res = []
        cur = []

        def dfs(i, total):
            if total == target:
                res.append(cur.copy())
                return
            for j in range(i, len(nums)):
                if total + nums[j] > target:
                    break
                cur.append(nums[j])
                dfs(j, total + nums[j])
                cur.pop()

        dfs(0, 0)
        return res

sol = Solution()

out1 = sol.combinationSum([2, 5, 6, 9], 9)
assert sorted(map(tuple, out1)) == sorted(map(tuple, [[2, 2, 5], [9]]))
print(out1)

out2 = sol.combinationSum([3, 4, 5], 16)
assert sorted(map(tuple, out2)) == sorted(map(tuple, [[3,3,3,3,4], [3,3,5,5], [3,4,4,5], [4,4,4,4]]))
print(out2)
```

### Key Insight

Build combinations in non-decreasing index order, so `[2,5,2]` is never generated separately from `[2,2,5]`. Backtracking explores candidate choices from index `i` onward, and reusing a number is done by recursing with the **same index**. Sorting enables pruning: once `total + nums[j] > target`, all later values are also too large.

```python
# Growth intuition for recursion depth bound ~ target / min(nums)
def max_depth(target, nums):
    return target // min(nums)

print(max_depth(9, [2,5,6,9]))   # 4
print(max_depth(16, [3,4,5]))    # 5
```

### Complexity Snapshot

- Time: `O(2^(t/m))` (commonly cited backtracking bound)
  - `t = target`, `m = min(nums)`
- Space: `O(t/m)` recursion depth (excluding output)
- Output size can be exponential and dominates in dense cases.

---

## Core Concepts

### Concept 1: Pattern Definition

This is a backtracking problem where state is a partially built combination `cur` and current sum `total`. At each state, choose next candidate from current start index onward.

```python
# Pattern skeleton (<=10 lines)
def dfs(i, total):
    if total == target:
        record(cur.copy())
        return
    for j in range(i, len(nums)):
        if total + nums[j] > target:
            break
        cur.append(nums[j])
        dfs(j, total + nums[j])
        cur.pop()
```

### Concept 2: Decision Process / State View

State: `(i, cur, total)`

- `i`: minimum index allowed next (keeps combinations unique)
- `cur`: current chosen numbers
- `total`: sum of numbers in `cur`

```python
def trace_states(nums, target):
    nums.sort()
    cur = []

    def dfs(i, total):
        print(f"enter i={i}, cur={cur}, total={total}")
        if total == target:
            print(f"record i={i}, cur={cur}, total={total}")
            return
        for j in range(i, len(nums)):
            nxt = total + nums[j]
            if nxt > target:
                print(f"prune j={j}, val={nums[j]}, total={total}")
                break
            print(f"choose j={j}, val={nums[j]}")
            cur.append(nums[j])
            dfs(j, nxt)
            cur.pop()
            print(f"backtrack j={j}, cur={cur}")

    dfs(0, 0)

trace_states([2, 5, 6, 9], 9)
```

### Concept 3: When to Use This Pattern

Use this pattern when:

- You need **all** combinations (not just count or one solution).
- Choices can be repeated (unbounded pick).
- Order should not create duplicates.
- Constraints are small enough for exponential search.

Related problems:

- Combination Sum II
- Combination Sum III
- Subsets
- Permutations
- Palindrome Partitioning

### Important Caveat

Most common mistake: moving to `j + 1` after choosing `nums[j]`. That incorrectly forbids reuse.

```python
# WRONG: disallows reuse because it advances index after choosing
from typing import List

def wrong(nums: List[int], target: int) -> List[List[int]]:
    nums.sort()
    res, cur = [], []

    def dfs(i, total):
        if total == target:
            res.append(cur.copy())
            return
        for j in range(i, len(nums)):
            if total + nums[j] > target:
                break
            cur.append(nums[j])
            dfs(j + 1, total + nums[j])  # BUG
            cur.pop()

    dfs(0, 0)
    return res

print(wrong([2,3,6,7], 7))  # misses [2,2,3]

# FIX: recurse with dfs(j, ...) so same value can be picked again
```

---

## Step-by-Step Walkthrough

1. Initialize result and path containers.

```python
res = []
cur = []
nums.sort()
```

Why: `res` stores complete answers, `cur` is current path, sorting enables prune.

2. Define DFS state `(i, total)`.

```python
def dfs(i, total):
    ...
```

Why: `i` controls allowed indices (uniqueness), `total` tracks current sum.

3. Base case when target is reached.

```python
if total == target:
    res.append(cur.copy())
    return
```

Why: this path is a valid combination.

4. Iterate choices from `i` onward.

```python
for j in range(i, len(nums)):
    ...
```

Why: prevents generating permutations of same combination.

5. Prune impossible branches.

```python
if total + nums[j] > target:
    break
```

Why: sorted array guarantees later numbers are larger.

6. Choose current number and recurse.

```python
cur.append(nums[j])
dfs(j, total + nums[j])
```

Why: `j` (not `j+1`) allows unlimited reuse.

7. Backtrack to restore state.

```python
cur.pop()
```

Why: removes last decision before trying next candidate.

8. Start DFS and return result.

```python
dfs(0, 0)
return res
```

Why: begin with empty path and sum zero.

### Complete Solution (Primary)

```python
from typing import List

class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        res = []
        cur = []

        def dfs(i, total):
            if total == target:
                res.append(cur.copy())
                return

            for j in range(i, len(nums)):
                nxt = total + nums[j]
                if nxt > target:
                    break
                cur.append(nums[j])
                dfs(j, nxt)
                cur.pop()

        dfs(0, 0)
        return res

print(Solution().combinationSum([2, 5, 6, 9], 9))
# Expected: [[2, 2, 5], [9]] (order may vary)
```

### Dry Run

Input: `nums = [2, 5, 6, 9]`, `target = 9`

- Start `dfs(0,0)`, `cur=[]`
- Choose `2` -> `cur=[2]`, total 2
- Choose `2` -> `cur=[2,2]`, total 4
- Choose `2` -> total 6
- Choose `2` -> total 8
- Next `2` would make 10, prune branch
- Try `5` from total 4 -> total 9, record `[2,2,5]`
- Backtrack and try higher values; only `[9]` reaches target from root

```python
def dry_run_trace(nums, target):
    nums.sort()
    res = []
    cur = []

    def dfs(i, total):
        print(f"enter i={i}, total={total}, cur={cur}")
        if total == target:
            print(f"record {cur}")
            res.append(cur.copy())
            return

        for j in range(i, len(nums)):
            nxt = total + nums[j]
            if nxt > target:
                print(f"prune at j={j}, val={nums[j]}, total={total}")
                break
            cur.append(nums[j])
            print(f"choose {nums[j]} -> cur={cur}")
            dfs(j, nxt)
            cur.pop()
            print(f"backtrack -> cur={cur}")

    dfs(0, 0)
    return res

print(dry_run_trace([2, 5, 6, 9], 9))
```

---

## Interactive Visualizer (Markdown-Compatible Spec)

### Visualizer Input

- Format: `{ "nums": List[int], "target": int }`
- Sample: `{ "nums": [2, 5, 6, 9], "target": 9 }`

```python
sample = {"nums": [2, 5, 6, 9], "target": 9}
```

### State Fields to Track

- `i`: current start index
- `j`: current choice index in loop
- `cur`: current path
- `total`: current sum
- `action`: `enter|choose|record|prune|backtrack`
- `res_count`: number of found combinations

### Step Events

```python
def event_stream(nums, target):
    nums = sorted(nums)
    cur = []
    res = []

    def dfs(i, total):
        yield {"action": "enter", "i": i, "j": None, "cur": cur.copy(), "total": total, "res_count": len(res)}
        if total == target:
            res.append(cur.copy())
            yield {"action": "record", "i": i, "j": None, "cur": cur.copy(), "total": total, "res_count": len(res)}
            return
        for j in range(i, len(nums)):
            nxt = total + nums[j]
            if nxt > target:
                yield {"action": "prune", "i": i, "j": j, "cur": cur.copy(), "total": total, "res_count": len(res)}
                break
            cur.append(nums[j])
            yield {"action": "choose", "i": i, "j": j, "cur": cur.copy(), "total": nxt, "res_count": len(res)}
            yield from dfs(j, nxt)
            cur.pop()
            yield {"action": "backtrack", "i": i, "j": j, "cur": cur.copy(), "total": total, "res_count": len(res)}

    yield from dfs(0, 0)

for e in event_stream([2,5,6,9], 9):
    print(e)
```

### Tree / Graph / Table Representation

Render as recursion tree where each node is `(cur,total)` and edge label is chosen value.

---

## Knowledge Check (Quiz)

1. What is the typical backtracking complexity bound for this problem?
A. `O(n)`
B. `O(n log n)`
C. `O(2^(t/m))`
D. `O(t^2)`

Correct: **C**

```python
# Depth is bounded by target/min(nums), tree branching makes it exponential.
target, nums = 16, [3,4,5]
m = min(nums)
print(target // m)  # depth upper bound indicator
```

2. Which invariant prevents duplicate permutations?
A. Always sort output at the end
B. Always recurse with j+1
C. Only choose indices from current i forward
D. Use a set of tuples for every path

Correct: **C**

```python
# Forward-only index progression yields canonical order in each path.
def demo_forward_only():
    nums = [2,3]
    paths = []
    cur = []
    def dfs(i, total):
        if total == 5:
            paths.append(cur.copy())
            return
        for j in range(i, len(nums)):
            if total + nums[j] > 5:
                break
            cur.append(nums[j])
            dfs(j, total + nums[j])
            cur.pop()
    dfs(0, 0)
    print(paths)  # [[2,3]] no [3,2]

demo_forward_only()
```

3. Edge case: `nums=[3]`, `target=5`. Output?
A. `[[3,2]]`
B. `[[3]]`
C. `[]`
D. Error

Correct: **C**

```python
print(Solution().combinationSum([3], 5))  # []
```

4. Implementation pitfall: after choosing `nums[j]`, next call should be?
A. `dfs(j + 1, total + nums[j])`
B. `dfs(0, total + nums[j])`
C. `dfs(j, total + nums[j])`
D. `dfs(i + 1, total + nums[j])`

Correct: **C**

```python
# Reuse requires staying at j.
nums = [2,3,6,7]
print(Solution().combinationSum(nums, 7))  # contains [2,2,3]
```

---

## Code Playground

### Starter Code

```python
from typing import List

class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        res = []
        cur = []

        def dfs(i, total):
            # TODO: if total == target, append copy of cur to res
            # TODO: iterate j from i to len(nums)-1
            # TODO: prune when total + nums[j] > target
            # TODO: choose nums[j], recurse with dfs(j, ...), backtrack
            pass

        dfs(0, 0)
        return res

print(Solution().combinationSum([2,5,6,9], 9))
# Expected (order may vary): [[2,2,5], [9]]
```

### Suggested Experiments

1. Constraint variant: each number can be used at most `k` times.

```python
from typing import List

def combinationSum_k(nums: List[int], target: int, k: int) -> List[List[int]]:
    # TODO: backtracking with usage count limit k per value
    return []

print(combinationSum_k([2,3,5], 8, 2))
```

2. Alternative paradigm: iterative DP that stores combinations by sum.

```python
from typing import List

def combinationSum_dp(nums: List[int], target: int) -> List[List[int]]:
    # TODO: dp[s] = list of combinations that sum to s
    return []

print(combinationSum_dp([2,3,6,7], 7))
```

3. Optimization task: count combinations without listing them.

```python
from typing import List

def countCombinationSum(nums: List[int], target: int) -> int:
    # TODO: return number of unique combinations (order-insensitive)
    return 0

print(countCombinationSum([2,3,6,7], 7))  # expected 2
```

---

## Alternative Approaches

### Alternative 1: Include/Skip Binary Backtracking

Intuition: at each index, either include current value (stay at same index) or skip it (move to next index).

```python
from typing import List

def combinationSum_include_skip(nums: List[int], target: int) -> List[List[int]]:
    res = []
    cur = []

    def dfs(i, total):
        if total == target:
            res.append(cur.copy())
            return
        if i >= len(nums) or total > target:
            return

        cur.append(nums[i])
        dfs(i, total + nums[i])
        cur.pop()

        dfs(i + 1, total)

    dfs(0, 0)
    return res

print(combinationSum_include_skip([2,5,6,9], 9))
# Expected (order may vary): [[2,2,5], [9]]
```

- Time: `O(2^(t/m))`
- Space: `O(t/m)`
- Prefer when teaching decision-tree include/exclude pattern.

### Alternative 2: DP by Sum (Build Combinations)

Intuition: build combinations for each sum from `0` to `target`, ensuring non-decreasing order to avoid duplicates.

```python
from typing import List

def combinationSum_dp(nums: List[int], target: int) -> List[List[int]]:
    nums.sort()
    dp = [[] for _ in range(target + 1)]
    dp[0] = [[]]

    for num in nums:
        for s in range(num, target + 1):
            for prev in dp[s - num]:
                if not prev or prev[-1] <= num:
                    dp[s].append(prev + [num])

    return dp[target]

print(combinationSum_dp([2,5,6,9], 9))
# Expected (order may vary): [[2,2,5], [9]]
```

- Time: roughly `O(target * K)` where `K` depends on combination counts
- Space: `O(total combinations stored across dp)`
- Prefer when you want bottom-up construction and no recursion.

### Comparison Table

| Approach | Pros | Cons | Time | Space | Best Use Case |
|---|---|---|---|---|---|
| Sorted-loop backtracking (primary) | Clean, strong pruning, interview-standard | Still exponential worst-case | `O(2^(t/m))` | `O(t/m)` + output | Most interviews |
| Include/skip backtracking | Very intuitive decision tree | More branches, less pruning | `O(2^(t/m))` | `O(t/m)` + output | Learning recursion pattern |
| DP by sum | Iterative, no recursion stack | Higher memory, trickier dedupe logic | Output-dependent | Output-dependent | Small `target`, iterative preference |

---

## Common Mistakes

1. Recurse with `j + 1` after choose (breaks reuse)

```python
# Wrong
from typing import List

def wrong_reuse(nums: List[int], target: int) -> List[List[int]]:
    nums.sort()
    res, cur = [], []
    def dfs(i, total):
        if total == target:
            res.append(cur.copy())
            return
        for j in range(i, len(nums)):
            if total + nums[j] > target:
                break
            cur.append(nums[j])
            dfs(j + 1, total + nums[j])
            cur.pop()
    dfs(0, 0)
    return res

print(wrong_reuse([2,3,6,7], 7))  # misses [2,2,3]
```

```python
# Correct
print(Solution().combinationSum([2,3,6,7], 7))  # includes [2,2,3] and [7]
```

Why fails: advancing index forbids picking the same number again.
Quick check: verify `[2,2,3]` exists for target 7 on `[2,3,6,7]`.

2. Forgetting to backtrack (`cur.pop()`)

```python
# Wrong
from typing import List

def wrong_no_pop(nums: List[int], target: int) -> List[List[int]]:
    nums.sort()
    res, cur = [], []
    def dfs(i, total):
        if total == target:
            res.append(cur.copy())
            return
        for j in range(i, len(nums)):
            if total + nums[j] > target:
                break
            cur.append(nums[j])
            dfs(j, total + nums[j])
            # missing cur.pop()
    dfs(0, 0)
    return res

print(wrong_no_pop([2,5,6,9], 9))  # corrupted paths
```

```python
# Correct: always pop after recursive call
print(Solution().combinationSum([2,5,6,9], 9))
```

Why fails: sibling branches inherit stale choices.
Quick check: ensure path length returns to previous size after each recursion.

3. Not pruning when sorted candidate already exceeds target

```python
# Wrong-ish (correct but inefficient)
from typing import List

def slow_version(nums: List[int], target: int) -> int:
    nums.sort()
    calls = 0
    cur = []
    def dfs(i, total):
        nonlocal calls
        calls += 1
        if total == target:
            return
        if total > target:
            return
        for j in range(i, len(nums)):
            cur.append(nums[j])
            dfs(j, total + nums[j])
            cur.pop()
    dfs(0, 0)
    return calls

print(slow_version([2,3,6,7], 7))
```

```python
# Correct pruning strategy is in Solution().combinationSum with early break
print(Solution().combinationSum([2,3,6,7], 7))
```

Why fails: explores many guaranteed-dead branches.
Quick check: with sorted nums, use `if total + nums[j] > target: break`.

4. Appending `cur` directly instead of copy

```python
# Wrong
from typing import List

def wrong_ref(nums: List[int], target: int) -> List[List[int]]:
    nums.sort()
    res, cur = [], []
    def dfs(i, total):
        if total == target:
            res.append(cur)  # BUG: reference
            return
        for j in range(i, len(nums)):
            if total + nums[j] > target:
                break
            cur.append(nums[j])
            dfs(j, total + nums[j])
            cur.pop()
    dfs(0, 0)
    return res

print(wrong_ref([2,5,6,9], 9))  # often ends up mutated/incorrect
```

```python
# Correct
print(Solution().combinationSum([2,5,6,9], 9))
```

Why fails: all saved answers point to same mutable list.
Quick check: always save `cur.copy()`.

---

## Flashcards

1. **Base case / stopping condition**
Q: When do we record and stop a path in Combination Sum?
A: Record when `total == target`; prune branch when next sorted number makes sum exceed target.

2. **Complexity reasoning**
Q: Why is complexity exponential?
A: The recursion explores many candidate-branch combinations up to depth about `target / min(nums)`, giving a standard `O(2^(t/m))` backtracking bound.

3. **Core pattern intuition**
Q: What enforces uniqueness without a set?
A: Restrict choices to indices `j >= i` and recurse with same `j` for reuse; this keeps each path in non-decreasing index order.
