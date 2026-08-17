"""Scan the commentary for post-first-century framing vocabulary.

This is NOT a bias detector, and passing it proves nothing about neutrality.
It catches one specific failure: reaching for a category that only exists
downstream of the text -- Reformation polemics, medieval divisions of Torah,
later systematics -- and using it as though it were the plain sense.

It exists because the alternative on offer was reviewing 260 chapters word by
word. A word list cannot see framing drift (emphasis, which reading is treated
as natural, which options go unmentioned), and that is the harder problem. But
it clears the loud cases across the whole corpus in a second, which is enough
to say where a human should not have to look.

Usage:
    python scripts/check_framing.py            # NT
    python scripts/check_framing.py --context  # with surrounding text

Every hit needs reading before it means anything. Most legitimate uses are the
commentary *refusing* the category ("this is not legalism but consistency") or
quoting a text that contains it (James 2:24, "not by faith alone").

A hit is reported against the section it sits in, not a line number: the source
is osis/nt/{BOOK}.xml, where one file holds a whole book and a line number would
say nothing useful.

Two terms were tried and dropped as pure noise: "merit" (64 hits, nearly all
"unmerited favor" glossing charis) and "forensic" (28, mostly actual Roman
courtrooms -- Acts 24 is a trial). Don't add them back.
"""
import re
import sys
import glob
import os
import collections
import xml.etree.ElementTree as ET

NS = '{http://www.bibletechnologies.net/2003/OSIS/namespace}'

# Vocabulary with no first-century referent. The value is why it is a flag.
TERMS = {
    r'legalis(m|tic)': 'modern label, no first-century referent',
    r'antinomian\w*': 'later polemic',
    r'sola fide': 'Reformation slogan',
    r'faith alone': 'Reformation slogan (legitimate when quoting James 2:24)',
    r'(moral|ceremonial) law': 'medieval tripartite division of Torah',
    r'Judaiz(er|ers|ing)': 'modern coinage for a party the text never names so',
    r'imput(ed|ation)': 'forensic category from later systematics',
    r'covenant of (works|grace)': 'federal theology',
    r'ordo salutis': 'later systematics',
    r'total depravity': 'later systematics',
    r'irresistible grace': 'later systematics',
    r'abolish(ed|es) the (law|Torah)': 'a claim about Torah itself, not a function of it',
    r'the (law|Torah) (is|was) (temporary|abolished|obsolete)': 'Torah itself, not its custodial role',
    r'earn(s|ed)? (his|her|their|our|your) (own )?(salvation|righteousness|favou?r)':
        'framing rather than exegesis',
}

COMPILED = [(re.compile(p, re.I), p, why) for p, why in TERMS.items()]


def scan(pattern):
    """-> (chapters scanned, hits). A hit is (where, section, found, pattern,
    why, context)."""
    hits = []
    chapters = []
    for path in sorted(glob.glob(pattern)):
        book = os.path.basename(path)[:-4]
        for ch in ET.parse(path).getroot().iter(NS + 'div'):
            if ch.get('type') != 'chapter':
                continue
            where = '%s %s' % (book, (ch.get('osisID') or '.?').split('.')[-1])
            chapters.append(where)
            for sec in ch:
                if sec.tag != NS + 'div' or sec.get('type') != 'section':
                    continue
                title = next((c.text or '' for c in sec if c.tag == NS + 'title'), '')
                text = ' '.join(''.join(sec.itertext()).split())
                for rx, pat, why in COMPILED:
                    for m in rx.finditer(text):
                        s, e = max(0, m.start() - 95), min(len(text), m.end() + 95)
                        hits.append((where, title.strip(), m.group(0), pat, why,
                                     text[s:e]))
    return chapters, hits


def main():
    show_context = '--context' in sys.argv
    files, hits = scan('osis/nt/*.xml')

    by_file = collections.Counter(h[0] for h in hits)
    by_term = collections.Counter(h[3] for h in hits)

    print('scanned %d chapters' % len(files))
    print('hits:    %d across %d chapters\n' % (len(hits), len(by_file)))

    if by_term:
        print('BY TERM')
        for pat, n in by_term.most_common():
            print('  %4d  %-42s %s' % (n, pat, TERMS[pat]))
        print('\nBY CHAPTER')
        for name, n in by_file.most_common():
            print('  %4d  %s' % (n, name))

    if show_context:
        print('\nHITS')
        for name, section, found, pat, why, ctx in hits:
            print('\n%s  %s  [%s] -- %s' % (name, section, found, why))
            print('    ...%s...' % ctx)

    # Never fails the build. Every hit needs a human, and most are innocent.
    return 0


if __name__ == '__main__':
    sys.exit(main())
