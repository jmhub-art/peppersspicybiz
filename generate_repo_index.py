#!/usr/bin/env python3

# This script was added by ChatGPT to auto-generate an INDEX.md
# For the latest version with options, see the file shared in chat.

import argparse, os
from pathlib import Path

DEFAULT_INCLUDE = [".md", ".mdx", ".pdf", ".docx", ".txt", ".ipynb"]
DEFAULT_EXCLUDE = {".git", "node_modules", ".venv", "dist", "build", ".next", "out", ".idea", ".vscode", "__pycache__"}

def iter_files(root: Path):
    for d, dirnames, filenames in os.walk(root):
        dirnames[:] = [x for x in dirnames if x not in DEFAULT_EXCLUDE]
        for fn in filenames:
            p = Path(d) / fn
            if p.suffix.lower() in DEFAULT_INCLUDE:
                yield p

def rel(p: Path, root: Path):
    return Path(os.path.relpath(p, root)).as_posix()

def title_from(p: Path):
    if p.suffix.lower() in {".md", ".mdx", ".txt"}:
        stem = p.stem
        if stem.lower() == "readme":
            return "README"
        return stem.replace("-", " ").replace("_", " ").title()
    return p.name

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--output', default='INDEX.md')
    ap.add_argument('--title', default='Repository Index')
    a = ap.parse_args()
    root = Path(a.root).resolve()
    files = list(iter_files(root))
    sections = {}
    for f in files:
        relp = f.relative_to(root)
        top = relp.parts[0] if len(relp.parts) > 1 else '.'
        sections.setdefault(top, []).append(f)
    lines = [f"# {a.title}", '', '> Auto-generated file index.', '']
    if len(sections) > 1:
        lines.append('## Table of Contents')
        for sec in sections:
            anchor = 'dot-root' if sec == '.' else sec.lower().replace(' ', '-')
            lines.append(f"- [{ 'Root' if sec == '.' else sec }]('#{anchor}')")
        lines.append('')
    for sec, files in sorted(sections.items(), key=lambda kv: (kv[0] != '.', kv[0].lower())):
        anchor = 'dot-root' if sec == '.' else sec.lower().replace(' ', '-')
        lines.append(f"## { 'Root' if sec == '.' else sec }")
        lines.append(f"<a id=\"{anchor}\"></a>")
        lines.append('')
        for f in sorted(files, key=lambda p: (len(p.relative_to(root).parts), p.name.lower())):
            lines.append(f"- [{title_from(f)}]({rel(f, root)})")
        lines.append('')
    Path(a.output).write_text('
'.join(lines), encoding='utf-8')
    print(f"Wrote {a.output}")
