# Reusable HTML Framework for NeetCode Guides

This framework lets you generate a new `html/lc-...html` page from a markdown context file.

## Files Added

- `templates/problem-guide.template.html`
  - Shared reusable page shell (style + nav + sections + progress bar).
- `scripts/generate_problem_html.py`
  - Generator that converts markdown context into the HTML shell.

## Context Format

Use your existing pattern in `md/*.md`:

1. First line as title:

```md
# Problem Name
```

2. Optional front matter block:

```md
---
problem_name: Problem Name
platform: LeetCode / NeetCode
difficulty: Medium
pattern: Backtracking
primary_tags:
  - Backtracking
  - DFS
status: Not Started
last_updated: 2026-04-20
---
```

3. Main content split by `##` headings. Each `##` becomes a separate tab in HTML.

## Generate One HTML

```bash
python3 scripts/generate_problem_html.py --context md/lc-39-combination-sum.md
```

This writes:

- `html/lc-39-combination-sum.html`

You can also pass a custom output path:

```bash
python3 scripts/generate_problem_html.py \
  --context md/lc-39-combination-sum.md \
  --out html/custom-name.html
```

## Workflow for New Problems

1. Create a new markdown context file in `md/`:
   - Example: `md/lc-46-permutations.md`
2. Fill the content with your structure (`## Problem Statement`, `## Core Concepts`, etc.).
3. Run:

```bash
python3 scripts/generate_problem_html.py --context md/lc-46-permutations.md
```

4. Open generated file in `html/`.

## Generate All Existing Context Files

```bash
python3 scripts/generate_problem_html.py --all-md
```

This scans `md/*.md` and writes matching `html/*.html` files.

## Notes

- Markdown supported: `##/###/####` headings, lists, numbered lists, paragraphs, inline code, bold/italic, links, and fenced code blocks.
- If you want additional fixed tabs or interactive widgets later, extend the template and keep using the same context pipeline.
