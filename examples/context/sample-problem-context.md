# Sample Problem

---
problem_name: Sample Problem
platform: LeetCode / NeetCode
difficulty: Easy
pattern: Two Pointers
primary_tags:
  - Arrays
  - Two Pointers
status: In Progress
last_updated: 2026-04-20
---

## Problem Statement

### Challenge

Given an array of numbers, return whether a valid pair exists.

### Examples

- Input: `nums = [1, 2, 3], target = 4`
- Output: `True`

## Core Concepts

### Pattern Definition

Use two pointers from both ends after sorting.

```python
def has_pair(nums, target):
    nums.sort()
    i, j = 0, len(nums) - 1
    while i < j:
        s = nums[i] + nums[j]
        if s == target:
            return True
        if s < target:
            i += 1
        else:
            j -= 1
    return False
```

## Step-by-Step Walkthrough

1. Sort the array.
2. Initialize pointers.
3. Move pointer based on current sum.

## Mistakes

- Forgetting to sort before applying two pointers.
- Moving both pointers at once.

## Next Steps

- Solve 3Sum.
- Solve Container With Most Water.
