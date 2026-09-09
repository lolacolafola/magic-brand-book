#!/usr/bin/env python3
"""
Magic brand linter.

Checks any text or HTML against the Magic brand book's writing rules.
Deterministic. No model judgement involved: a pattern either matches or it does not.

    python3 brandlint.py draft.md
    python3 brandlint.py brandbook.html
    cat something.txt | python3 brandlint.py -

Exit code 0 = clean, 1 = errors found, 2 = warnings only.
"""

import re
import sys
import statistics

# ----------------------------------------------------------------------------
# ERRORS. Banned outright by the brand book. No exceptions in normal copy.
# ----------------------------------------------------------------------------

ERRORS = [
    ("em dash",
     r"—|&mdash;",
     "The number one AI tell. Use a full stop, a comma or a colon."),

    ("en dash in prose",
     r"(?<=[a-zA-Z])\s–\s(?=[a-zA-Z])",
     "Same problem as the em dash. Rewrite the sentence."),

    ("negation-contrast: rather than",
     r"\brather than\b",
     "Banned construction. Delete the rejected half and state the thing."),

    ("negation-contrast: instead of",
     r"\binstead of\b",
     "Same shape as 'rather than'. State the thing itself."),

    ("negation-contrast: X, not Y",
     r",\s+not\s+(?:a|an|the|just|only|because|from|what|who|how|where)\b",
     "Banned construction. Delete the rejected half."),

    ("negation-contrast: not just X but Y",
     r"\bnot (?:just|only|merely)\b[^.!?]{0,60}\bbut\b",
     "Banned construction. Say what it is."),

    ("negation-contrast: it isn't A, it's B",
     r"\b(?:isn't|is not|aren't|are not|wasn't|it's not)\b[^.!?]{0,50}[.!?]\s+(?:It's|It is|They're|They are|That's)\b",
     "Banned construction. Delete the rejected half."),

    ("negation-contrast: before it is",
     r"\bbefore it is\b",
     "Banned construction."),

    ("mascot called a ghost",
     r"\bghosts?\b",
     "Never call the character a ghost. It is the Magic mascot until it has a name."),

    ("Magic positioned as AI",
     r"\bAI[- ](?:powered|driven|first|native|enabled)\b|\bour AI\b|\bAI (?:platform|company|companion|assistant|technology)\b|\bpowered by (?:AI|Magic Brain)\b",
     "Magic is never positioned as an AI company or platform to fans, artists or their teams. Say what it does."),

    ("Magic owns the universe",
     r"\b(?:the Magic universe|our universe|join the (?:Magic )?universe|welcome to (?:the|our))\b",
     "A Fanverse is built for its fans. Write 'your universe', 'your Fanverses'."),
]

# ----------------------------------------------------------------------------
# WARNINGS. Judgement needed, but each one is a known AI cadence.
# ----------------------------------------------------------------------------

WARNINGS = [
    ("hedging adverb",
     r"\b(?:genuinely|truly|simply|actually|incredibly|seamlessly|effortlessly|remarkably|undoubtedly)\b",
     "Cut the word. The sentence is stronger without it."),

    ("announcing opener",
     r"(?:^|[.!?]\s+)(?:Here's the thing|Let's be clear|The truth is|What's more|At the end of the day|It's worth noting)\b",
     "Start with the thing itself."),

    ("trailing participle",
     r",\s+(?:making|ensuring|allowing|enabling|helping|creating|delivering|providing|driving)\s+\w+",
     "A new sentence, or nothing."),

    ("empty intensifier pair",
     r"\b(?:more|less)\s+\w+,?\s+and\s+(?:more|less)\s+\w+\b",
     "Reads as generated cadence. Name the specific change."),

    ("vague scale claim",
     r"\b(?:a wide range of|a variety of|countless|myriad|a host of|numerous)\b",
     "Give the number or name the things."),

    ("three-item rise",
     r"\b(\w+ly|\w+er|\w+est),\s+(\w+ly|\w+er|\w+est),?\s+and\s+(\w+ly|\w+er|\w+est)\b",
     "Three parallel items is a machine cadence. Use two, or four."),
]


