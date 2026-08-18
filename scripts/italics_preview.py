"""Render a marked book to a single local HTML page so it can be read.

    python scripts/italics_preview.py ROM

Writes preview/italics-{BOOK}.html -- one self-contained file, no server, no
data file, nothing to regenerate. Open it in a browser.

It exists because the real viewer reads docs/commentary/data/{BOOK}.js, which
is built from osis/nt/. Pointing that at the marked copy would put unapproved
work on the live site. This shows the marked book without touching any of it.

The toggle at the top switches the italics off, so the same page shows what
the reader has now and what the pass would give them.
"""

import html
import os
import re
import sys
import xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"

PAGE = """<!doctype html>
<meta charset="utf-8">
<title>%(book)s -- italics preview</title>
<style>
 :root { color-scheme: light dark; }
 body { max-width: 46rem; margin: 0 auto; padding: 1rem 1.2rem 6rem;
        font: 17px/1.65 Georgia, "Times New Roman", serif; }
 .bar { position: sticky; top: 0; background: Canvas; padding: .7rem 0;
        border-bottom: 1px solid color-mix(in srgb, CanvasText 20%%, Canvas);
        font: 14px/1.4 system-ui, sans-serif; display: flex; gap: 1rem;
        align-items: center; flex-wrap: wrap; }
 .bar button { font: inherit; padding: .35rem .8rem; cursor: pointer; }
 .count { opacity: .65; }
 h1 { font-size: 1.6rem; }
 h2 { font-size: 1.25rem; margin-top: 2.4rem;
      padding-top: .6rem;
      border-top: 1px solid color-mix(in srgb, CanvasText 12%%, Canvas); }
 h3 { font-size: 1.05rem; margin-top: 1.8rem; }
 .ref { font: 12px/1 system-ui, sans-serif; opacity: .55;
        letter-spacing: .04em; text-transform: uppercase; }
 i { color: #7a3e00; font-style: italic; }
 @media (prefers-color-scheme: dark) { i { color: #e8b57a; } }
 body.off i { font-style: normal; color: inherit; }
 blockquote { margin: 1rem 0 1rem 1.4rem; padding-left: 1rem;
              border-left: 3px solid color-mix(in srgb, CanvasText 20%%, Canvas); }
</style>
<div class="bar">
  <button id="t">Turn italics off</button>
  <span class="count">%(n)d italicised in %(book)s</span>
</div>
%(body)s
<script>
 const b = document.body, t = document.getElementById('t');
 t.onclick = () => {
   b.classList.toggle('off');
   t.textContent = b.classList.contains('off') ? 'Turn italics on' : 'Turn italics off';
 };
</script>
"""


def inline(el):
    """Render an element's text and children as HTML."""
    out = [html.escape(el.text or "")]
    for kid in el:
        tag = kid.tag.replace(NS, "")
        inner = inline(kid)
        if tag == "hi":
            kind = kid.get("type")
            out.append("<i>%s</i>" % inner if kind == "italic" else
                       "<b>%s</b>" % inner if kind == "bold" else inner)
        else:
            out.append(inner)
        out.append(html.escape(kid.tail or ""))
    return "".join(out)


def block(el, depth):
    tag = el.tag.replace(NS, "")
    if tag == "p":
        return "<p>%s</p>\n" % inline(el)
    if tag == "title":
        return "<h%d>%s</h%d>\n" % (min(depth, 4), inline(el), min(depth, 4))
    if tag in ("list",):
        return "<ul>%s</ul>\n" % "".join(
            "<li>%s</li>" % inline(k) for k in el)
    if tag == "div" and el.get("type") in ("x-blockquote", "x-indent"):
        return "<blockquote>%s</blockquote>\n" % "".join(
            block(k, depth + 1) for k in el)
    if tag == "div":
        out = []
        ref = el.get("annotateRef")
        if ref:
            out.append('<div class="ref">%s</div>\n' % html.escape(ref))
        out.extend(block(k, depth + 1) for k in el)
        return "".join(out)
    return "".join(block(k, depth) for k in el) or ""


def main(book):
    src = os.path.join(REPO, "osis", "nt-italics", book + ".xml")
    if not os.path.exists(src):
        sys.exit("no marked book at %s -- run italics.py build first" % src)

    with open(src, encoding="utf-8") as fh:
        raw = fh.read()
    n = len(re.findall(r'<hi type="italic">', raw))

    root = ET.fromstring(raw)
    text = root.find(NS + "osisText")
    body = "".join(block(d, 1) for d in text.findall(NS + "div"))

    out_dir = os.path.join(REPO, "preview")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "italics-%s.html" % book)
    with open(dst, "w", encoding="utf-8", newline="") as fh:
        fh.write(PAGE % {"book": book, "n": n, "body": body})
    print("wrote %s" % os.path.relpath(dst, REPO))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python scripts/italics_preview.py {BOOK}")
    main(sys.argv[1])
