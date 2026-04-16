# Problem Learning Guide - LLM Structure Specification

Use this document as the **single source of truth** for generating every future problem guide.
The goal is consistent depth, pedagogy, and section order across all problems.

## 1. Output Contract

- Output format: Markdown.
- Tone: clear, direct, educational, interview-focused.
- Audience: learners preparing for coding interviews.
- Section order: must exactly follow the order in this file.
- Every section must be present. If data is unknown, write `TBD` and state what is missing.
- Include at least one runnable solution in Python.
- Include time and space complexity for the main solution.
- Use consistent variable naming across all sections.

## 2. Required Frontmatter (Top of Every Problem)

Use this YAML block first:

```yaml
problem_name: <string>
platform: <LeetCode | NeetCode | etc>
difficulty: <Easy | Medium | Hard>
pattern: <e.g., Backtracking, Two Pointers, DP>
primary_tags:
  - <tag1>
  - <tag2>
status: <Not Started | In Progress | Mastered>
last_updated: <YYYY-MM-DD>
```

## 3. Canonical Section Template (Mandatory)

## Problem Statement

### Challenge
- Restate the problem in plain language.
- Clarify input and output.
- Clarify uniqueness/ordering constraints.

### Examples
- Provide at least 2 examples.
- Each example must contain:
  - Input
  - Output
  - Brief explanation of why output is correct

### Key Insight
- 1 short paragraph with the core intuition.
- Include any key counting formula (like `2^n`, `n!`, `n^2`, etc.) where relevant.

### Complexity Snapshot
- Main approach time complexity.
- Main approach space complexity.
- Any derived metric relevant to this problem (e.g., total states, recursion depth).

---

## Core Concepts

### Concept 1: Pattern Definition
- Define the core pattern for this problem.
- Explain why this pattern fits.

### Concept 2: Decision Process / State View
- Show how decisions are made at each step.
- If recursive: explain state as `(index, path, extra_state...)`.
- If iterative/DP: explain state transition.

### Concept 3: When to Use This Pattern
- 3-5 bullet triggers that suggest this pattern.
- 3-5 related problems.

### Important Caveat
- One warning box equivalent: most common conceptual mistake for this pattern.

---

## Step-by-Step Walkthrough

Break the primary solution into numbered steps (typically 5-8):

1. Initialize required data structures.
2. Define helper/recursive/iterative engine.
3. Define base case / stopping condition.
4. Apply first decision branch or transition.
5. Restore state if needed (backtrack/rollback).
6. Apply second branch/alternative transition.
7. Start execution.
8. Return final result.

For each step include:
- Mini code snippet.
- Why this step is needed.

### Complete Solution (Primary)
- Full Python code block.
- Must be runnable as-is.
- Use readable names (avoid one-letter names except loop indexes).

### Dry Run
- One complete dry run on a non-trivial input.
- Show key state changes line-by-line or step-by-step.

---

## Interactive Visualizer (Markdown-Compatible Spec)

Even if no UI is built, provide a visualizer spec so future tooling can consume it.

### Visualizer Input
- Input format and sample input.

### State Fields to Track
- Current index/pointer/state ID.
- Current path/subset/window/buffer.
- Current action.
- Current result count / best value.

### Step Events
- Define event types (e.g., `include`, `exclude`, `backtrack`, `update_best`).
- Define what changes in state for each event.

### Tree / Graph / Table Representation
- State what structure should be rendered.

---

## Knowledge Check (Quiz)

- Provide exactly 4 multiple-choice questions.
- Each question must have 4 options (A-D).
- Exactly 1 correct answer per question.
- Include explanation for each answer.
- Coverage requirements:
  - 1 question on complexity
  - 1 on correctness invariant
  - 1 on edge case
  - 1 on implementation pitfall

---

## Code Playground

### Starter Code
- Provide editable starter Python code.
- Include one default test case.

### Suggested Experiments
- Provide 3 challenges:
  1. Constraint variant (e.g., size `k`, duplicates, bounded sum)
  2. Alternative paradigm (iterative vs recursive, memoized vs tabulated)
  3. Optimization or proof task

---

