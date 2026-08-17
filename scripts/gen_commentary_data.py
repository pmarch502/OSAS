"""Regenerate the commentary data file from OSIS source.

The twin of gen_rcb_data.py, deliberately. The Bible and the commentary are
carried into docs/ the same way -- source at the repo root, a thin wrapper in
the served folder, the viewer parsing the real markup in the browser -- so
there is one pattern to learn rather than two.

    python scripts/gen_commentary_data.py ROM
    python scripts/gen_commentary_data.py --all
"""
import sys
import os
import glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def gen(book):
    src = os.path.join(REPO, 'osis', 'nt', book + '.xml')
    dst = os.path.join(REPO, 'docs', 'commentary', 'data', book + '.js')
    if not os.path.exists(src):
        print('%-5s no OSIS source at %s' % (book, src))
        return False

    with open(src, 'r', encoding='utf-8') as f:
        osis = f.read()

    escaped = osis.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'w', encoding='utf-8', newline='\n') as f:
        f.write('const OSIS = `')
        f.write(escaped)
        f.write('`;\n')

    secs = osis.count('type="section"')
    chs = osis.count('type="chapter"')
    print('%-5s %2d chapters, %4d sections, %8.0fK' % (book, chs, secs, len(escaped) / 1024))
    return True


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    if args == ['--all']:
        books = sorted(os.path.basename(p)[:-4]
                       for p in glob.glob(os.path.join(REPO, 'osis', 'nt', '*.xml')))
    else:
        books = [a.upper() for a in args]

    ok = sum(gen(b) for b in books)
    print('\nwrote %d of %d' % (ok, len(books)))
    return 0 if ok == len(books) else 1


if __name__ == '__main__':
    sys.exit(main())
