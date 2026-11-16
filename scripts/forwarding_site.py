#!/usr/bin/env python3
"""The forwarding version of the published site, for its former address.

PLATO's site is at https://plato.pelagios.org/. It was first published at
https://pelagios.org/place-attestation-ontology/, from this repository's
gh-pages branch, and links to that address are in papers, in other sites and
in software. This script makes, from the built site, what gh-pages holds now:

- every HTML page becomes a small page that sends the reader to the same path
  on the new host, the query and the #fragment kept (by script; without
  script, by a refresh to the page; and a link to follow by hand). Each names
  the new address as canonical and asks not to be indexed;
- every other file (ontology.ttl, .jsonld, .owl, .nt, schemas/, releases/,
  the guide's downloads, images, styles and scripts) is copied as it is, so
  that software which fetches a file from the former address still gets it;
- 404.html sends a path that is not there to the same path on the new host;
- .nojekyll, so that GitHub Pages serves every file as it is.

    python3 scripts/forwarding_site.py <built site> <out>

The site itself is published to the `site` branch, which plato.pelagios.org
copies (pelagios/plato-tools, .github/workflows/pages.yml). That workflow
refuses a tree of these pages, which there would each forward to themselves:
it knows them by MARK, below, so do not rename it.

Standard library only. The script checks what it wrote and exits non-zero if
any page does not forward or any other file is not the copy.
"""
import filecmp
import html
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

NEW = "https://plato.pelagios.org/"
# Where gh-pages is served: the path a request's own path is taken from.
OLD_BASE = "/place-attestation-ontology/"
# The mark of a forwarding page. plato-tools looks for it (scripts/assemble-site.mjs, forwardsHere).
MARK = '<meta name="plato-forward" content="%s">' % NEW

PAGE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<title>PLATO has moved to plato.pelagios.org</title>
{mark}
<meta name="robots" content="noindex">
<link rel="canonical" href="{target}">
<script>
(function () {{
  var base = {base}, p = location.pathname;
  var to = p.toLowerCase().indexOf(base) === 0 ? {new} + p.slice(base.length) : {target_js};
  location.replace(to + location.search + location.hash);
}})();
</script>
<noscript><meta http-equiv="refresh" content="0; url={target}"></noscript>
</head><body>
<p>PLATO, the Place Attestation Ontology, has moved. {what} is now at
<a href="{target}">{target}</a>.</p>
</body></html>
"""


def js(text):
    """A JavaScript string literal, safe inside a <script> element."""
    import json
    return json.dumps(text).replace("<", "\\u003c")


def page(target, what="This page"):
    return PAGE.format(mark=MARK, target=html.escape(target, quote=True), base=js(OLD_BASE), new=js(NEW),
                       target_js=js(target), what=what)


def target_of(rel):
    """The new address of a page, from its path in the site: a directory's index.html is the directory."""
    parts = list(rel.parts)
    if parts[-1].lower() in ("index.html", "index.htm"):
        parts[-1] = ""
    return NEW + "/".join(quote(part) for part in parts)


def is_page(path):
    return path.suffix.lower() in (".html", ".htm")


def build(site, out):
    site, out = Path(site), Path(out)
    for needed in ("index-en.html", "guide/index.html", "ontology.ttl"):
        if not (site / needed).is_file():
            sys.exit(f"{site} has no {needed}: not the built site")
    files = sorted(p for p in site.rglob("*") if p.is_file() and ".git" not in p.relative_to(site).parts)
    for path in files:
        if is_page(path) and 'name="plato-forward"' in path.read_text(encoding="utf-8", errors="replace"):
            sys.exit(f"{path} is already a forwarding page: give the built site, not its forwarding version")
    if out.exists():
        shutil.rmtree(out)
    pages = copies = 0
    for path in files:
        rel = path.relative_to(site)
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if is_page(path):
            dest.write_text(page(target_of(rel)), encoding="utf-8")
            pages += 1
        else:
            shutil.copyfile(path, dest)
            copies += 1
    # A path that is not there: the same path on the new host (which answers with its own 404 page if it has none).
    (out / "404.html").write_text(page(NEW, what="What was at this address"), encoding="utf-8")
    (out / ".nojekyll").touch()

    # What was written, checked: every page forwards, every other file is the copy, nothing is missing.
    wrong = []
    for path in files:
        rel = path.relative_to(site)
        dest = out / rel
        if is_page(path):
            text = dest.read_text(encoding="utf-8")
            if MARK not in text or "location.replace" not in text or 'rel="canonical"' not in text or "noindex" not in text:
                wrong.append(f"{rel}: not a forwarding page")
        elif not filecmp.cmp(path, dest, shallow=False):
            wrong.append(f"{rel}: not the copy")
    for rel in ("404.html", ".nojekyll", "ontology.ttl", "schemas/plato.context.jsonld"):
        if not (out / rel).is_file():
            wrong.append(f"{rel}: missing")
    if MARK not in (out / "404.html").read_text(encoding="utf-8"):
        wrong.append("404.html: not a forwarding page")
    if wrong:
        sys.exit("The forwarding version is not as it should be:\n  " + "\n  ".join(wrong))
    print(f"{out}: {pages} pages forward to {NEW} and {copies} other files are copied as they are, with 404.html and .nojekyll")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python3 scripts/forwarding_site.py <built site> <out>")
    build(sys.argv[1], sys.argv[2])
