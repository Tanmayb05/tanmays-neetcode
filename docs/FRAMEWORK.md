# Reusable HTML Framework for NeetCode Guides

This framework generates `lc-...` HTML pages from markdown context files using:

- `content/problems/` -> source markdown
- `templates/` -> reusable page shell
- `tools/` -> generator + checks
- `site/problems/` -> generated HTML output

## Core Files

- `templates/problem-guide.template.html`
  - Shared reusable page shell (style + nav + sections + progress bar).
- `tools/generate_problem_html.py`
  - Generator that converts markdown context into the HTML shell.
- `tools/check_structure.py`
  - Validates directories and naming conventions.
- `Makefile`
  - Short aliases for generation and validation.

## Context Format

Use this structure in `content/problems/*.md`:

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
make generate-one CONTEXT=content/problems/lc-39-combination-sum.md
```

This writes:

- `site/problems/lc-39-combination-sum.html`

You can also pass a custom output path:

```bash
python3 tools/generate_problem_html.py \
  --context content/problems/lc-39-combination-sum.md \
  --out site/problems/custom-name.html
```

## Workflow for New Problems

1. Create a new markdown context file in `content/problems/`:
   - Example: `content/problems/lc-46-permutations.md`
2. Fill the content with your structure (`## Problem Statement`, `## Core Concepts`, etc.).
3. Run:

```bash
make generate-one CONTEXT=content/problems/lc-46-permutations.md
```

4. Open generated file in `site/problems/`.

## Generate All Existing Context Files

```bash
make generate-all
```

This scans `content/problems/*.md` and writes matching `site/problems/*.html` files.

## Validate Project Structure

```bash
make check-structure
```

Checks:

- Required folders exist.
- Source/output naming follows `lc-{number}-{slug}.{md|html}`.
- Every source markdown has a matching generated HTML.

## Notes

- Markdown supported: `##/###/####` headings, lists, numbered lists, paragraphs, inline code, bold/italic, links, and fenced code blocks.
- If you want additional fixed tabs or interactive widgets later, extend the template and keep using the same context pipeline.
