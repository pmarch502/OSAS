"""Verify the OSIS commentary is structurally sound.

    python scripts/check_osis.py            # all books
    python scripts/check_osis.py ROM        # one book

Run it after writing or editing any osis/nt/{BOOK}.xml. It answers the
questions that would otherwise fail silently in the viewer:

  1. Is the file well-formed XML?
  2. Does every section carry an annotateRef, and does that reference name
     this book? A section without one is invisible to the pane.
  3. Is every reference parseable, in range, and pointing forward rather than
     backward?
  4. Does every section have a title and a body? An empty section renders as a
     heading with nothing under it.
  5. Are the elements ones the viewer knows how to render? Anything else falls
     through to its text in the browser, which is survivable but not intended.

It deliberately does *not* check verse coverage -- that is
check_pane_coverage.py, which walks the USFM rather than the OSIS and so can
see a verse nothing covers. Run both.

Two earlier checks are gone with the sources they compared against: the prose
was verified word-for-word against exegesis/nt/*.md, and section ranges against
the ids in docs/exegesis/nt/*.html, during the one-time migration. The OSIS is
the source now, so there is nothing left to compare it to.
"""
import os
import sys
import glob
import xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = '{http://www.bibletechnologies.net/2003/OSIS/namespace}'

# What docs/commentary/osis.js renders. Anything outside this set still shows
# its text, but as unstyled prose -- a table would lose its rows.
KNOWN = {'p', 'title', 'hi', 'list', 'item', 'table', 'row', 'cell', 'div'}


def parse_ref(ref):
    parts = ref.split('-')
    head = parts[0].split('.')
    if len(head) < 3:
        return None
    sc, sv = int(head[1]), int(head[2])
    if len(parts) == 1:
        return sc, sv, sc, sv
    tail = parts[1].split('.')
    return sc, sv, int(tail[1]), int(tail[2])


def check(path):
    book = os.path.basename(path)[:-4]
    problems = []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return book, 0, 0, ['XML is not well-formed: %s' % e]

    books = [d for d in root.iter(NS + 'div') if d.get('type') == 'book']
    if len(books) != 1:
        problems.append('expected exactly one book div, found %d' % len(books))
        return book, 0, 0, problems

    osis_id = books[0].get('osisID')
    n_ch = n_sec = 0

    for ch in books[0]:
        if ch.tag != NS + 'div' or ch.get('type') != 'chapter':
            continue
        n_ch += 1
        cid = ch.get('osisID') or ''
        try:
            chapter = int(cid.split('.')[1])
        except (IndexError, ValueError):
            problems.append('chapter div has an unusable osisID %r' % cid)
            continue

        for sec in ch:
            if sec.tag != NS + 'div' or sec.get('type') != 'section':
                continue
            n_sec += 1
            where = '%s %d' % (book, chapter)

            ref = sec.get('annotateRef')
            if not ref:
                problems.append('%s: a section has no annotateRef' % where)
                continue
            if not ref.startswith(osis_id + '.'):
                problems.append('%s: annotateRef %r does not name this book' % (where, ref))
                continue

            try:
                rng = parse_ref(ref)
            except (ValueError, IndexError):
                problems.append('%s: annotateRef %r will not parse' % (where, ref))
                continue

            if rng:
                sc, sv, ec, ev = rng
                if (ec, ev) < (sc, sv):
                    problems.append('%s: annotateRef %r ends before it starts' % (where, ref))
                # A section may reach into the chapter next door, and two do:
                # John 8 carries 7:53-8:11, and 2 Corinthians 6 closes with a
                # section on 7:1 because the passage is 6:14-7:1. Anything
                # further away is a mistake, not a passage that straddles.
                if min(abs(sc - chapter), abs(ec - chapter)) > 1:
                    problems.append('%s: annotateRef %r is not in or beside its '
                                    'own chapter' % (where, ref))

            titles = [c for c in sec if c.tag == NS + 'title']
            body = [c for c in sec if c.tag != NS + 'title']
            if not titles or not (titles[0].text or '').strip():
                problems.append('%s: section %r has no title' % (where, ref))
            if not body:
                problems.append('%s: section %r has no body' % (where, ref))

            for el in sec.iter():
                name = el.tag.replace(NS, '')
                if name not in KNOWN:
                    problems.append('%s: section %r contains <%s>, which the '
                                    'viewer does not render' % (where, ref, name))

    return book, n_ch, n_sec, problems


def main():
    wanted = [a.upper() for a in sys.argv[1:]]
    paths = sorted(glob.glob(os.path.join(REPO, 'osis', 'nt', '*.xml')))
    if wanted:
        paths = [p for p in paths if os.path.basename(p)[:-4] in wanted]
    if not paths:
        print('no OSIS files found')
        return 1

    tot_ch = tot_sec = 0
    failures = []
    for path in paths:
        book, n_ch, n_sec, problems = check(path)
        tot_ch += n_ch
        tot_sec += n_sec
        flag = 'FAIL' if problems else 'ok'
        print('%-5s %2d chapters %4d sections  %s' % (book, n_ch, n_sec, flag))
        failures.extend(problems)

    print('\nbooks: %d   chapters: %d   sections: %d' % (len(paths), tot_ch, tot_sec))
    if failures:
        print('\nFAILURES: %d' % len(failures))
        for f in failures[:40]:
            print('  - %s' % f)
        return 1
    print('OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
