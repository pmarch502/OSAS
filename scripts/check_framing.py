"""Scan the neutral readings for post-first-century framing vocabulary.

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
exegesis *refusing* the category ("this is not legalism but consistency") or
quoting a text that contains it (James 2:24, "not by faith alone").

Two terms were tried and dropped as pure noise: "merit" (64 hits, nearly all
"unmerited favor" glossing charis) and "forensic" (28, mostly actual Roman
courtrooms -- Acts 24 is a trial). Don't add them back.
"""
import re
import sys
import glob
import os
import collections

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
    hits = []
    files = sorted(glob.glob(pattern))
    for path in files:
        text = open(path, encoding='utf-8').read()
        name = os.path.basename(path)[:-3]
        for rx, pat, why in COMPILED:
            for m in rx.finditer(text):
                line = text.count('\n', 0, m.start()) + 1
                s, e = max(0, m.start() - 95), min(len(text), m.end() + 95)
                hits.append((name, line, m.group(0), pat, why,
                             ' '.join(text[s:e].split())))
    return files, hits


def main():
    show_context = '--context' in sys.argv
    files, hits = scan('exegesis/nt/*.md')

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
        for name, line, found, pat, why, ctx in hits:
            print('\n%s:%d  [%s] -- %s' % (name, line, found, why))
            print('    ...%s...' % ctx)

    # Never fails the build. Every hit needs a human, and most are innocent.
    return 0


if __name__ == '__main__':
    sys.exit(main())
