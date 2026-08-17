"""One-time migration: exegesis/nt/*.md  ->  osis/nt/{BOOK}.xml

This is scaffolding, not a pipeline stage. It runs once to move 260 markdown
chapters into 27 OSIS books, after which the OSIS is the source and this script
is deleted. Do not wire it into anything.

    python scripts/md_to_osis.py            # all 27 books
    python scripts/md_to_osis.py ROM        # one book

What it must get right, and why:

  * The verse range of every section. The pane finds commentary by verse
    containment, so a range lost in translation is commentary that vanishes.
    parse_heading_range() below is copied from check_pane_coverage.py rather
    than reimplemented, so the two cannot drift during the migration.
  * The 745 sections with no verse range. These are chapter-level -- "Context
    and Placement" and the chapter summaries. They are not failures. In OSIS
    they take the chapter as their annotateRef, which makes them addressable
    for the first time; the HTML gave them no id at all.
  * Every word of the prose. check_osis.py verifies this by stripping both
    sides back to bare text and comparing.
"""
import os
import re
import sys
import glob
from xml.sax.saxutils import escape

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'exegesis', 'nt')
DST = os.path.join(REPO, 'osis', 'nt')

# USFM code -> (exegesis filename stem, OSIS book ID, display name).
# The file is named for the USFM code so the commentary sits beside the Bible
# under the same name; the OSIS ID is what annotateRef has to speak.
BOOKS = [
    ('MAT', 'Matthew',        'Matt',   'Matthew'),
    ('MRK', 'Mark',           'Mark',   'Mark'),
    ('LUK', 'Luke',           'Luke',   'Luke'),
    ('JHN', 'John',           'John',   'John'),
    ('ACT', 'Acts',           'Acts',   'Acts'),
    ('ROM', 'Romans',         'Rom',    'Romans'),
    ('1CO', '1Corinthians',   '1Cor',   '1 Corinthians'),
    ('2CO', '2Corinthians',   '2Cor',   '2 Corinthians'),
    ('GAL', 'Galatians',      'Gal',    'Galatians'),
    ('EPH', 'Ephesians',      'Eph',    'Ephesians'),
    ('PHP', 'Philippians',    'Phil',   'Philippians'),
    ('COL', 'Colossians',     'Col',    'Colossians'),
    ('1TH', '1Thessalonians', '1Thess', '1 Thessalonians'),
    ('2TH', '2Thessalonians', '2Thess', '2 Thessalonians'),
    ('1TI', '1Timothy',       '1Tim',   '1 Timothy'),
    ('2TI', '2Timothy',       '2Tim',   '2 Timothy'),
    ('TIT', 'Titus',          'Titus',  'Titus'),
    ('PHM', 'Philemon',       'Phlm',   'Philemon'),
    ('HEB', 'Hebrews',        'Heb',    'Hebrews'),
    ('JAS', 'James',          'Jas',    'James'),
    ('1PE', '1Peter',         '1Pet',   '1 Peter'),
    ('2PE', '2Peter',         '2Pet',   '2 Peter'),
    ('1JN', '1John',          '1John',  '1 John'),
    ('2JN', '2John',          '2John',  '2 John'),
    ('3JN', '3John',          '3John',  '3 John'),
    ('JUD', 'Jude',           'Jude',   'Jude'),
    ('REV', 'Revelation',     'Rev',    'Revelation'),
]

# ---------------------------------------------------------------------------
# Heading range parsing -- copied verbatim from check_pane_coverage.py.
# ---------------------------------------------------------------------------

HEADING = re.compile(r'^Verses?\s+(\d+)[ab]?(?:\s*[-–]\s*(\d+)[ab]?)?', re.I)
CQ = re.compile(r'(\d+):(\d+)[ab]?(?:\s*[-–]\s*(?:(\d+):)?(\d+)[ab]?)?')
CQ_LEAD = re.compile(r'^(?:Verses?\s+)?\d+:\d+', re.I)
TRAILING = re.compile(r'^[):\s]*$')
LAST_WORD = re.compile(r'([A-Za-z]+)\s*$')
RANGE = re.compile(r'^(\d+)[a-z]?(?:-(\d+)[a-z]?)?$')

# '(vv. 1-6)', which heads every section of 30 chapters -- Matthew 2-4 and the
# Luke parables among them. The documented parser does not recognise it; those
# chapters work today only because a matching id was written into the HTML by
# hand. Reading it here is what lets the OSIS stand on its own.
VV = re.compile(r'\(vv?\.\s*(\d+)[a-z]?(?:\s*[-–]\s*(\d+)[a-z]?)?\)\s*$', re.I)


