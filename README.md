# Magic Brand Book

The working rules for how Magic sounds, reads and looks.
Single self-contained page. No build step, no dependencies, no framework.

## What is in here

| File | What it is |
|---|---|
| `index.html` | The whole book. The mascot is embedded, so the only external request is the Outfit webfont. |
| `.nojekyll` | Stops GitHub trying to process the page as a Jekyll site. |

There is deliberately **no `CNAME` file**. `brand.the-magic.app` has no DNS record yet, and a `CNAME` file would make GitHub redirect the working `github.io` URL to a domain that does not resolve. See *The custom domain* below for how to switch over.

## Deploying it

Already done. The book is live at **https://vibeonmagic.github.io/magic-brand-book/**, served from the `main` branch of `vibeonmagic/magic-brand-book`.

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

`brand.the-magic.app` is a subdomain, so this does not touch the Webflow site on the apex domain. Then in Settings → Pages → Custom domain, enter `brand.the-magic.app` and tick **Enforce HTTPS** once the certificate is issued. GitHub writes the `CNAME` file itself when you do this; do not commit one by hand before the DNS record exists.

## Updating it

Replace `index.html` and commit. The page is live within a minute. There is no version pinning and no share dialog: whoever holds the link sees the current file.

## Two things to know

**The page carries `noindex`.** Search engines will not list it, but anyone with the URL can read it. That is the right setting while the Coming section still has open items on it. Remove the `<meta name="robots">` line when the book is finished.

**Gilroy is not embedded.** The page asks for Gilroy first and falls back to Outfit, which loads from Google Fonts. Anyone with Gilroy installed sees Gilroy; everyone else sees Outfit. That is the fallback rule the book itself sets.