## Alternative Approaches

Provide at least 2 alternatives.

For each alternative include:
- Short intuition.
- Python code snippet.
- Time complexity.
- Space complexity.
- When to prefer it.

### Comparison Table
Columns:
- Approach
- Pros
- Cons
- Time
- Space
- Best Use Case

---

## Common Mistakes

Provide exactly 4 mistakes.

For each mistake include:
- Mistake title.
- Wrong snippet.
- Correct snippet.
- Why the wrong version fails.
- Quick check to avoid it.

---

## Flashcards

Provide exactly 3 flashcards:
- Card 1: base case / stopping condition
- Card 2: complexity reasoning
- Card 3: core pattern intuition

Format each as:
- Front (question)
- Back (concise answer)

---

## Quick Reference

### Template Code
- Minimal reusable template for this pattern.
- Should be copy-ready.

### Pattern Mnemonic
- One-line execution mnemonic (example format: `Initialize -> Recurse -> Backtrack -> Return`).

### Key Metrics
- Number of key steps.
- Dominant growth term.
- Max recursion depth / memory driver.

---

## Next Steps

### Next Challenges
- 4 related problems ordered easy -> hard.

### Study Tips
- 4 concrete review actions.
- Include spaced repetition schedule recommendation.

---

## 4. Quality Gate Checklist (Must Pass)

Before finalizing any new problem guide, verify:

- All mandatory sections exist and in correct order.
- Primary solution is correct and runnable.
- Complexity claims match implementation.
- Examples are valid and internally consistent.
- Dry run is complete and coherent.
- Quiz has 4 questions with explanations.
- Mistakes section has 4 items with wrong/correct code.
- Flashcards section has exactly 3 cards.
- Alternatives include at least 2 approaches.
- Next steps include 4 problems and 4 study tips.

## 5. Reusable Skeleton (Copy/Paste)

```text
# <Problem Name>

---
problem_name: <...>
platform: <...>
difficulty: <...>
pattern: <...>
primary_tags:
  - <...>
status: <...>
last_updated: <YYYY-MM-DD>
---

## Problem Statement
### Challenge
...
### Examples
#### Example 1
Input: ...
Output: ...
Explanation: ...
#### Example 2
Input: ...
Output: ...
Explanation: ...
### Key Insight
...
### Complexity Snapshot
- Time: ...
- Space: ...
- Extra Metric: ...

## Core Concepts
### Concept 1: Pattern Definition
...
### Concept 2: Decision Process / State View
...
### Concept 3: When to Use This Pattern
...
### Important Caveat
...

## Step-by-Step Walkthrough
1. ...
2. ...
3. ...
4. ...
5. ...
### Complete Solution (Primary)
[python code block here]
### Dry Run
...

## Interactive Visualizer (Markdown-Compatible Spec)
### Visualizer Input
...
### State Fields to Track
...
### Step Events
...
### Tree / Graph / Table Representation
...

## Knowledge Check (Quiz)
### Q1
...
### Q2
...
### Q3
...
### Q4
...

## Code Playground
### Starter Code
[python code block here]
### Suggested Experiments
1. ...
2. ...
3. ...

## Alternative Approaches
### Alternative 1
...
### Alternative 2
...
### Comparison Table
| Approach | Pros | Cons | Time | Space | Best Use Case |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## Common Mistakes
### Mistake 1
Wrong:
[python code block here]
Correct:
[python code block here]
...

## Flashcards
### Card 1
Front: ...
Back: ...
### Card 2
Front: ...
Back: ...
### Card 3
Front: ...
Back: ...

## Quick Reference
### Template Code
[python code block here]
### Pattern Mnemonic
...
### Key Metrics
- ...

## Next Steps
### Next Challenges
1. ...
2. ...
3. ...
4. ...
### Study Tips
1. ...
2. ...
3. ...
4. ...
```

## 6. Notes for Future LLM Runs

- Keep explanations short per section but complete across the full guide.
- Prefer correctness and consistency over stylistic variation.
- If the problem has multiple valid patterns, pick one as primary and clearly mark others as alternatives.
- Never skip dry run, mistakes, or quiz sections.
