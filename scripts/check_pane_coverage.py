"""Check that the commentary pane can find a section for every verse the RCB has.

The pane syncs by verse containment: it takes the verse at the reading line and
shows the section whose range contains it. Where no section contains it the pane
says so honestly, but each such verse is a stretch of text with no commentary,
so they are worth knowing about and worth not growing.

    python scripts/check_pane_coverage.py

Exits non-zero if an uncovered verse appears that is not in EXPECTED below.

This walks the same path the viewer does -- every verse in usfm/nt/{BOOK}.usfm
against the section ranges in osis/nt/{BOOK}.xml -- so it catches interior gaps,
chapters whose commentary starts late, and verses running past the last section
alike.

**A gap used to mean two different things and now means one.** Until the
commentary moved to OSIS the range was parsed out of the section's heading text,
and three times running a reported gap turned out to be a heading this checker
could not read sitting on top of analysis that was written all along:

    Titus 2:7-10      the section covered 2-10, with subsections on the younger
                      men (6-8) and on slaves (9-10). Only its heading said
                      "Verses 2-6". Fixed 2026-08-13.
    John 7:53-8:11    John_08 carried a full reading of the passage under the
                      heading "A Note on 7:53-8:11" -- the entrapment between
                      Rome's monopoly on capital sentences and Moses, the
                      missing man of Deuteronomy 22:22, the witnesses casting
                      first at Deuteronomy 17:7. The heading did not begin
                      "Verses", so it got no id, and a section the pane never
                      looked at was recorded as the commentary having "not gone
                      there". Fixed 2026-08-17.
    Revelation 12:18  the clause was discussed in Revelation_13 under "Context
                      and Placement", which carried no verse range. That was the
                      Textus Receptus framing, where the clause is 13:1a and the
                      one standing is the seer. The RCB follows the earlier
                      witnesses -- the dragon stands, and it is the last beat of
                      chapter 12 -- so Revelation 12's closing section now runs
                      13-18. Fixed 2026-08-17.

annotateRef states the passage outright, so that whole class of false gap is
gone: a gap here now means the commentary genuinely does not cover the verse.
It is still worth reading the neighbouring chapter's sections before believing
one -- analysis of a passage straddling a chapter boundary is written in one
chapter and belongs to both, and the OSIS says so with a range like
John.7.53-John.8.11.
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = '{http://www.bibletechnologies.net/2003/OSIS/namespace}'

# USFM code -> OSIS book id. The file is named for the USFM code so the
# commentary sits beside the Bible under the same name; annotateRef speaks the
# OSIS id.
BOOKS = {
    'MAT': 'Matt', 'MRK': 'Mark', 'LUK': 'Luke', 'JHN': 'John', 'ACT': 'Acts',
    'ROM': 'Rom', '1CO': '1Cor', '2CO': '2Cor', 'GAL': 'Gal', 'EPH': 'Eph',
    'PHP': 'Phil', 'COL': 'Col', '1TH': '1Thess', '2TH': '2Thess',
    '1TI': '1Tim', '2TI': '2Tim', 'TIT': 'Titus', 'PHM': 'Phlm', 'HEB': 'Heb',
    'JAS': 'Jas', '1PE': '1Pet', '2PE': '2Pet', '1JN': '1John', '2JN': '2John',
    '3JN': '3John', 'JUD': 'Jude', 'REV': 'Rev',
}

# Verses the RCB carries that no section covers. Empty, and it should stay that
# way -- every verse of the RCB has commentary behind it.
EXPECTED = {}


def parse_ref(ref):
    """'Rom.8.1-Rom.8.4' -> (8, 1, 8, 4). None for a chapter-level section."""
    parts = ref.split('-')
    head = parts[0].split('.')
    if len(head) < 3:
        return None
    sc, sv = int(head[1]), int(head[2])
    if len(parts) == 1:
        return sc, sv, sc, sv
    tail = parts[1].split('.')
    return sc, sv, int(tail[1]), int(tail[2])


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


def sections(code):
    """Every verse range the commentary for this book covers, or None."""
    path = os.path.join(REPO, 'osis', 'nt', code + '.xml')
    if not os.path.exists(path):
        return None
    out = []
    for div in ET.parse(path).getroot().iter(NS + 'div'):
        if div.get('type') != 'section':
            continue
        ref = div.get('annotateRef')
        if not ref:
            continue
        rng = parse_ref(ref)
        if rng:
            out.append(rng)
    return out


def main():
    total = 0
    uncovered = []
    missing_files = []

    for code in BOOKS:
        verses = rcb_verses(code)
        total += len(verses)
        ranges = sections(code)
        if ranges is None:
            missing_files.append(code)
            ranges = []
        for chapter, verse in verses:
            if not any(contains(r, chapter, verse) for r in ranges):
                uncovered.append('%s %d:%d' % (code, chapter, verse))

    new = [v for v in uncovered if v not in EXPECTED]

    print('verses in the RCB:      %d' % total)
    print('covered by a section:   %d (%.2f%%)'
          % (total - len(uncovered), 100 * (total - len(uncovered)) / total))
    print('missing OSIS files:     %d %s' % (len(missing_files), missing_files[:5]))

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
