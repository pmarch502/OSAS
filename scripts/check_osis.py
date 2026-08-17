"""Verify osis/nt/*.xml against the markdown it was migrated from.

Four questions, in order of how badly a No would hurt:

  1. Is every file well-formed XML, and does every section carry an
     annotateRef the pane can read?
  2. Is every word of the prose still there? Both sides are stripped back to
     bare text and compared, so a dropped paragraph or a mangled list cannot
     hide behind a section count that still adds up.
  3. Does every verse of the RCB still have commentary? This is the number
     that must not move: 7943 of 7943. The HTML pipeline reached 100% and the
     OSIS has to hold it.
  4. Do the section ranges agree with what the HTML headings resolved to?
     A range that shifted during migration is commentary pointing at the
     wrong passage, which nothing else here would catch.

    python scripts/check_osis.py

Exits non-zero on any failure.
"""
import os
import re
import sys
import glob
import xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = '{http://www.bibletechnologies.net/2003/OSIS/namespace}'

sys.path.insert(0, os.path.join(REPO, 'scripts'))
from check_pane_coverage import (  # noqa: E402
    BOOKS as USFM_BOOKS, rcb_verses, sections as html_sections, contains,
)
from md_to_osis import BOOKS  # noqa: E402


def bare(text):
    """Prose reduced to comparable words.

    Emphasis marks are *deleted*, not blanked. Replacing them with a space
    splits '*conversion*:' into two words on the markdown side and one on the
    OSIS side, which reads as 123 missing words in Galatians that were never
    missing at all.
    """
    text = text.replace('—', '--')
    text = re.sub(r'[*`]', '', text)              # emphasis: remove, no space
    text = re.sub(r'[>|]', ' ', text)             # block marks: separate
    text = re.sub(r'^\s*#+\s*', ' ', text, flags=re.M)
    text = re.sub(r'^\s*\d+[.)]\s+', ' ', text, flags=re.M)
    text = re.sub(r'^\s*[-+]\s+', ' ', text, flags=re.M)
    # Table separator rows. They arrive as '|-----|------|', so by the time the
    # pipes are spaces the row is several tokens on one line and a whole-line
    # anchor never fires. Match the tokens themselves.
    text = re.sub(r'(?<!\S):?-{2,}:?(?!\S)', ' ', text)
    text = re.sub(r'&mdash;', '--', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def osis_text(elem):
    return ''.join(elem.itertext())


def parse_ref(ref):
    """'Rom.8.1-Rom.9.2' or 'Rom.8' -> (sc, sv, ec, ev) or None for chapter."""
    parts = ref.split('-')
    head = parts[0].split('.')
    if len(head) == 2:
        return None
    sc, sv = int(head[1]), int(head[2])
    if len(parts) == 1:
        return sc, sv, sc, sv
    tail = parts[1].split('.')
    return sc, sv, int(tail[1]), int(tail[2])


def main():
    failures = []
    n_sections = n_chapters = 0
    ref_by_book = {}

    # ---- 1. well-formed, and every section annotated ----------------------
    for code, stem, osis_id, name in BOOKS:
        path = os.path.join(REPO, 'osis', 'nt', code + '.xml')
        if not os.path.exists(path):
            failures.append('%s: missing %s' % (code, path))
            continue
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as e:
            failures.append('%s: XML not well-formed -- %s' % (code, e))
            continue

        refs = {}
        for ch_div in root.iter(NS + 'div'):
            if ch_div.get('type') != 'chapter':
                continue
            n_chapters += 1
            chapter = int(ch_div.get('osisID').split('.')[1])
            for sec in ch_div:
                if sec.tag != NS + 'div' or sec.get('type') != 'section':
                    continue
                n_sections += 1
                ref = sec.get('annotateRef')
                if not ref:
                    failures.append('%s %d: section with no annotateRef' % (code, chapter))
                    continue
                if not ref.startswith(osis_id + '.'):
                    failures.append('%s %d: annotateRef %r is not this book' % (code, chapter, ref))
                    continue
                try:
                    rng = parse_ref(ref)
                except (ValueError, IndexError):
                    failures.append('%s %d: unparseable annotateRef %r' % (code, chapter, ref))
                    continue
                refs.setdefault(chapter, []).append(rng)
        ref_by_book[code] = refs

    print('chapters: %d   sections: %d' % (n_chapters, n_sections))

    # ---- 2. prose preserved ----------------------------------------------
    drift = []
    for code, stem, osis_id, name in BOOKS:
        path = os.path.join(REPO, 'osis', 'nt', code + '.xml')
        if not os.path.exists(path):
            continue
        root = ET.parse(path).getroot()
        # The book div only, minus its own title -- the header and the book
        # name are the OSIS's own furniture, not prose carried over.
        book = next(d for d in root.iter(NS + 'div') if d.get('type') == 'book')
        body = [c for c in book if c.tag != NS + 'title']
        got = bare(''.join(osis_text(c) for c in body))

        src = []
        for md in sorted(glob.glob(os.path.join(REPO, 'exegesis', 'nt',
                                                '%s_[0-9][0-9].md' % stem))):
            with open(md, encoding='utf-8-sig') as fh:
                src.append(fh.read())
        want = bare('\n'.join(src))

        # The OSIS drops the '---' section rules and adds the book title, so
        # compare on words rather than on the exact string.
        gw, ww = got.split(), want.split()
        if gw != ww:
            i = next((k for k in range(min(len(gw), len(ww))) if gw[k] != ww[k]),
                     min(len(gw), len(ww)))
            drift.append('%s: %d words in OSIS vs %d in markdown; first differs at %d\n'
                         '        osis: %s\n        md:   %s'
                         % (code, len(gw), len(ww), i,
                            ' '.join(gw[max(0, i - 6):i + 6]),
                            ' '.join(ww[max(0, i - 6):i + 6])))

    if drift:
        failures.extend(drift)
        print('prose preserved:        NO -- %d books differ' % len(drift))
    else:
        print('prose preserved:        yes, all 27 books word-for-word')

    # ---- 3. verse coverage ------------------------------------------------
    total = covered = 0
    uncovered = []
    for code in USFM_BOOKS:
        refs = ref_by_book.get(code, {})
        allr = [r for rs in refs.values() for r in rs if r]
        for chapter, verse in rcb_verses(code):
            total += 1
            if any(contains(r, chapter, verse) for r in allr):
                covered += 1
            else:
                uncovered.append('%s %d:%d' % (code, chapter, verse))

    pct = 100.0 * covered / total if total else 0
    print('verse coverage:         %d/%d (%.2f%%)' % (covered, total, pct))
    if uncovered:
        failures.append('%d verses uncovered, e.g. %s'
                        % (len(uncovered), ', '.join(uncovered[:8])))

    # ---- 4. ranges match what the HTML resolved to -------------------------
    # A range the HTML had and the OSIS does not is commentary going dark, and
    # fails. The reverse is a gain: the HTML checker can only see an <h2> that
    # was given an id by hand, so a section whose heading names its passage but
    # never got an id was invisible to it and is not invisible here.
    lost, gained = [], []
    for code, stem, osis_id, name in BOOKS:
        refs = ref_by_book.get(code, {})
        for chapter in sorted(refs):
            was = html_sections(stem, chapter) or []
            now = [r for r in refs[chapter] if r]
            only_html = [r for r in was if r not in now]
            only_osis = [r for r in now if r not in was]
            if only_html:
                lost.append('%s %d: ranges lost %s' % (code, chapter, only_html[:4]))
            if only_osis:
                gained.append('%s %d: %s' % (code, chapter, only_osis[:4]))

    if lost:
        failures.extend(lost)
        print('ranges kept from HTML:  NO -- %d chapters lost a range' % len(lost))
    else:
        print('ranges kept from HTML:  yes, all 260 chapters')
    if gained:
        print('sections newly visible: %d' % len(gained))
        for g in gained[:10]:
            print('    %s' % g)

    print()
    if failures:
        print('FAILURES: %d' % len(failures))
        for f in failures[:30]:
            print('  - %s' % f)
        return 1
    print('OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
