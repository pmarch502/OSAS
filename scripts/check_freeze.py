"""Verify that RCB pass 2 left the pass-1 translation untouched.

    python scripts/check_freeze.py GAL

Strips the five amplification markers back out of the finished book and
compares what is left against the pass-1 file, line for line. Prints the
number of real differences; 0 means the freeze held.

Must run before the pass-1 intermediate is deleted — it is the only baseline.

Removing an \\add that sat before a comma leaves a stray space, so both sides
are normalized for whitespace before punctuation. A line-count mismatch means
pass 2 inserted or removed a line, almost always a \\p added to carry a heading.
"""

import re
import sys

PASS2_LINE = re.compile(r"\\(s1|imt|ip)\b")
ADD_SPAN = re.compile(r"\\add .*?\\add\*")
NOTE_SPAN = re.compile(r"\\f \+.*?\\f\*")
BEFORE_PUNCT = re.compile(r"\s+([,.;:!?)\u2014])")


def base_text(path):
    """The book with every pass-2 addition stripped away."""
    lines = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if PASS2_LINE.match(line):
                continue
            line = ADD_SPAN.sub("", line)
            line = NOTE_SPAN.sub("", line)
            line = re.sub(r"\s+", " ", line).strip()
            if line:
                lines.append(line)
    return lines


def normalize(line):
    return BEFORE_PUNCT.sub(r"\1", line)


def main(book):
    pass1 = "usfm/nt/%s-pass1.usfm" % book
    try:
        before = base_text(pass1)
    except IOError:
        sys.exit("%s is gone, so the freeze can no longer be checked for %s.\n"
                 "Run this before deleting the intermediate at publish time."
                 % (pass1, book))
    after = base_text("usfm/nt/%s.usfm" % book)

    if len(before) != len(after):
        print("LINE COUNT CHANGED: pass 1 has %d, finished book has %d"
              % (len(before), len(after)))
        print("Pass 2 added or removed a line — look for an inserted \\p.")

    diffs = [(i, b, a) for i, (b, a) in enumerate(zip(before, after))
             if normalize(b) != normalize(a)]

    print("%d" % len(diffs))
    for i, b, a in diffs[:10]:
        print("--- line %d" % i)
        print("pass 1: %s" % b)
        print("book:   %s" % a)

    return 1 if (diffs or len(before) != len(after)) else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python scripts/check_freeze.py {BOOK}")
    sys.exit(main(sys.argv[1]))
