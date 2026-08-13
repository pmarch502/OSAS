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

# Verses the RCB carries that no exegesis section covers. Both are places where
# the RCB followed the printed NA28 and the exegesis did not go, not parsing
# failures.
#
# Titus 2:7-10 used to sit here as "no exegesis section written". That was
# wrong: the section covers 2-10 and carries subsections on the younger men
# (6-8) and on slaves (9-10). Only its heading said "Verses 2-6", and this
# checker reads ranges from heading text, so a mislabelled heading invented a
# four-verse hole. Fixed 2026-08-13. Suspect the heading before believing a
# gap.
EXPECTED = {
    'JHN 7:53': 'pericope adulterae -- John_07 ends at 7:52, John_08 starts at 8:12',
    'REV 12:18': 'NA28 numbers it separately; the exegesis treats it under 13:1',
}
for _v in range(1, 12):
    EXPECTED['JHN 8:%d' % _v] = EXPECTED['JHN 7:53']


def parse_heading_range(text, ident):
    """Mirror parseHeadingRange() in docs/index.html.

    A section starting or ending mid-verse has an id holding only its first
    verse token ('Verses 16b-18' carries id="16"), so the heading text is the
    authority and the id is the fallback. Reading the ids alone left 31 phantom
    gaps across the NT.
    """
    m = HEADING.match(text.strip())
    if m:
        return int(m.group(1)), int(m.group(2) or m.group(1))
    n = RANGE.match(ident.strip())
    if n:
        return int(n.group(1)), int(n.group(2) or n.group(1))
    return None


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
        r = parse_heading_range(text, ident)
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
        for chapter, verse in verses:
            if chapter not in cache:
                cache[chapter] = sections(stem, chapter)
                if cache[chapter] is None:
                    missing_files.append('%s %d' % (stem, chapter))
            found = any(s <= verse <= e for s, e in (cache[chapter] or []))
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