def cq_anywhere(text):
    for m in CQ.finditer(text):
        before, after = text[:m.start()], text[m.end():]
        at_start = before.strip().lower() in ('', 'verse', 'verses')
        if not (at_start or TRAILING.match(after)):
            continue
        w = LAST_WORD.search(before)
        if w and w.group(1)[0].isupper():
            continue
        return m
    return None


def parse_heading_range(text, chapter, ident=''):
    """(start_ch, start_v, end_ch, end_v) or None for a chapter-level section.

    `ident` is the id the published HTML gave this heading. It is the last
    resort and exists only for the migration: a handful of headings name their
    passage in a form no parser here reads, and the id is the only record of
    what the author meant. Once the OSIS carries annotateRef this is moot.
    """
    text = text.strip()

    if CQ_LEAD.match(text):
        m = CQ.search(text)
        if m:
            sc, sv = int(m.group(1)), int(m.group(2))
            ec = int(m.group(3)) if m.group(3) else sc
            ev = int(m.group(4)) if m.group(4) else sv
            return sc, sv, ec, ev

    m = HEADING.match(text)
    if m:
        return chapter, int(m.group(1)), chapter, int(m.group(2) or m.group(1))

    m = cq_anywhere(text)
    if m:
        sc, sv = int(m.group(1)), int(m.group(2))
        ec = int(m.group(3)) if m.group(3) else sc
        ev = int(m.group(4)) if m.group(4) else sv
        return sc, sv, ec, ev

    m = VV.search(text)
    if m:
        return chapter, int(m.group(1)), chapter, int(m.group(2) or m.group(1))

    n = RANGE.match((ident or '').strip())
    if n:
        return chapter, int(n.group(1)), chapter, int(n.group(2) or n.group(1))

    n = re.match(r'^(\d+)\.(\d+)-(\d+)\.(\d+)$', (ident or '').strip())
    if n:
        return int(n.group(1)), int(n.group(2)), int(n.group(3)), int(n.group(4))

    return None


# The verse label exactly as the heading writes it, part-verse letters and all:
# 'Verses 1-3a:' -> '1-3a', 'The Setting (vv. 1-3a)' -> '1-3a'. annotateRef can
# only speak in whole verses, so without this the fact that Matthew 13 splits
# verse 3 between two sections is lost, and the anchor a report links to
# ('#1-3a') stops existing. Both heading shapes have to be read: Matthew and
# the Luke parables use the parenthesised one throughout.
LABEL = re.compile(r'^Verses?\s+(\d+[a-z]?(?:\s*[-–]\s*\d+[a-z]?)?)\s*:', re.I)
LABEL_VV = re.compile(r'\(vv?\.\s*(\d+[a-z]?(?:\s*[-–]\s*\d+[a-z]?)?)\)\s*$', re.I)


def heading_label(text):
    text = text.strip()
    m = LABEL.match(text) or LABEL_VV.search(text)
    if not m:
        return None
    return re.sub(r'\s*[-–]\s*', '-', m.group(1))


def plain_id(rng):
    """What the label would be if the heading named whole verses only."""
    if rng is None:
        return None
    sc, sv, ec, ev = rng
    if sc != ec:
        return '%d.%d-%d.%d' % (sc, sv, ec, ev)
    return str(sv) if ev == sv else '%d-%d' % (sv, ev)


def annotate_ref(osis_id, chapter, rng):
    """The Bible passage a section is about, as an osisRef."""
    if rng is None:
        return '%s.%d' % (osis_id, chapter)
    sc, sv, ec, ev = rng
    start = '%s.%d.%d' % (osis_id, sc, sv)
    if (sc, sv) == (ec, ev):
        return start
    return '%s-%s.%d.%d' % (start, osis_id, ec, ev)


# ---------------------------------------------------------------------------
# Inline markdown
# ---------------------------------------------------------------------------

