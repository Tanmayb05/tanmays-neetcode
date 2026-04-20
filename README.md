# NeetCode Guides

## Project Layout

- `content/problems/`: markdown source files
- `site/problems/`: HTML files
- `templates/`: shared HTML templates
- `tools/`: validation scripts
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
make check-structure
```

## Notes

- Naming convention: `lc-{number}-{slug}.md` and `lc-{number}-{slug}.html`
