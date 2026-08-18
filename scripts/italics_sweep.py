"""The word-set sweep: every word this book italicises somewhere, found
sitting unmarked somewhere else.

Needs no guess about what Greek looks like. It found the one real miss in
Acts' 4,996 spans (`hoi adelphoi`, left plain twice in Acts 17).

Read the list rather than trusting it. Most lines are correct by design --
`Life` the Josephus title beside "life" the English word, a name italicised
only inside a Greek phrase, a term deliberately left plain in its English
sense. The job is to spot the one line that has no such explanation.

    python scripts/italics_sweep.py 1CO
"""
import io
import re
import sys
import unicodedata

ITALIC = re.compile(r'<hi type="italic">(.*?)</hi>', re.S)
TAG = re.compile(r"<[^>]+>")
WORD = re.compile(r"[^\W\d_]+", re.U)

# Words that carry an English sense as well, so a plain occurrence proves
# nothing. Extend rather than loosening the match.
SKIP = {
    "a", "e", "he", "hen", "his", "in", "is", "it", "kai", "me", "no", "on",
    "one", "so", "son", "the", "to", "us", "was", "an", "and", "are", "as",
    "at", "be", "by", "de", "do", "for", "go", "had", "has", "if", "not",
    "of", "or", "out", "own", "sun", "ten", "that", "this", "up", "we",
    "life", "time", "men", "man", "god", "lord", "christ", "jesus", "paul",
    "peter", "john", "law", "word", "come", "die", "end", "eye", "far",
    "hand", "here", "hope", "into", "love", "made", "may", "mind", "more",
    "new", "now", "old", "our", "part", "same", "see", "self", "some",
    "than", "them", "then", "they", "true", "way", "were", "what", "when",
    "who", "will", "with", "you", "your",
}


def fold(w):
    """Strip accents and case so `sōma` and `soma` are the same word."""
    n = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in n if not unicodedata.combining(c))


def main(book):
    path = "osis/nt-italics/%s.xml" % book
    xml = io.open(path, encoding="utf-8").read()

    marked = set()
    for span in ITALIC.findall(xml):
        for w in WORD.findall(TAG.sub("", span)):
            f = fold(w)
            if len(f) > 2 and f not in SKIP:
                marked.add(f)

    plain = TAG.sub("\x00", ITALIC.sub("\x00", xml))
    hits = {}
    for line_no, line in enumerate(plain.split("\n"), 1):
        for w in WORD.findall(line):
            f = fold(w)
            if f in marked:
                hits.setdefault(f, []).append(line_no)

    if not hits:
        print("%s -- clean, nothing italicised elsewhere sits plain" % book)
        return 0

    print("%s -- %d word(s) italicised somewhere and plain elsewhere\n" % (book, len(hits)))
    for f in sorted(hits):
        where = hits[f]
        print("  %-24s %d plain  (lines %s%s)" % (
            f, len(where), ", ".join(str(n) for n in where[:6]),
            ", ..." if len(where) > 6 else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1].upper()))
