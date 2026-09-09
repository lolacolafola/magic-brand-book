#!/usr/bin/env python3
"""
Magic claims check.

The linter catches how something is written. This catches whether it is true.

Every factual claim in the brand book must have a line in sources.txt naming
where it came from. A claim with no source line fails. That makes an invented
number impossible to ship quietly: writing a new one and not sourcing it
breaks the build.

    python3 claims.py brandbook.html sources.txt

Exit 0 = every claim sourced, 1 = unsourced claims found.
"""
import re, sys, html

NUM = r"(?:\d+(?:\.\d+)?\s*(?:%|px|pt|x|×)?|~\d+%)"

# Claim shapes worth forcing a source for.
PATTERNS = [
    ("quantity",   rf"\b{NUM}\b"),
    ("counted",    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirty)\b\s+\w+"),
    ("named as",   r"\bis called\b[^.]{0,40}"),
    ("attributed", r"\b(?:from the|according to|sourced to|published)\b[^.]{0,45}"),
]

STOPWORDS = re.compile(
    r"^(?:one|two|three|four)\s+(?:of|or|thing|things|idea|ideas|line|lines|"
    r"word|words|way|ways|more|other|others|per|and|in|at|to|for|is|are|"
    r"sentence|sentences|item|items|beat|beats|meaning|meanings|version|versions)\b",
    re.I)


def strip_markup(raw):
    t = re.sub(r"<style[^>]*>.*?</style>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<script[^>]*>.*?</script>", " ", t, flags=re.S | re.I)
    t = re.sub(r"data:[a-z/+-]+;base64,[A-Za-z0-9+/=]+", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    # Decode entities first, or emoji codepoints read as numeric claims.
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t)


def extract(text):
    claims = []
    seen = set()
    for kind, pat in PATTERNS:
        for m in re.finditer(pat, text, re.I):
            hit = m.group(0).strip()
            if STOPWORDS.match(hit):
                continue
            if re.match(r"^#?[0-9A-Fa-f]{6}$", hit):     # hex values
                continue
            start = max(0, m.start() - 70)
            ctx = text[start:m.end() + 50].strip()
            key = hit.lower()
            if key in seen:
                continue
            seen.add(key)
            claims.append((kind, hit, ctx))
    return claims


def load_sources(path):
    """sources.txt: 'claim | where it came from'. Blank lines and # ignored."""
    out = {}
    try:
        for line in open(path, encoding="utf8"):
            line = line.strip()
            if not line or line.startswith("#") or "|" not in line:
                continue
            claim, src = line.split("|", 1)
            out[claim.strip().lower()] = src.strip()
    except FileNotFoundError:
        pass
    return out


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 0
    text = strip_markup(open(sys.argv[1], encoding="utf8").read())
    sources = load_sources(sys.argv[2])
    claims = extract(text)

    sourced, unsourced = [], []
    for kind, hit, ctx in claims:
        if hit.lower() in sources:
            sourced.append((hit, sources[hit.lower()]))
        else:
            unsourced.append((kind, hit, ctx))

    print(f"\nMagic claims check: {sys.argv[1]}")
    print(f"{len(claims)} claims found, {len(sourced)} sourced, {len(unsourced)} unsourced\n")

    if sourced:
        print("=" * 64)
        print("SOURCED")
        print("=" * 64)
        for hit, src in sourced:
            print(f"  {hit:<22} {src}")

    if unsourced:
        print("\n" + "=" * 64)
        print("UNSOURCED  (add a line to sources.txt or remove the claim)")
        print("=" * 64)
        for kind, hit, ctx in unsourced:
            print(f"\n  [{kind}] {hit}")
            print(f"    ...{ctx}...")

    print(f"\n{len(unsourced)} unsourced claim(s)\n")
    return 1 if unsourced else 0


if __name__ == "__main__":
    sys.exit(main())
