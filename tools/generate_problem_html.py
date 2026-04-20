#!/usr/bin/env python3
"""Generate reusable NeetCode problem HTML from context markdown.

Usage:
  python3 tools/generate_problem_html.py --context content/problems/lc-39-combination-sum.md
  python3 tools/generate_problem_html.py --context content/problems/lc-39-combination-sum.md --out site/problems/lc-39-combination-sum.html
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "templates" / "problem-guide.template.html"
DEFAULT_CONTENT_DIR = ROOT / "content" / "problems"
DEFAULT_OUTPUT_DIR = ROOT / "site" / "problems"


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "section"


def parse_front_matter(raw: str) -> Tuple[Dict[str, str], str]:
    lines = raw.splitlines()
    if len(lines) < 3:
        return {}, raw

    # The existing files use:
    # # Title
    #
    # ---
    # key: value
    # ---
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if start is None:
                start = i
            else:
                end = i
                break

    if start is None or end is None or end <= start:
        return {}, raw

    meta: Dict[str, str] = {}
    cur_key = None
    cur_list: List[str] = []

    for line in lines[start + 1 : end]:
        if not line.strip():
            continue

        if re.match(r"^\s*-\s+", line) and cur_key:
            cur_list.append(line.strip()[2:].strip())
            continue

        if ":" in line:
            if cur_key and cur_list:
                meta[cur_key] = ", ".join(cur_list)
                cur_list = []

            k, v = line.split(":", 1)
            cur_key = k.strip()
            val = v.strip()
            if val:
                meta[cur_key] = val
                cur_key = None
            else:
                # list key starts here
                meta[cur_key] = ""
        elif cur_key and cur_list:
            meta[cur_key] = ", ".join(cur_list)
            cur_key = None
            cur_list = []

    if cur_key and cur_list:
        meta[cur_key] = ", ".join(cur_list)

    body = "\n".join(lines[:start] + lines[end + 1 :]).strip()
    return meta, body


def extract_title(body: str) -> Tuple[str, str]:
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        return title, "\n".join(lines[1:]).strip()
    return "Problem Guide", body


def split_sections(body: str) -> List[Tuple[str, str]]:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE))
    if not matches:
        return [("Notes", body)]

    sections: List[Tuple[str, str]] = []
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        sections.append((title, content))
    return sections


def convert_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',
        text,
    )
    return text


def markdown_to_html(md: str) -> str:
    out: List[str] = []
    lines = md.splitlines()
    i = 0

    in_code = False
    code_lang = ""
    code_buf: List[str] = []

    in_ul = False
    in_ol = False
    paragraph_buf: List[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_buf
        if paragraph_buf:
            text = " ".join(s.strip() for s in paragraph_buf if s.strip())
            if text:
                out.append(f"<p>{convert_inline(text)}</p>")
            paragraph_buf = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if in_code:
            if stripped.startswith("```"):
                code = "\n".join(code_buf)
                lang_cls = f" class=\"language-{html.escape(code_lang)}\"" if code_lang else ""
                out.append(f"<pre><code{lang_cls}>{html.escape(code)}</code></pre>")
                in_code = False
                code_lang = ""
                code_buf = []
            else:
                code_buf.append(line)
            i += 1
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            close_lists()
            in_code = True
            code_lang = stripped[3:].strip()
            i += 1
            continue

        if not stripped:
            flush_paragraph()
            close_lists()
            i += 1
            continue

        if stripped == "---":
            flush_paragraph()
            close_lists()
            out.append("<hr />")
            i += 1
            continue

        h3 = re.match(r"^###\s+(.+)$", stripped)
        h4 = re.match(r"^####\s+(.+)$", stripped)
        ol = re.match(r"^(\d+)\.\s+(.+)$", stripped)
        ul = re.match(r"^-\s+(.+)$", stripped)

        if h4:
            flush_paragraph()
            close_lists()
            out.append(f"<h4>{convert_inline(h4.group(1))}</h4>")
            i += 1
            continue

        if h3:
            flush_paragraph()
            close_lists()
            out.append(f"<h3>{convert_inline(h3.group(1))}</h3>")
            i += 1
            continue

        if ul:
            flush_paragraph()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{convert_inline(ul.group(1))}</li>")
            i += 1
            continue

        if ol:
            flush_paragraph()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{convert_inline(ol.group(2))}</li>")
            i += 1
            continue

        paragraph_buf.append(line)
        i += 1

    flush_paragraph()
    close_lists()

    if in_code:
        code = "\n".join(code_buf)
        out.append(f"<pre><code>{html.escape(code)}</code></pre>")

    return "\n".join(out)


def render(template: str, replacements: Dict[str, str]) -> str:
    for key, value in replacements.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def build_nav_and_sections(sections: List[Tuple[str, str]]) -> Tuple[str, str]:
    nav_items = [
        '<li><button class="nav-tab-link" data-section="overview">Overview</button></li>'
    ]
    section_html_parts: List[str] = []

    seen_ids = {"overview"}

    for title, md in sections:
        sid = slugify(title)
        base_sid = sid
        idx = 2
        while sid in seen_ids:
            sid = f"{base_sid}-{idx}"
            idx += 1
        seen_ids.add(sid)

        nav_items.append(
            f'<li><button class="nav-tab-link" data-section="{sid}">{html.escape(title)}</button></li>'
        )

        content_html = markdown_to_html(md)
        section_html_parts.append(
            "\n".join(
                [
                    f'<section id="{sid}" class="section">',
                    f'  <h2 class="section-title">{html.escape(title)}</h2>',
                    '  <div class="card">',
                    f"{content_html}",
                    '  </div>',
                    '</section>',
                ]
            )
        )

    return "\n".join(nav_items), "\n\n".join(section_html_parts)


def meta_pills(meta: Dict[str, str]) -> str:
    order = [
        "platform",
        "difficulty",
        "pattern",
        "primary_tags",
        "status",
        "last_updated",
    ]

    pills: List[str] = []
    for key in order:
        value = meta.get(key)
        if value:
            label = key.replace("_", " ").title()
            pills.append(
                f'<div class="meta-pill"><strong>{html.escape(label)}:</strong> {html.escape(value)}</div>'
            )

    if not pills:
        pills.append('<div class="meta-pill"><strong>Meta:</strong> No front matter provided.</div>')

    return "\n".join(pills)


def guess_output_path(context_path: Path) -> Path:
    stem = context_path.stem
    return DEFAULT_OUTPUT_DIR / f"{stem}.html"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reusable HTML from markdown context")
    parser.add_argument("--context", help="Path to markdown context file")
    parser.add_argument(
        "--all-md",
        action="store_true",
        help="Generate HTML for all markdown files under content/problems/",
    )
    parser.add_argument("--out", help="Optional output HTML path")
    parser.add_argument(
        "--template",
        default=str(DEFAULT_TEMPLATE),
        help="Template HTML path",
    )
    args = parser.parse_args()

    template_path = Path(args.template)
    if not template_path.is_absolute():
        template_path = (ROOT / template_path).resolve()

    if not template_path.exists():
        raise SystemExit(f"Template file not found: {template_path}")

    if args.all_md and args.out:
        raise SystemExit("--out is not supported with --all-md")
    if not args.all_md and not args.context:
        raise SystemExit("Either --context or --all-md is required")

    if args.all_md:
        md_dir = DEFAULT_CONTENT_DIR
        if not md_dir.exists():
            raise SystemExit(f"Directory not found: {md_dir}")
        contexts = sorted(md_dir.glob("*.md"))
        if not contexts:
            raise SystemExit(f"No markdown files found in: {md_dir}")
    else:
        context_path = Path(args.context)
        if not context_path.is_absolute():
            context_path = (ROOT / context_path).resolve()
        if not context_path.exists():
            raise SystemExit(f"Context file not found: {context_path}")
        contexts = [context_path]

    template = template_path.read_text(encoding="utf-8")
    generated = 0

    for context_path in contexts:
        out_path = (
            Path(args.out).resolve()
            if args.out
            else guess_output_path(context_path)
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)

        raw = context_path.read_text(encoding="utf-8")
        meta, body = parse_front_matter(raw)
        title, body = extract_title(body)
        sections = split_sections(body)
        nav_html, sections_html = build_nav_and_sections(sections)

        difficulty = meta.get("difficulty", "Unknown")
        tagline = f"Pattern: {meta.get('pattern', 'General')} | Platform: {meta.get('platform', 'NeetCode')}"

        page_title = f"{title} - Backtracking Learning Guide"
        replacements = {
            "PAGE_TITLE": html.escape(page_title),
            "PROBLEM_TITLE": html.escape(title),
            "TAGLINE": html.escape(tagline),
            "DIFFICULTY": html.escape(difficulty),
            "NAV_ITEMS": nav_html,
            "META_PILLS": meta_pills(meta),
            "SOURCE_FILE": html.escape(str(context_path.relative_to(ROOT))),
            "SECTION_HTML": sections_html,
        }

        output = render(template, replacements)
        out_path.write_text(output, encoding="utf-8")
        generated += 1
        print(f"Generated: {out_path}")

    print(f"Done. Generated {generated} file(s).")


if __name__ == "__main__":
    main()
