"""Build the book/chapter/verse index the RCB reference picker reads.

The picker has to draw chapter blocks for a book, and verse blocks for a
chapter, before that book's text has been loaded -- so it needs the shape of
the canon up front. This walks every USFM file present and records it.

Because it counts what the RCB actually contains, the picker never offers a
verse the RCB omits: Romans has no 16:24, Mark no 11:26, and those simply do
not appear as blocks.

Run after adding or changing any book:

    python scripts/gen_rcb_index.py

Writes docs/rcb/data/index.js.

---------------------------------------------------------------------------
Book identifiers
---------------------------------------------------------------------------
The canonical identifier is the **USFM 3-letter code**, which this project
already uses for USFM filenames, the data files and the ?book= parameter.

Two characters cannot identify a book. Across the 66-book canon the leading
two letters collide seven ways:

    JO -> Joshua, Job, Joel, Jonah, John      MA -> Malachi, Matthew, Mark
    EZ -> Ezra, Ezekiel                       PH -> Philippians, Philemon
    JU -> Judges, Jude                        ZE -> Zephaniah, Zechariah
    HA -> Habakkuk, Haggai

Three leading letters collide only twice -- JUD (Judges/Jude) and PHI
(Philippians/Philemon) -- and the USFM codes exist precisely to break those:
JDG/JUD and PHP/PHM. So the codes below are unique across all 66, which
validate() asserts rather than assumes.

Short input is still convenient without inventing a scheme: the viewer's
parser accepts any *unambiguous* prefix, and 40 of the 66 books resolve in two
characters ("ro", "ga", "ep"). The rest need a third. Ambiguous input resolves
to nothing rather than to a guess.
---------------------------------------------------------------------------
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The whole canon in order: (USFM code, block label, genre).
#
# The label is what the picker prints -- a readable short form, not the code.
# Column widths are fixed by the grid, so a longer label costs no space and
# stays legible for books nobody abbreviates in their head.
#
# Genre drives only the block colour. Several genres deliberately share a
# colour across the testaments (law with gospels, wisdom with the epistles),
# which is why the genre stays semantically accurate here and the CSS does the
# merging.
#
# Books whose USFM file is absent are skipped, so the Old Testament rows below
# simply start appearing as those files land.
CANON = [
    # --- Torah ---
    ('GEN', 'Gen', 'law'), ('EXO', 'Exod', 'law'), ('LEV', 'Lev', 'law'),
    ('NUM', 'Num', 'law'), ('DEU', 'Deut', 'law'),
    # --- History ---
    ('JOS', 'Josh', 'history'), ('JDG', 'Judg', 'history'),
    ('RUT', 'Ruth', 'history'), ('1SA', '1 Sam', 'history'),
    ('2SA', '2 Sam', 'history'), ('1KI', '1 Kings', 'history'),
    ('2KI', '2 Kings', 'history'), ('1CH', '1 Chron', 'history'),
    ('2CH', '2 Chron', 'history'), ('EZR', 'Ezra', 'history'),
    ('NEH', 'Neh', 'history'), ('EST', 'Esth', 'history'),
    # --- Wisdom ---
    ('JOB', 'Job', 'wisdom'), ('PSA', 'Ps', 'wisdom'),
    ('PRO', 'Prov', 'wisdom'), ('ECC', 'Eccles', 'wisdom'),
    ('SNG', 'Song', 'wisdom'),
    # --- Prophets ---
    ('ISA', 'Isa', 'prophets'), ('JER', 'Jer', 'prophets'),
    ('LAM', 'Lam', 'prophets'), ('EZK', 'Ezek', 'prophets'),
    ('DAN', 'Dan', 'prophets'), ('HOS', 'Hos', 'prophets-minor'),
    ('JOL', 'Joel', 'prophets-minor'), ('AMO', 'Amos', 'prophets-minor'),
    ('OBA', 'Obad', 'prophets-minor'), ('JON', 'Jonah', 'prophets-minor'),
    ('MIC', 'Micah', 'prophets-minor'), ('NAM', 'Nahum', 'prophets-minor'),
    ('HAB', 'Hab', 'prophets-minor'), ('ZEP', 'Zeph', 'prophets-minor'),
    ('HAG', 'Hag', 'prophets-minor'), ('ZEC', 'Zech', 'prophets-minor'),
    ('MAL', 'Mal', 'prophets-minor'),
    # --- Gospels and Acts ---
    ('MAT', 'Matt', 'gospel'), ('MRK', 'Mark', 'gospel'),
    ('LUK', 'Luke', 'gospel'), ('JHN', 'John', 'gospel'),
    ('ACT', 'Acts', 'history'),
    # --- Paul ---
    ('ROM', 'Rom', 'epistle'), ('1CO', '1 Cor', 'epistle'),
    ('2CO', '2 Cor', 'epistle'), ('GAL', 'Gal', 'epistle'),
    ('EPH', 'Eph', 'epistle'), ('PHP', 'Phil', 'epistle'),
    ('COL', 'Col', 'epistle'), ('1TH', '1 Thess', 'epistle'),
    ('2TH', '2 Thess', 'epistle'), ('1TI', '1 Tim', 'epistle'),
    ('2TI', '2 Tim', 'epistle'), ('TIT', 'Titus', 'epistle'),
    ('PHM', 'Phlm', 'epistle'),
    # --- General letters ---
    ('HEB', 'Heb', 'general'), ('JAS', 'Jas', 'general'),
    ('1PE', '1 Pet', 'general'), ('2PE', '2 Pet', 'general'),
    ('1JN', '1 John', 'general'), ('2JN', '2 John', 'general'),
    ('3JN', '3 John', 'general'), ('JUD', 'Jude', 'general'),
    # --- Apocalyptic ---
    ('REV', 'Rev', 'apocalyptic'),
]

# Where to look for a book's USFM, in order.
USFM_DIRS = ['nt', 'ot']


def validate():
    """The codes must be unique, or two books collapse into one everywhere."""
    codes = [c for c, _, _ in CANON]
    dupes = {c for c in codes if codes.count(c) > 1}
    if dupes:
        sys.exit('DUPLICATE USFM CODES: %s' % sorted(dupes))

    labels = [l.lower() for _, l, _ in CANON]
    label_dupes = {l for l in labels if labels.count(l) > 1}
    if label_dupes:
        sys.exit('DUPLICATE BLOCK LABELS: %s' % sorted(label_dupes))

    if len(CANON) != 66:
        print('NOTE: canon table has %d books, not 66' % len(CANON))


def usfm_path(code):
    for sub in USFM_DIRS:
        p = os.path.join(REPO, 'usfm', sub, code + '.usfm')
        if os.path.exists(p):
            return p
    return None


def read_book(code, label, genre, path):
    with open(path, encoding='utf-8') as fh:
        text = fh.read()

    name = label
    chapters = {}
    chapter = 0
    for raw in text.split('\n'):
        line = raw.strip()
        m = re.match(r'\\h (.+)', line)
        if m:
            name = m.group(1).strip()
            continue
        m = re.match(r'\\c (\d+)', line)
        if m:
            chapter = int(m.group(1))
            chapters.setdefault(chapter, [])
            continue
        m = re.match(r'\\v (\d+)', line)
        if m and chapter:
            chapters[chapter].append(int(m.group(1)))

    return {
        'name': name,
        'abbrev': label,
        'genre': genre,
        # Verse numbers per chapter, in order, so omitted verses are simply absent.
        'chapters': [chapters[c] for c in sorted(chapters)],
    }


def main():
    validate()

    order = []
    books = {}
    for code, label, genre in CANON:
        path = usfm_path(code)
        if not path:
            continue
        order.append(code)
        books[code] = read_book(code, label, genre, path)

    payload = {'order': order, 'books': books}

    out = os.path.join(REPO, 'docs', 'rcb', 'data', 'index.js')
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write('/* Generated by scripts/gen_rcb_index.py -- do not edit. */\n')
        fh.write('var RCB_INDEX = ')
        json.dump(payload, fh, separators=(',', ':'), ensure_ascii=False)
        fh.write(';\n')

    chapters = sum(len(b['chapters']) for b in books.values())
    verses = sum(len(c) for b in books.values() for c in b['chapters'])
    missing = len(CANON) - len(order)
    print('%d books, %d chapters, %d verses -> docs/rcb/data/index.js (%.0fK)'
          % (len(books), chapters, verses, os.path.getsize(out) / 1024))
    if missing:
        print('%d canon books have no USFM yet and were skipped' % missing)


if __name__ == '__main__':
    main()
