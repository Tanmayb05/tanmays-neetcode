# Project Conventions

## Directory Layout

- `content/problems/`: source markdown problem guides.
- `site/problems/`: HTML problem guides.
- `templates/`: reusable HTML templates.
- `tools/`: validation scripts.
- `docs/`: framework and reference documentation.
- `examples/context/`: sample context markdown files.

## Naming

- Markdown: `lc-{number}-{slug}.md`
- HTML: `lc-{number}-{slug}.html`
- Markdown and HTML stems should match exactly.

## Update Pipeline

1. Create or update markdown in `content/problems/`.
2. Create or update matching HTML in `site/problems/`.
3. Verify content and links in `site/problems/`.
4. Run structure validation before commit.

## Canonical Paths Only

Use only the directories above in commands, docs, and links. Avoid adding alias paths or duplicate directory names.
