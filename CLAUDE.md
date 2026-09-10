# Magic Brand Book

The working rules for how Magic sounds, reads and looks. One self-contained page, no build framework, no dependencies.

Read this before touching anything in the repo.

## The one rule that has already been broken

**`index.html` is generated. Never edit it.** Edit `brandbook.html` and run the build.

Two writers on the generated file is what broke this repo before, and git will not warn you, because the diff looks clean either way. An em dash added by hand goes unnoticed until it turns up in a screenshot.

## Every change bumps the version

`VERSION` at the root is the only place the number lives.

```
# 1. edit brandbook.html
# 2. edit VERSION
python3 tools/version.py --set
python3 tools/build.py
```

`--set` writes the number into the footer of `brandbook.html` and into the version line of `tools/sources.txt`, because a bumped version is a new number in the book and an unsourced number fails the claims check.

Nothing else will remind you to do this. The footer once read 4.4 across the source, the working copy and the last commit while the register recorded 4.8.

## The three checks

`tools/build.py` runs all three and refuses to write `index.html` if any fails.

| Check | Fails on |
|---|---|
| `tools/version.py --check` | The book misstating its own version |
| `tools/brandlint.py` | Em dashes, negation-contrast, the banned mascot noun, Magic positioned as AI, Magic owning the universe |
| `tools/claims.py` | Any factual claim with no line in `tools/sources.txt` |

Run them on a draft as well as on the book:

```
python3 tools/brandlint.py FILE
python3 tools/claims.py FILE tools/sources.txt
```

Exit 1 means fix every error. Warnings need a judgement call and a reason to stay.

Mark text that quotes a banned form on purpose with `class="lint-skip"` in HTML, or between `<!--lint-skip-->` markers in markdown.

## The fourth check, which is not a script

Before anything is delivered, run a **book compliance review** as a subagent. It reads the whole book and the draft, and nothing else. It never sees the writer's reasoning, because a reviewer that watched the draft being written confirms the draft.

**Every finding quotes the book verbatim with its section, or it is deleted.** An invented brand rule enforced at scale is worse than no reviewer, because a writer will obey it and nobody will know where it came from.

Full prompt in the Brand Guardian plugin, skill `magic-book-compliance`.

On the first real job it found nine things across two rounds. The scripts found two.

## Writing rules

<!--lint-skip-->
- No em dashes anywhere.
- No negation-contrast: no "rather than", no "instead of", no "X, not a Y", no "it isn't A, it's B".
- No AI cadence. Vary sentence length hard.
- No literary jargon. Plain words a reader would use themselves.
- Sentence case everywhere. The tagline is the only thing in full caps.
<!--/lint-skip-->

**The tagline is LIVE IT. FOR REAL.** It is never rewritten. Both full stops stay. Never an exclamation mark.

**Product names:** Magic Companion, Magic Fanverses, Magic Rewards. Never translated into French.

**The mascot has no agreed name.** Say the mark for the logo and the mascot everywhere else. Do not give it a name and do not reintroduce a withdrawn one.

## Two rules that govern the content

**Every rule names the failure it prevents.** Either one that has happened, or one a real person would plausibly commit. No failure in view means no rule. "Do not add gradients" holds, because an agency would. "No countdown to something that is not happening" was cut, because nobody would.

**The book carries no working state.** Where a writer must not invent something, give an instruction ("ask the French gate"), never a status ("undecided"). Everything unsettled lives in the register, which is outside this repo.

## What none of the checks catch

All three read syntax. Four fault types walk past them, and every one has shipped:

1. **The overstated absolute.** A narrow true point with "and never" bolted on for weight.
2. **The internal contradiction.** A rule written above a table that breaks it.
3. **Literary jargon.** Parses perfectly, tells a reader nothing.
4. **Invention inside the tooling.** The linter's own advice string once named the mascot.

After the checks pass, read the work cold. Check the tooling on the same terms as the book.

## Layout

| Path | What it is |
|---|---|
| `brandbook.html` | The source. Every change starts here |
| `index.html` | Generated. Never edited |
| `VERSION` | The only place the version number lives |
| `tools/` | The build and the three checks. See `tools/README.md` |
| `tools/sources.txt` | Every factual claim and where it came from |

`brandbook.html` carries no doctype, no head and no body. It is also published as a Claude artifact, and that platform adds the wrapper at publish time. `tools/build.py` adds the same wrapper so the two stay identical.

## One more thing

Nothing from Laura's personal brand system enters Magic work. Flag it and say so. Never drop it silently.
