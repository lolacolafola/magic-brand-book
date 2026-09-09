# Brand book tooling

`brandbook.html` at the repo root is the source of truth. `index.html` is generated from it.

## The one-writer rule

**Nobody edits `index.html`.** Edit `brandbook.html`, then run the build. Two writers on the generated file is what caused the last mess, and git will not warn you: the diff looks clean either way.

## Build

```
python3 tools/build.py                      # writes index.html beside brandbook.html
python3 tools/build.py site/index.html      # writes it somewhere else
```

Pass the path that GitHub Pages serves. The build runs both checks first and refuses to write if either fails.

`tools/_head.html` is the doctype, meta, favicon and reset that the Claude artifact platform adds automatically at publish time. The build adds the same thing so the hosted page and the artifact stay identical. Do not edit it unless the artifact wrapper changes.

## Changing the version

**Every change to `brandbook.html` bumps the version.** Nothing else in the process will remind you, and the drift is invisible: the footer read 4.4 across the source, the working copy and the last commit while the register recorded 4.8. Four versions of edits with no way to date any of them.

```
# edit VERSION, then:
python3 tools/version.py --set
python3 tools/build.py
```

`VERSION` at the repo root is the only place the number lives. `--set` writes it into the footer of `brandbook.html` and into the version line of `tools/sources.txt`, because a bumped version is a new number in the book and an unsourced number fails the claims check.

`tools/version.py --check` compares the two and exits 1 on a mismatch. The build runs it before anything else and refuses to write `index.html` if they disagree.

## The three checks

```
python3 tools/version.py --check
python3 tools/brandlint.py brandbook.html
python3 tools/claims.py brandbook.html tools/sources.txt
```

**version.py** checks that the book states its own version correctly. See above.

**brandlint.py** checks how it is written. Deterministic pattern matching, no model judgement. Exit 1 on errors: em dashes, negation-contrast forms, <!--lint-skip-->the mascot called a ghost<!--/lint-skip-->, Magic positioned as AI to fans or artists, Magic owning the universe. Warnings for hedging adverbs, announcing openers, trailing participles, vague scale claims. It also computes per-paragraph sentence-length variation and flags summarising closes.

Mark a region that quotes a banned form on purpose with `class="lint-skip"` in HTML, or wrap it in `<!--lint-skip-->` and `<!--/lint-skip-->` in markdown. The mascot line above uses the second form.

**claims.py** checks whether it is true. Every factual claim needs a line in `tools/sources.txt`. A new number with no source line fails the build. This exists because three invented numbers shipped before anyone caught them.

`sources.txt` groups claims four ways: verifiable in a file, from Magic's own documents, borrowed from an external brand book and needing Magic's adoption, and written by Claude with no external source. **"No source, needs adoption" is an honest entry. Silence is not.**

## What the checks do not catch

All three read syntax. Four fault types get past them:

1. **The overstated absolute.** A true narrow point with "and never" added for weight.
2. **The internal contradiction.** A rule written above a table that breaks it.
3. **Literary jargon.** Parses perfectly, means nothing to a reader.
4. **Invention inside the tooling.** The linter's own advice string once named the mascot "Lumi". Nobody has named the mascot. The script that exists to stop invented content carried invented content in the one place nothing checks.

Read the tooling as well as the work the tooling checks.

## Adding a rule

Every rule needs a failure in view. Either one that has happened, or one a real person would plausibly commit. "Do not add gradients" is valid because an agency would. "No countdown to something that is not happening" was cut because nobody would.

If the "wrong" column of an example pair reads better than the "right" column, the rule is wrong.
