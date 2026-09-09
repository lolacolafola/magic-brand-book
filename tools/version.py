#!/usr/bin/env python3
"""
Magic brand book version stamp.

The book's footer states its own version. Nothing used to check that the
stated version was the real one, and it drifted: the footer read 4.4 while
the register recorded 4.8, across the source, the working copy and the last
commit. Nobody could date a finding against it.

VERSION at the repo root is now the only place the number lives.

    python3 tools/version.py --check     compare the footer to VERSION
    python3 tools/version.py --set       rewrite the footer from VERSION
    python3 tools/version.py             print the current version

Exit 0 = the footer matches VERSION, 1 = it does not.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "brandbook.html")
VERSION_FILE = os.path.join(ROOT, "VERSION")
SOURCES = os.path.join(ROOT, "tools", "sources.txt")

# The line in sources.txt that sources the book's own version number.
SOURCE_TAG = "this document's own version"

STAMP = re.compile(r"(Magic Brand Book\s*·\s*version\s+)([0-9.]+)(\s*·\s*)([^.<]+?)(\.\s*Where)")


def read_version():
    fields = {}
    for line in open(VERSION_FILE, encoding="utf8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        fields[k.strip()] = v.strip()
    for key in ("version", "date"):
        if key not in fields:
            sys.exit(f"VERSION is missing a '{key}' line.")
    return fields["version"], fields["date"]


def read_stamp():
    src = open(SRC, encoding="utf8").read()
    m = STAMP.search(src)
    if not m:
        sys.exit("No version footer found in brandbook.html. "
                 "Expected 'Magic Brand Book · version N · DATE. Where...'")
    return src, m


def set_source_line(version):
    """Keep sources.txt's own-version line in step. A bumped version is a new
    number in the book, and an unsourced number fails the claims check."""
    lines = open(SOURCES, encoding="utf8").read().splitlines(True)
    for i, line in enumerate(lines):
        if SOURCE_TAG in line and "|" in line and not line.lstrip().startswith("#"):
            lines[i] = f"{version:<18} | {SOURCE_TAG}\n"
            open(SOURCES, "w", encoding="utf8").writelines(lines)
            return True
    return False


def main():
    want_v, want_d = read_version()
    src, m = read_stamp()
    got_v, got_d = m.group(2), m.group(4).strip()
    arg = sys.argv[1] if len(sys.argv) > 1 else "--check"

    if arg == "--set":
        new = src[:m.start()] + m.group(1) + want_v + m.group(3) + want_d + m.group(5) + src[m.end():]
        open(SRC, "w", encoding="utf8").write(new)
        print(f"  brandbook.html footer set to {want_v} · {want_d}")
        if set_source_line(want_v):
            print(f"  sources.txt version line set to {want_v}")
        else:
            print(f"  WARNING: no line in sources.txt reading '{SOURCE_TAG}'.")
            print("  The claims check will fail on the new version number.")
        print("  Rebuild so index.html carries it too: python3 tools/build.py")
        return 0

    if arg == "--check":
        if (got_v, got_d) == (want_v, want_d):
            print(f"  version: {got_v} · {got_d}")
            return 0
        print(f"\n  VERSION says      {want_v} · {want_d}")
        print(f"  brandbook.html says {got_v} · {got_d}")
        print("\n  The book cannot state its own version correctly, so nothing")
        print("  checked against it can be dated. Decide which is right, edit")
        print("  VERSION, then run: python3 tools/version.py --set\n")
        return 1

    print(f"{got_v} · {got_d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
