"""Regenerate RCB data file from USFM source."""
import sys, os

book = sys.argv[1] if len(sys.argv) > 1 else 'GAL'
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(base, 'usfm', 'nt', book + '.usfm')
dst = os.path.join(base, 'docs', 'rcb', 'data', book + '.js')

with open(src, 'r', encoding='utf-8') as f:
    usfm = f.read()

escaped = usfm.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')

with open(dst, 'w', encoding='utf-8') as f:
    f.write('const USFM = `')
    f.write(escaped)
    f.write('`;\n')

fn = usfm.count('\\f +')
print(f'Wrote {dst}: {len(escaped)} chars, {fn} footnotes, {len(usfm.splitlines())} lines')