BOLD = re.compile(r'\*\*(.+?)\*\*', re.S)
ITALIC = re.compile(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', re.S)

stats = {'emdash': 0, 'tight_dash': 0}


def inline(text):
    """Markdown inline -> OSIS. Only bold and italic occur in the corpus."""
    # The prose writes em-dashes as '--'; the published HTML rendered them as
    # &mdash;. OSIS is UTF-8, so carry the real character.
    stats['tight_dash'] += len(re.findall(r'(?<! )--(?! )', text))
    stats['emdash'] += text.count('--')
    text = text.replace('--', '—')

    out, pos = [], 0
    marks = []
    for m in BOLD.finditer(text):
        marks.append((m.start(), m.end(), 'bold', m.group(1)))
    for m in ITALIC.finditer(text):
        if any(s <= m.start() < e for s, e, _, _ in marks):
            continue
        marks.append((m.start(), m.end(), 'italic', m.group(1)))
    marks.sort()

    for start, end, kind, inner in marks:
        if start < pos:
            continue
        out.append(escape(text[pos:start]))
        out.append('<hi type="%s">%s</hi>' % (kind, escape(inner)))
        pos = end
    out.append(escape(text[pos:]))
    return ''.join(out)


# ---------------------------------------------------------------------------
# Block markdown
# ---------------------------------------------------------------------------

UL = re.compile(r'^\s*[-*+]\s+(.*)$')
OL = re.compile(r'^\s*\d+[.)]\s+(.*)$')
HR = re.compile(r'^\s*(?:---+|\*\*\*+|___+)\s*$')
BQ = re.compile(r'^>\s?(.*)$')
INDENT = re.compile(r'^(?:    |\t)\s*(\S.*)$')


def blocks(lines):
    """Group raw markdown lines into (kind, payload) blocks."""
    out = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        if HR.match(line):                       # section separators; the OSIS
            i += 1                               # divs carry that structure now
            continue

        if line.startswith('###'):
            out.append(('h3', line.lstrip('#').strip()))
            i += 1
            continue

        if line.startswith('|'):                 # pipe table
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c):
                    rows.append(cells)
                i += 1
            out.append(('table', rows))
            continue

        if UL.match(line) or OL.match(line):
            kind = 'ul' if UL.match(line) else 'ol'
            items = []
            while i < len(lines):
                m = UL.match(lines[i].rstrip()) or OL.match(lines[i].rstrip())
                if not m:
                    if lines[i].strip():
                        break
                    i += 1
                    continue
                items.append(m.group(1))
                i += 1
            out.append((kind, items))
            continue

        if BQ.match(line):
            quoted = []
            while i < len(lines) and BQ.match(lines[i].rstrip()):
                quoted.append(BQ.match(lines[i].rstrip()).group(1))
                i += 1
            out.append(('quote', ' '.join(q for q in quoted if q.strip())))
            continue

        if INDENT.match(line):
            out.append(('indent', INDENT.match(line).group(1)))
            i += 1
            continue

        out.append(('p', line.strip()))
        i += 1
    return out


def render(block, indent):
    kind, payload = block
    pad = ' ' * indent
    if kind == 'p':
        return ['%s<p>%s</p>' % (pad, inline(payload))]
    if kind == 'h3':
        return ['%s<title level="2">%s</title>' % (pad, inline(payload))]
    if kind == 'quote':
        return ['%s<div type="x-blockquote"><p>%s</p></div>' % (pad, inline(payload))]
    if kind == 'indent':
        return ['%s<div type="x-indent"><p>%s</p></div>' % (pad, inline(payload))]
    if kind in ('ul', 'ol'):
        lines = ['%s<list type="%s">' % (pad, 'x-ordered' if kind == 'ol' else 'x-bullet')]
        for item in payload:
            lines.append('%s  <item>%s</item>' % (pad, inline(item)))
        lines.append('%s</list>' % pad)
        return lines
    if kind == 'table':
        lines = ['%s<table>' % pad]
        for row in payload:
            lines.append('%s  <row>' % pad)
            for cell in row:
                lines.append('%s    <cell>%s</cell>' % (pad, inline(cell)))
            lines.append('%s  </row>' % pad)
        lines.append('%s</table>' % pad)
        return lines
    raise AssertionError(kind)


# ---------------------------------------------------------------------------
# Chapter and book assembly
# ---------------------------------------------------------------------------

H2 = re.compile(r'<h2(?:\s+id="([^"]*)")?\s*>(.*?)</h2>', re.S)


def norm_heading(text):
    """Heading text reduced so markdown and HTML forms compare equal."""
    text = re.sub(r'<[^>]+>', '', text)
    text = (text.replace('&mdash;', '--').replace('—', '--')
                .replace('&amp;', '&').replace('&quot;', '"')
                .replace('&lsquo;', "'").replace('&rsquo;', "'"))
    return re.sub(r'\s+', ' ', text).strip().lower()


