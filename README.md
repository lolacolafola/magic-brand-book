# Magic Brand Book

The working rules for how Magic sounds, reads and looks.
Single self-contained page. No build step, no dependencies, no framework.

## What is in here

| File | What it is |
|---|---|
| `index.html` | The whole book. The mascot is embedded, so the only external request is the Outfit webfont. |
| `.nojekyll` | Stops GitHub trying to process the page as a Jekyll site. |

## Deploying it

Already done. The book is live at **https://vibeonmagic.github.io/magic-brand-book/**, served from the `main` branch of `vibeonmagic/magic-brand-book`, and mirrored to `lolacolafola/magic-brand-book`.

There is deliberately **no `CNAME` file in this repo**. `brand.the-magic.app` has no DNS record yet, and a `CNAME` file would make GitHub redirect the working `github.io` URL to a domain that does not resolve. See *The custom domain* below.

To set it up again from scratch:

1. Create a repository. `magic-brand-book` is fine. **Private is fine too**, GitHub Pages serves from private repos on paid plans; on the free plan the repo must be public, and the page is public either way.
2. Push `index.html`, `README.md` and `.nojekyll` to the root of the `main` branch.
3. Settings → Pages → Source: **Deploy from a branch** → `main` → `/ (root)` → Save.
4. Wait a minute or two. The page appears at `https://<user>.github.io/<repo>/`.

## The custom domain

Not switched on yet. To do it, add a CNAME record in the DNS for `the-magic.app`:

```
brand    CNAME    vibeonmagic.github.io
```

`brand.the-magic.app` is a subdomain, so this does not touch the Webflow site on the apex domain. Then in Settings → Pages → Custom domain, enter `brand.the-magic.app` and tick **Enforce HTTPS** once the certificate is issued. GitHub writes the `CNAME` file itself at that point; do not commit one by hand before the DNS record exists.

## Updating it

Replace `index.html` and commit. The page is live within a minute. There is no version pinning and no share dialog: whoever holds the link sees the current file.

## Two things to know

**The page carries `noindex`.** Search engines will not list it, but anyone with the URL can read it. That is the right setting while the Coming section still has open items on it. Remove the `<meta name="robots">` line when the book is finished.

**Gilroy is not embedded.** The page asks for Gilroy first and falls back to Outfit, which loads from Google Fonts. Anyone with Gilroy installed sees Gilroy; everyone else sees Outfit. That is the fallback rule the book itself sets.

## Who edits this

**One writer.** `index.html` is generated, and it is authored in the Cowork session that holds the brand book, the linter (`brandlint.py`), the claims checker (`claims.py`) and `sources.txt`. Every rule in the book traces to a line in that sources file, and every publish is checked against both scripts.

**Do not edit `index.html` in the repo.** Changes made here are lost the next time the file is regenerated, and they bypass both checks. An em dash added by hand will not be caught by anyone until it turns up in a screenshot.

**If another agent or another session touches this repo,** it commits the file it was handed and changes nothing inside it. Two writers on this file is what caused the last mess.

To change the book: ask in the Cowork session, take the new `index.html`, commit it.
