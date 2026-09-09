# Magic Brand Book

The working rules for how Magic sounds, reads and looks.
Single self-contained page. The only external request is the Outfit webfont.

## What is in here

| File | What it is |
|---|---|
| `brandbook.html` | **The source of truth.** Every change starts here. |
| `index.html` | Generated from `brandbook.html` by the build. Never edited by hand. |
| `tools/` | The build and the two checks. See `tools/README.md`. |
| `.nojekyll` | Stops GitHub trying to process the page as a Jekyll site. |

`brandbook.html` carries no doctype, no `<head>` and no `<body>`. It is also published as a Claude artifact, and that platform adds the wrapper at publish time. `tools/build.py` adds the same wrapper, so the hosted page and the artifact stay identical.

## Changing the book

```
# 1. edit brandbook.html
# 2. build. This runs both checks and refuses to write if either fails.
python3 tools/build.py
# 3. commit both files
git add brandbook.html index.html && git commit -m "..." && git push
```

Run the checks on their own while drafting:

```
python3 tools/brandlint.py brandbook.html
python3 tools/claims.py brandbook.html tools/sources.txt
```

Read `tools/README.md` before adding a rule or a number. Two things it says that matter most: every rule needs a failure in view, and every factual claim needs a line in `tools/sources.txt`.

## Who edits this

**One writer at a time, and never `index.html`.** Changes made to the generated file are lost on the next build and they bypass both checks. An em dash added by hand goes unnoticed until it turns up in a screenshot.

Two writers on the generated file is what caused the last mess. Git will not warn you: the diff looks clean either way.

## Deploying it

1. Settings, then Pages, then Source: **Deploy from a branch**, `main`, `/ (root)`, Save.
2. The page appears at `https://<user>.github.io/<repo>/` within a minute or two.

On the free plan the repo must be public for Pages to serve it. The page is public either way.

## The custom domain

There is no `CNAME` file in this repo, so the page serves from `github.io` until the domain is set. To point `brand.the-magic.app` at it, first add a CNAME record in DNS:

```
brand    CNAME    <user>.github.io
```

`brand.the-magic.app` is a subdomain, so this does not touch the Webflow site on the apex domain. Then in Settings, Pages, Custom domain, enter `brand.the-magic.app` and tick **Enforce HTTPS** once the certificate is issued. GitHub writes the `CNAME` file itself when you do that. Do the DNS record first: setting the domain before the record resolves takes the `github.io` URL down as well.

## Two things to know

**The page carries `noindex`.** Search engines will not list it. Anyone with the URL can read it. That is the right setting while the Coming section still has open items on it. Remove the `<meta name="robots">` line when the book is finished.

**Gilroy is not embedded.** The page asks for Gilroy first and falls back to Outfit, which loads from Google Fonts. Anyone with Gilroy installed sees Gilroy; everyone else sees Outfit. That is the fallback rule the book itself sets.
