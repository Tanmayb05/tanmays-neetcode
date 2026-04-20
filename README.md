# NeetCode Guide Generator

Generate interactive HTML learning guides from markdown problem notes.

## Project Layout

- `content/problems/`: markdown source files
- `site/problems/`: generated HTML files
- `templates/`: shared HTML templates
- `tools/`: generator and validation scripts
- `docs/`: framework + reference docs
- `examples/context/`: sample context files

```text
.
├── content/
│   └── problems/
├── site/
│   └── problems/
├── templates/
├── tools/
├── docs/
├── examples/
│   └── context/
├── index.html
├── Makefile
└── README.md
```

## Quick Start

```bash
make generate-one CONTEXT=content/problems/lc-39-combination-sum.md
make generate-all
make check-structure
```

## Notes

- Naming convention: `lc-{number}-{slug}.md` and `lc-{number}-{slug}.html`