def html_ids(stem, chapter):
    """{normalised heading text: id} from the published HTML for this chapter."""
    path = os.path.join(REPO, 'docs', 'exegesis', 'nt',
                        '%s_%02d.html' % (stem, chapter))
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as fh:
        return {norm_heading(t): (i or '') for i, t in H2.findall(fh.read())}


def parse_chapter(path, chapter, ids=None):
    """-> (chapter_title, [(heading, range, [blocks])])"""
    ids = ids or {}
    with open(path, encoding='utf-8-sig') as fh:
        lines = fh.read().split('\n')

    title = None
    sections = []
    current = None
    body = []

    for line in lines:
        s = line.rstrip()
        if s.startswith('# ') and title is None:
            title = s[2:].strip()
            continue
        if s.startswith('## '):
            if current is not None or body:
                sections.append((current, body))
            current = s[3:].strip()
            body = []
            continue
        body.append(line)

    if current is not None or body:
        sections.append((current, body))

    out = []
    for heading, raw in sections:
        if heading is None:
            # Prose before the first h2. None occurs in the corpus, but if one
            # ever appears it belongs to the chapter rather than being dropped.
            if not any(l.strip() for l in raw):
                continue
            heading = 'Introduction'
        ident = ids.get(norm_heading(heading), '')
        out.append((heading, parse_heading_range(heading, chapter, ident), blocks(raw)))
    return title, out


def build_book(code, stem, osis_id, name):
    paths = sorted(glob.glob(os.path.join(SRC, '%s_[0-9][0-9].md' % stem)))
    if not paths:
        return None, 0, 0

    lines = []
    add = lines.append
    add('<?xml version="1.0" encoding="UTF-8"?>')
    add('<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace"')
    add('      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    add('      xsi:schemaLocation="http://www.bibletechnologies.net/2003/OSIS/namespace '
        'http://www.bibletechnologies.net/osisCore.2.1.1.xsd">')
    add('  <osisText osisIDWork="RCBComm" osisRefWork="Bible" xml:lang="en">')
    add('    <header>')
    add('      <work osisWork="RCBComm">')
    add('        <title>Restored Context Bible: Commentary</title>')
    add('        <type type="OSIS">Commentary</type>')
    add('        <identifier type="OSIS">Commentary.en.RCB</identifier>')
    add('        <refSystem>Bible</refSystem>')
    add('      </work>')
    add('      <work osisWork="Bible">')
    add('        <type type="OSIS">Bible</type>')
    add('        <refSystem>Bible</refSystem>')
    add('      </work>')
    add('    </header>')
    add('    <div type="book" osisID="%s">' % osis_id)
    add('      <title>%s</title>' % escape(name))

    n_sections = 0
    for path in paths:
        chapter = int(os.path.basename(path)[:-3].rsplit('_', 1)[1])
        title, sections = parse_chapter(path, chapter, html_ids(stem, chapter))
        add('      <div type="chapter" osisID="%s.%d">' % (osis_id, chapter))
        add('        <title>%s</title>' % inline(title or '%s %d' % (name, chapter)))
        for heading, rng, body in sections:
            ref = annotate_ref(osis_id, chapter, rng)
            label = heading_label(heading)
            n = ''
            if label and label != plain_id(rng):
                n = ' n="%s"' % escape(label, {'"': '&quot;'})
            add('        <div type="section" annotateType="commentary" '
                'annotateRef="%s"%s>' % (ref, n))
            add('          <title>%s</title>' % inline(heading))
            for block in body:
                lines.extend(render(block, 10))
            add('        </div>')
            n_sections += 1
        add('      </div>')

    add('    </div>')
    add('  </osisText>')
    add('</osis>')
    return '\n'.join(lines) + '\n', len(paths), n_sections


def main():
    wanted = [b.upper() for b in sys.argv[1:]]
    os.makedirs(DST, exist_ok=True)

    tot_ch = tot_sec = 0
    for code, stem, osis_id, name in BOOKS:
        if wanted and code not in wanted:
            continue
        xml, n_ch, n_sec = build_book(code, stem, osis_id, name)
        if xml is None:
            print('%-5s no markdown found' % code)
            continue
        out = os.path.join(DST, code + '.xml')
        with open(out, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(xml)
        tot_ch += n_ch
        tot_sec += n_sec
        print('%-5s %2d chapters  %4d sections  %8.0fK' % (code, n_ch, n_sec, len(xml) / 1024))

    print()
    print('chapters: %d   sections: %d' % (tot_ch, tot_sec))
    print('em-dashes converted: %d (of which not space-separated: %d)'
          % (stats['emdash'], stats['tight_dash']))


if __name__ == '__main__':
    main()
