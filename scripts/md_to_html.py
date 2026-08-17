"""Convert an exegesis markdown chapter to the site's HTML form.

    python scripts/md_to_html.py Galatians 1 2 3 4 5 6
    python scripts/md_to_html.py Galatians          # all chapters of the book

Reads  exegesis/nt/{Book}_{NN}.md
Writes docs/exegesis/nt/{Book}_{NN}.html

The HTML is the house format: a nav strip with prev / Home / next, an <h1>,
<h2> section headings carrying an id built from the verse range, <p> for
paragraphs, <hr> between sections.

The id matters beyond anchoring: scripts/check_pane_coverage.py reads section
ranges from the *heading text*, and the commentary pane in docs/index.html syncs
to the exegesis by verse containment. A heading that does not begin
"Verses N-M:" will not be matched as a range.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "exegesis" / "nt"
OUT = ROOT / "docs" / "exegesis" / "nt"

# Canonical NT order with chapter counts, for the prev/next links.
NT = [
    ("Matthew", 28), ("Mark", 16), ("Luke", 24), ("John", 21), ("Acts", 28),
    ("Romans", 16), ("1Corinthians", 16), ("2Corinthians", 13), ("Galatians", 6),
    ("Ephesians", 6), ("Philippians", 4), ("Colossians", 4),
    ("1Thessalonians", 5), ("2Thessalonians", 3),
    ("1Timothy", 6), ("2Timothy", 4), ("Titus", 3), ("Philemon", 1),
    ("Hebrews", 13), ("James", 5), ("1Peter", 5), ("2Peter", 3),
    ("1John", 5), ("2John", 1), ("3John", 1), ("Jude", 1), ("Revelation", 22),
]

STYLE = """:root { --bg: #ffffff; --fg: #1a1a1a; --border: #dee2e6; --accent: #2471a3; --qbg: #f8f9fa; }
@media (prefers-color-scheme: dark) {
  :root { --bg: #1a1a2e; --fg: #e0e0e0; --border: #2a2a4a; --accent: #5dade2; --qbg: #16213e; }
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Georgia,'Times New Roman',serif;background:var(--bg);color:var(--fg);line-height:1.75;padding:24px;max-width:820px;margin:0 auto}
h1{font-size:1.6rem;margin:28px 0 12px}
h2{font-size:1.3rem;margin:24px 0 10px;border-bottom:1px solid var(--border);padding-bottom:4px}
h3{font-size:1.1rem;margin:20px 0 8px}
p{margin:10px 0;text-align:justify}
hr{border:none;border-top:2px solid var(--border);margin:24px 0}
ul,ol{margin:10px 0 10px 24px}
li{margin:4px 0}
blockquote{border-left:3px solid var(--accent);padding:8px 16px;margin:12px 0;background:var(--qbg)}
a{color:var(--accent)}

.nav{display:flex;justify-content:space-between;align-items:center;padding:0 0 16px;font-size:0.88rem;border-bottom:1px solid var(--border);margin-bottom:16px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.nav a{color:var(--accent);text-decoration:none}
.nav a:hover{text-decoration:underline}
.nav .ph{visibility:hidden}
.nav-bottom{border-bottom:none;border-top:1px solid var(--border);padding:16px 0 0;margin-top:28px;margin-bottom:0}"""


# A chapter-qualified verse range: '7:53-8:11', '12:18-13:2', '8:3-11', '3:16'.
# The end may drop the chapter when it does not change.
CHAPTER_QUALIFIED = re.compile(
    r"\d+:\d+[ab]?(?:\s*[-–]\s*(?:\d+:)?\d+[ab]?)?")
TRAILING = re.compile(r"^[):\s]*$")
LAST_WORD = re.compile(r"([A-Za-z]+)\s*$")
CQ_LEAD = re.compile(r"^(?:Verses?\s+)?\d+:\d+", re.I)
# The plain form, which must not require a colon straight after the range:
# 'Verses 31-33 and 11:1:' and 'Verses 18-25 (through 4:1):' are both real
# section headings, and demanding the colon left them with no id at all -- so
# the checker saw the section and the pane did not.
PLAIN = re.compile(r"^Verses?\s+(\d+[ab]?(?:\s*[-–]\s*\d+[ab]?)?)", re.I)


def about_range(title):
    """The chapter-qualified range a heading is *about*, or None.

    Mirrors cq_anywhere() in check_pane_coverage.py, and the two must agree:
    this decides whether the heading gets an id, and without an id the pane
    never looks at the section at all.

    The range has to open or close the heading -- 'The Lost Sheep (15:4-7)',
    'A Note on 7:53-8:11' -- and must not follow a capitalised word, which is
    how a cross-reference names its book. 'The Fulfillment of Acts 1:8' is a
    heading inside Acts 10 and is not a section on Acts 1.
    """
    for m in CHAPTER_QUALIFIED.finditer(title):
        before, after = title[:m.start()], title[m.end():]
        at_start = before.strip().lower() in ("", "verse", "verses")
        if not (at_start or TRAILING.match(after)):
            continue
        w = LAST_WORD.search(before)
        if w and w.group(1)[0].isupper():
            continue
        return m
    return None


def flat(book, chapter):
    """('Galatians', 1) -> 'Galatians_01'"""
    return "%s_%02d" % (book, chapter)


def pretty(book, chapter):
    """('1Corinthians', 3) -> '1 Corinthians 3'"""
    name = re.sub(r"^([123])(?=[A-Z])", r"\1 ", book)
    return "%s %d" % (name, chapter)


def neighbours(book, chapter):
    """Return (prev, next) as (book, chapter) tuples, crossing book boundaries."""
    i = [b for b, _ in NT].index(book)
    prev = (book, chapter - 1) if chapter > 1 else (
        (NT[i - 1][0], NT[i - 1][1]) if i > 0 else None)
    nxt = (book, chapter + 1) if chapter < NT[i][1] else (
        (NT[i + 1][0], 1) if i < len(NT) - 1 else None)
    return prev, nxt


def inline(text):
    """Escape, then apply inline markdown. Order matters throughout."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\*\w])\*([^\*]+?)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    # House style for the em-dash. Must run after the --- hr lines are consumed.
    text = text.replace("--", "&mdash;")
    return text


def heading_id(title, chapter):
    """'Verses 16b-18: The Sign' -> '16b-18'. Non-verse headings get no id.

    A heading may also carry a chapter-qualified range anywhere in its text --
    'A Note on 7:53-8:11', 'The Lost Sheep (15:4-7)' -- and those get an id
    too. Without one the pane skips the heading entirely, because it queries
    h2[id], which is how a fully written section came to be reported as
    missing analysis.
    """
    if CQ_LEAD.match(title):
        m = CHAPTER_QUALIFIED.search(title)
        if m:
            return qualified_id(m, chapter)
    m = PLAIN.match(title)
    if m:
        return re.sub(r"\s+", "", m.group(1))
    m = about_range(title)
    return qualified_id(m, chapter) if m else None


def qualified_id(m, chapter):
    """'(2:1-12)' in Matthew 2 -> '1-12'; 'A Note on 7:53-8:11' -> '7.53-8.11'.

    A range wholly inside the chapter it is written in keeps the bare verse
    form, because that is what the reports build their anchors from --
    exegesisHref() takes the part of '2:1-12' after the colon. Anything that
    reaches into another chapter has to say so, and is dotted rather than
    colon-separated to stay usable as a fragment and in a selector.
    """
    raw = re.sub(r"\s+", "", m.group(0)).replace("–", "-")
    parts = raw.split("-")
    chapters = set(p.split(":")[0] for p in parts if ":" in p)
    if chapters == {str(chapter)}:
        return "-".join(p.split(":")[-1] for p in parts)
    return raw.replace(":", ".")


def convert(book, chapter):
    src = SRC / (flat(book, chapter) + ".md")
    if not src.exists():
        raise SystemExit("missing source: %s" % src)
    lines = src.read_text(encoding="utf-8").split("\n")

    title = pretty(book, chapter)
    body = []
    para = []
    list_buf = []
    list_tag = None

    def flush_para():
        if para:
            body.append("<p>" + inline(" ".join(para).strip()) + "</p>")
            del para[:]

    def flush_list():
        if list_buf:
            body.append("<%s>" % list_tag)
            body.extend("<li>" + inline(x) + "</li>" for x in list_buf)
            body.append("</%s>" % list_tag)
            del list_buf[:]

    for raw in lines:
        line = raw.rstrip()

        if not line.strip():
            flush_para()
            flush_list()
            continue

        if line.startswith("# "):
            flush_para(); flush_list()
            body.append("<h1>" + inline(line[2:].strip()) + "</h1>")
            continue

        if line.startswith("## "):
            flush_para(); flush_list()
            text = line[3:].strip()
            hid = heading_id(text, chapter)
            attr = ' id="%s"' % hid if hid else ""
            body.append("<h2%s>%s</h2>" % (attr, inline(text)))
            continue

        if line.startswith("### "):
            flush_para(); flush_list()
            body.append("<h3>" + inline(line[4:].strip()) + "</h3>")
            continue

        if re.match(r"^-{3,}$", line.strip()):
            flush_para(); flush_list()
            body.append("<hr>")
            continue

        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            flush_para()
            list_tag = "ul"
            list_buf.append(m.group(1))
            continue

        # Numbered points render as paragraphs in this format, not as <ol>,
        # so that the bolded lead sentence sits inline with its body text.
        para.append(line.strip())

    flush_para()
    flush_list()

    prev, nxt = neighbours(book, chapter)
    left = ('<a href="%s.html">&larr; %s</a>' % (flat(*prev), pretty(*prev))
            if prev else '<span class="ph">&larr;</span>')
    right = ('<a href="%s.html">%s &rarr;</a>' % (flat(*nxt), pretty(*nxt))
             if nxt else '<span class="ph">&rarr;</span>')
    nav = '<div class="nav">%s<a href="../../index.html">Home</a>%s</div>' % (left, right)

    html = "\n".join([
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        "<title>%s</title>" % title,
        "<style>",
        STYLE,
        "</style>",
        "</head>",
        "<body>",
        nav,
        "\n".join(body),
        "",
        "</body>",
        "</html>",
        "",
    ])

    dest = OUT / (flat(book, chapter) + ".html")
    dest.write_text(html, encoding="utf-8")
    return dest


def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    book = argv[0]
    known = dict(NT)
    if book not in known:
        raise SystemExit("unknown book: %s" % book)
    chapters = [int(x) for x in argv[1:]] or list(range(1, known[book] + 1))
    for ch in chapters:
        print("wrote %s" % convert(book, ch).relative_to(ROOT))


if __name__ == "__main__":
    main(sys.argv[1:])
