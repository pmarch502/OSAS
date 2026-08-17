"""Check that the commentary pane can find a section for every verse the RCB has.

The pane syncs by verse containment: it takes the verse at the reading line and
shows the exegesis section whose range contains it. Where no section contains
it the pane says so honestly, but each such verse is a stretch of text with no
commentary, so they are worth knowing about and worth not growing.

This walks the same path the viewer does -- every verse in usfm/nt/{BOOK}.usfm
against the section ranges in docs/exegesis/nt/{Book}_{NN}.html -- so it catches
interior gaps, chapters whose exegesis starts late, and verses running past the
last section alike. An earlier version compared section ranges only to each
other and structurally could not see that last case.

    python scripts/check_pane_coverage.py

Exits non-zero if an uncovered verse appears that is not in EXPECTED below.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

H2 = re.compile(r'<h2 id="([^"]+)">(.*?)</h2>', re.S)
HEADING = re.compile(r'^Verses?\s+(\d+)[ab]?(?:\s*[-–]\s*(\d+)[ab]?)?', re.I)
RANGE = re.compile(r'^(\d+)[a-z]?(?:-(\d+)[a-z]?)?$')

# A chapter-qualified range, for a section whose passage crosses a chapter
# boundary. Matched at the head of the text after an optional 'Verses', and
# otherwise searched for anywhere in it, which is what catches a heading like
# 'A Note on 7:53-8:11'.
CQ = re.compile(r'(\d+):(\d+)[ab]?(?:\s*[-–]\s*(?:(\d+):)?(\d+)[ab]?)?')
CQ_LEAD = re.compile(r'^(?:Verses?\s+)?\d+:\d+', re.I)
TRAILING = re.compile(r'^[):\s]*$')
LAST_WORD = re.compile(r'([A-Za-z]+)\s*$')

# USFM code -> exegesis filename stem.
BOOKS = {
    'MAT': 'Matthew', 'MRK': 'Mark', 'LUK': 'Luke', 'JHN': 'John',
    'ACT': 'Acts', 'ROM': 'Romans', '1CO': '1Corinthians',
    '2CO': '2Corinthians', 'GAL': 'Galatians', 'EPH': 'Ephesians',
    'PHP': 'Philippians', 'COL': 'Colossians', '1TH': '1Thessalonians',
    '2TH': '2Thessalonians', '1TI': '1Timothy', '2TI': '2Timothy',
    'TIT': 'Titus', 'PHM': 'Philemon', 'HEB': 'Hebrews', 'JAS': 'James',
    '1PE': '1Peter', '2PE': '2Peter', '1JN': '1John', '2JN': '2John',
    '3JN': '3John', 'JUD': 'Jude', 'REV': 'Revelation',
}

# Verses the RCB carries that no exegesis section covers.
#
# Treat every entry here as a suspect, not a finding. Three times running, a
# reported gap has turned out to be a heading this checker could not parse
# sitting on top of analysis that was written all along:
#
#   Titus 2:7-10        the section covered 2-10, with subsections on the
#                       younger men (6-8) and on slaves (9-10). Only its
#                       heading said "Verses 2-6". Fixed 2026-08-13.
#   John 7:53-8:11      John_08 carries a full reading of the passage under
#                       the heading "A Note on 7:53-8:11" -- the entrapment
#                       between Rome's monopoly on capital sentences and
#                       Moses, the missing man of Deuteronomy 22:22, the
#                       witnesses casting first at Deuteronomy 17:7. The
#                       heading did not begin "Verses", so it got no id, and
#                       a section the pane never even looked at was recorded
#                       here as the exegesis having "not gone there".
#                       Fixed 2026-08-17.
#
# Read the section body before believing a gap, and check the neighbouring
# chapter's file -- analysis of a passage that straddles a chapter boundary is
# written in one file and belongs to both.
#
# Revelation 12:18 is the one genuine entry, and it is still not missing
# analysis: Revelation_13 opens by discussing the clause, with the Greek and
# both textual traditions. But it discusses it under "Context and Placement",
# which carries no verse range by design, so no section claims the verse.
# Closing it means an authoring decision, not a parser change.
EXPECTED = {
    'REV 12:18': 'discussed in Revelation_13 under "Context and Placement", '
                 'which carries no verse range',
}


def cq_anywhere(text):
    """A chapter-qualified range that this heading is *about*.

    Two tests, both needed. The range must open or close the heading -- these
    sections are titled 'The Lost Sheep (15:4-7)' or 'A Note on 7:53-8:11', and
    a reference buried mid-sentence ('The Rhetorical Function of 1:18-32 in
    Context') is commentary on a passage the chapter has already covered under
    its own heading. And it must not follow a capitalised word, which is how a
    cross-reference to another book announces itself: 'The Fulfillment of Acts
    1:8' is a heading in Acts 10 and does not make it a section on Acts 1.
    """
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


def parse_heading_range(text, ident, chapter):
    """Mirror parseHeadingRange() in docs/index.html.

    Returns an absolute (start_ch, start_v, end_ch, end_v), because a section
    may cover a passage that crosses a chapter boundary and so cannot be
    described by verse numbers alone.

    A section starting or ending mid-verse has an id holding only its first
    verse token ('Verses 16b-18' carries id="16"), so the heading text is the
    authority and the id is the fallback. Reading the ids alone left 31 phantom
    gaps across the NT.

    Order matters. The plain form is tried before searching the text for a
    chapter-qualified range, so a heading like 'Verses 1-5: The 3:16 Principle'
    is read as verses 1-5 and not as chapter 3.
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

    n = RANGE.match(ident.strip())
    if n:
        return chapter, int(n.group(1)), chapter, int(n.group(2) or n.group(1))
    return None


def contains(rng, chapter, verse):
    sc, sv, ec, ev = rng
    after = chapter > sc or (chapter == sc and verse >= sv)
    before = chapter < ec or (chapter == ec and verse <= ev)
    return after and before


def rcb_verses(code):
    """[(chapter, verse)] in the order the RCB has them."""
    path = os.path.join(REPO, 'usfm', 'nt', code + '.usfm')
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    out = []
    chapter = 0
    for raw in text.split('\n'):
        line = raw.strip()
        m = re.match(r'\\c (\d+)', line)
        if m:
            chapter = int(m.group(1))
            continue
        m = re.match(r'\\v (\d+)', line)
        if m:
            out.append((chapter, int(m.group(1))))
    return out


def sections(stem, chapter):
    path = os.path.join(REPO, 'docs', 'exegesis', 'nt',
                        '%s_%02d.html' % (stem, chapter))
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as fh:
        heads = H2.findall(fh.read())
    out = []
    for ident, text in heads:
        r = parse_heading_range(text, ident, chapter)
        if r:
            out.append(r)
    return out or None


def main():
    total = 0
    uncovered = []
    missing_files = []

    for code, stem in BOOKS.items():
        verses = rcb_verses(code)
        total += len(verses)
        cache = {}

        def load(ch):
            if ch not in cache:
                cache[ch] = sections(stem, ch)
            return cache[ch] or []

        for chapter, verse in verses:
            if chapter not in cache:
                cache[chapter] = sections(stem, chapter)
                if cache[chapter] is None:
                    missing_files.append('%s %d' % (stem, chapter))
            found = any(contains(r, chapter, verse) for r in (cache[chapter] or []))
            # A section covering a passage that crosses a chapter boundary is
            # written in one chapter's file and covers verses in the other's.
            # John 7:53-8:11 is the case: the section lives in John_08, and
            # 7:53 is only reachable by looking into the neighbouring file.
            # This runs only for a verse nothing else covers, so it costs
            # nothing on the 7,930 verses that are covered outright.
            if not found:
                for neighbour in (chapter + 1, chapter - 1):
                    if any(contains(r, chapter, verse) for r in load(neighbour)):
                        found = True
                        break
            if not found:
                uncovered.append('%s %d:%d' % (code, chapter, verse))

    new = [v for v in uncovered if v not in EXPECTED]

    print('verses in the RCB:      %d' % total)
    print('covered by a section:   %d (%.2f%%)'
          % (total - len(uncovered), 100 * (total - len(uncovered)) / total))
    print('missing exegesis files: %d %s' % (len(missing_files), missing_files[:5]))

    print('\nknown uncovered: %d' % (len(uncovered) - len(new)))
    for reason in dict.fromkeys(EXPECTED.values()):
        hits = [v for v in uncovered if EXPECTED.get(v) == reason]
        if hits:
            span = hits[0] if len(hits) == 1 else '%s .. %s' % (hits[0], hits[-1])
            print('    %-24s %s' % (span, reason))

    print('\nNEW uncovered:   %d' % len(new))
    for v in new[:40]:
        print('    %s' % v)

    return 1 if (new or missing_files) else 0


if __name__ == '__main__':
    sys.exit(main())
