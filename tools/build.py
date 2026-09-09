#!/usr/bin/env python3
"""
Build site/index.html from brandbook.html.

brandbook.html is the source of truth. It is the file published as the Claude
artifact, so it carries no doctype, no <head> and no <body>: the artifact
platform wraps it at publish time. This script does the same wrapping for
GitHub Pages, so the two stay identical.

    python3 tools/build.py                      writes index.html beside brandbook.html
    python3 tools/build.py site/index.html      writes it somewhere else

Nobody edits index.html by hand. Edit brandbook.html and rebuild.
Two writers on that file is what caused the last mess.
"""

import os
import sys
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "brandbook.html")
HEAD = os.path.join(ROOT, "tools", "_head.html")
DEFAULT_OUT = os.path.join(ROOT, "index.html")

OPEN_BODY = "</style>\n\n<div class=\"wrap\">"
OPEN_BODY_OUT = "</style>\n</head>\n<body>\n<div class=\"wrap\">"
CLOSE = "</body>\n</html>\n"


def build(out):
    src = open(SRC, encoding="utf8").read()
    head = open(HEAD, encoding="utf8").read()
    if OPEN_BODY not in src:
        sys.exit("Cannot find the body opening in brandbook.html. "
                 "Expected a blank line between </style> and <div class=\"wrap\">.")
    body = src.replace(OPEN_BODY, OPEN_BODY_OUT, 1)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    open(out, "w", encoding="utf8").write(head + body + CLOSE)
    return len(head + body + CLOSE)


def gate():
    """Run every check against the source. Refuse to build on failure."""
    checks = [
        ["python3", os.path.join(ROOT, "tools", "version.py"), "--check"],
        ["python3", os.path.join(ROOT, "tools", "brandlint.py"), SRC],
        ["python3", os.path.join(ROOT, "tools", "claims.py"), SRC,
         os.path.join(ROOT, "tools", "sources.txt")],
    ]
    for cmd in checks:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 1:
            print(r.stdout)
            sys.exit(f"BUILD BLOCKED by {os.path.basename(cmd[1])}. Fix the source and run again.")
        print(f"  {os.path.basename(cmd[1])}: pass")


if __name__ == "__main__":
    print("\nChecking brandbook.html")
    gate()
    out = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT
    n = build(out)
    print(f"\n  Wrote {os.path.relpath(out, ROOT)}, {n:,} bytes\n")