def strip_markup(raw: str) -> str:
    """Remove CSS, base64 payloads, tags and entities. Keep readable prose."""
    # Regions the book marks as deliberate examples of a banned form.
    t = re.sub(r'<[^>]*\bclass="[^"]*\blint-skip\b[^"]*"[^>]*>.*?</\w+>', " ", raw, flags=re.S | re.I)
    t = re.sub(r"<!--lint-skip-->.*?<!--/lint-skip-->", " ", t, flags=re.S | re.I)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<script[^>]*>.*?</script>", " ", t, flags=re.S | re.I)
    t = re.sub(r"data:[a-z/+-]+;base64,[A-Za-z0-9+/=]+", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = (t.replace("&rsquo;", "'").replace("&lsquo;", "'")
          .replace("&ldquo;", '"').replace("&rdquo;", '"')
          .replace("&quot;", '"').replace("&amp;", "&").replace("&nbsp;", " "))
    return t


def sentences(text: str):
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def check_patterns(text: str, rules, label: str):
    found = []
    for name, pattern, advice in rules:
        for m in re.finditer(pattern, text, re.I):
            start = max(0, m.start() - 60)
            snippet = re.sub(r"\s+", " ", text[start:m.end() + 60]).strip()
            found.append((label, name, m.group(0)[:40], snippet, advice))
    return found


def check_rhythm(text: str):
    """Uniform sentence length is the deepest tell. Flag paragraphs that never vary."""
    flags = []
    for para in re.split(r"\n\s*\n", text):
        sents = sentences(para)
        if len(sents) < 4:
            continue
        lengths = [len(s.split()) for s in sents]
        if statistics.mean(lengths) == 0:
            continue
        cv = statistics.pstdev(lengths) / statistics.mean(lengths)
        if cv < 0.30 and min(lengths) > 8:
            flags.append((
                "RHYTHM", "uniform sentence length",
                f"{len(sents)} sentences, {min(lengths)}-{max(lengths)} words",
                re.sub(r"\s+", " ", para)[:130],
                "Vary hard. Put a four-word sentence next to a thirty-word one."))
    return flags


def check_closers(raw: str):
    """
    The summarising close. Last sentence of a section that states no fact
    and gives no instruction: no digit, no proper noun, no imperative.
    """
    IMPERATIVES = (
        "write", "use", "never", "always", "cut", "keep", "put", "read", "check",
        "start", "stop", "pick", "hold", "name", "say", "lead", "avoid", "treat",
        "give", "make", "set", "follow", "ask", "flag", "delete", "run", "add")
    flags = []
    blocks = re.split(r"(?=<h[123])|(?=</section>)|(?=</div>)", raw)
    seen = set()
    for blk in blocks:
        paras = re.findall(r"<p[^>]*>(.*?)</p>", blk, re.S)
        if not paras:
            continue
        last = strip_markup(paras[-1]).strip()
        last = re.sub(r"\s+", " ", last)
        if not (30 < len(last) < 400):
            continue
        final = sentences(last)[-1] if sentences(last) else ""
        if not final or final in seen:
            continue
        seen.add(final)
        has_digit = bool(re.search(r"\d", final))
        has_proper = bool(re.search(r"(?<!^)(?<![.!?] )\b[A-Z][a-z]{2,}", final))
        first = final.split()[0].lower().strip('"') if final.split() else ""
        has_imperative = first in IMPERATIVES
        # A flourish is abstract as well as factless: it talks about the idea
        # instead of naming anything a reader can act on.
        ABSTRACT = r"\b(?:the (?:whole )?(?:idea|point|thing|reason|difference|answer)|what makes|which is why|that is why|all along|from the start|worth saying|the same idea|says it all|matters most|comes down to)\b"
        is_abstract = bool(re.search(ABSTRACT, final, re.I))
        if not (has_digit or has_proper or has_imperative) and is_abstract:
            flags.append((
                "CLOSER", "possible summarising close", final[:70], final[:160],
                "If it states no fact and gives no instruction, cut it."))
    return flags


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    src = sys.argv[1]
    raw = sys.stdin.read() if src == "-" else open(src, encoding="utf8").read()
    text = strip_markup(raw)

    results = []
    results += check_patterns(text, ERRORS, "ERROR")
    results += check_patterns(text, WARNINGS, "WARN")
    results += check_rhythm(text)
    results += check_closers(raw)

    order = {"ERROR": 0, "WARN": 1, "RHYTHM": 2, "CLOSER": 3}
    results.sort(key=lambda r: order.get(r[0], 9))

    errors = [r for r in results if r[0] == "ERROR"]
    others = [r for r in results if r[0] != "ERROR"]

    print(f"\nMagic brand lint: {src}")
    print(f"{len(text.split()):,} words checked\n")

    if not results:
        print("  Clean. Nothing to fix.\n")
        return 0

    current = None
    for level, name, hit, snippet, advice in results:
        if level != current:
            print(f"\n{'=' * 62}\n{level}\n{'=' * 62}")
            current = level
        print(f"\n  [{name}]  \"{hit}\"")
        print(f"    ...{snippet}...")
        print(f"    -> {advice}")

    print(f"\n{'=' * 62}")
    print(f"  {len(errors)} error(s), {len(others)} warning(s)\n")
    return 1 if errors else (2 if others else 0)


if __name__ == "__main__":
    sys.exit(main())
