"""Add italics to transliterated Greek and Hebrew in the commentary, safely.

The commentary writes the original languages in Latin letters, inline in the
prose (doulos, pisteos, ho dikaios ek pisteos zesetai). Italicising them is a
reading job, not a search-and-replace job: only a reader can tell the Greek
particle "de" from an English word, and only a reader can see where a Greek
phrase starts and stops. So an agent reads a chapter and marks it.

This script is the safety net around that. It carves one chapter out of a
book, checks the agent's returned copy against the original, and assembles
the marked book only if nothing but italics changed.

    python scripts/italics.py extract ROM 8 stage/ROM.8.xml
    python scripts/italics.py verify  ROM 8 stage/ROM.8.xml
    python scripts/italics.py build   ROM stage/
    python scripts/italics.py report  ROM

osis/nt/ is the source and is opened read-only, always. build writes a whole
new book to osis/nt-italics/{BOOK}.xml, so the marked commentary and the
original sit side by side and can be compared, kept, or thrown away. Nothing
promotes one over the other; that is the author's call.

verify is the whole point. Two conditions, both absolute:

  1. Strip every tag from both sides and the words must be identical. An
     agent that reworded a sentence, dropped a clause, or "improved" a
     heading fails here.
  2. Line up the tag sequences. The new one may only have <hi type="italic">
     and its </hi> inserted. Anything else moved, dropped, or invented fails.

build runs the check on every chapter and refuses to write the book if one
fails, so a bad agent run costs nothing but the agent.
"""

import collections
import difflib
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The words being marked are full of macrons (pisteōs, dikaiosynē) and the
# Windows console is cp1252, so printing a report kills the script mid-run.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TAG = re.compile(r"<[^>]+>")
INLINE = re.compile(r"</?hi\b[^>]*>")
ITALIC_OPEN = '<hi type="italic">'
ITALIC_CLOSE = "</hi>"

SRC = os.path.join(REPO, "osis", "nt")
OUT = os.path.join(REPO, "osis", "nt-italics")


def book_path(book):
    return os.path.join(SRC, book + ".xml")


def out_path(book):
    return os.path.join(OUT, book + ".xml")


def chapter_bounds(lines, book, chapter):
    """Line range of one chapter div. The files indent chapter divs by six
    spaces and nothing else, checked across all 260, so this is exact."""
    opener = '      <div type="chapter" osisID='
    want = '.%s"' % chapter
    start = None
    for i, line in enumerate(lines):
        if start is None:
            if line.startswith(opener) and line.rstrip().endswith(want + ">"):
                start = i
        elif line.startswith("      </div>"):
            return start, i + 1
    if start is None:
        sys.exit("no chapter div for %s %s" % (book, chapter))
    sys.exit("chapter div for %s %s is not closed" % (book, chapter))


def read_chapter(book, chapter):
    with open(book_path(book), encoding="utf-8") as fh:
        lines = fh.readlines()
    a, b = chapter_bounds(lines, book, chapter)
    return lines, a, b


def words(xml):
    """Everything the reader sees, with markup and layout removed.

    <hi> is inline and sits tight against the words, so it is deleted rather
    than spaced out -- otherwise wrapping sarx in italics turns "(sarx)" into
    "( sarx )" and the comparison reports a prose change that never happened.
    Every other tag is block-level and becomes a space.
    """
    return re.sub(r"\s+", " ", TAG.sub(" ", INLINE.sub("", xml))).strip()


def tags(xml):
    return TAG.findall(xml)


ITALIC_SPAN = re.compile(r'<hi type="italic">(.*?)</hi>', re.S)


def unitalic(xml):
    """The chapter with every italic wrapper peeled off, inner text kept.

    This is the whole test. Peel the italics off both sides and the two files
    must come out byte-for-byte identical -- same words, same punctuation,
    same <p>, same <hi type="bold">, same indentation, same line breaks.
    Anything the agent touched other than italics shows up here.

    Do not go back to diffing the tag sequence. That was tried and it reports
    false failures: an inserted italic sits between existing <p> tags and
    difflib lines the two lists up differently rather than calling it a clean
    insertion. It failed a chapter that was in fact perfect.
    """
    while True:
        peeled = ITALIC_SPAN.sub(r"\1", xml)
        if peeled == xml:
            return xml
        xml = peeled


def check(before, after):
    """Return a list of complaints. Empty means only italics were added."""
    bad = []

    ub, ua = unitalic(before), unitalic(after)
    if ub != ua:
        bad.append("THE CHAPTER CHANGED -- this is a rejection, not a warning.")
        wb, wa = words(ub).split(), words(ua).split()
        if wb != wa:
            bad.append("  the prose itself differs:")
            shown = 0
            for op, i1, i2, j1, j2 in difflib.SequenceMatcher(
                    None, wb, wa).get_opcodes():
                if op == "equal" or shown >= 5:
                    continue
                bad.append("    was: %s" % " ".join(wb[i1:i2])[:200])
                bad.append("    now: %s" % " ".join(wa[j1:j2])[:200])
                shown += 1
        else:
            bad.append("  the words match, so it is markup or layout:")
            for line in list(difflib.unified_diff(
                    ub.splitlines(), ua.splitlines(),
                    "original", "marked", n=0))[:12]:
                bad.append("    %s" % line[:200])
        return bad

    kept = collections.Counter(spans(before))
    kept.subtract(collections.Counter(spans(after)))
    lost = [s for s, n in kept.items() if n > 0]
    if lost:
        bad.append("an italic that was already there was removed: %s" % lost[:5])

    if len(spans(after)) <= len(spans(before)):
        bad.append("nothing was italicised -- the agent did no work.")
    return bad


def spans(xml):
    """Every italicised string, in order."""
    return re.findall(r'<hi type="italic">(.*?)</hi>', xml, re.S)


def cmd_extract(book, chapter, out):
    lines, a, b = read_chapter(book, chapter)
    with open(out, "w", encoding="utf-8") as fh:
        fh.writelines(lines[a:b])
    print("%s %s -> %s (%d lines)" % (book, chapter, out, b - a))


def cmd_verify(book, chapter, new, quiet=False):
    lines, a, b = read_chapter(book, chapter)
    before = "".join(lines[a:b])
    with open(new, encoding="utf-8") as fh:
        after = fh.read()

    bad = check(before, after)
    if bad:
        print("FAIL %s %s" % (book, chapter))
        for line in bad:
            print(line)
        return 1

    fresh = len(spans(after)) - len(spans(before))
    print("OK %s %s -- %d italics added, prose untouched" % (book, chapter, fresh))
    if not quiet:
        for s in spans(after)[:400]:
            print("   %s" % s)
    return 0


def chapters(book):
    """Every chapter number in the book, in file order."""
    found = []
    with open(book_path(book), encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r'\s*<div type="chapter" osisID="[^."]+\.(\d+)"', line)
            if m:
                found.append(m.group(1))
    return found


def cmd_build(book, stage):
    """Assemble the marked book into osis/nt-italics/. The source in
    osis/nt/ is opened read-only and is never written."""
    with open(book_path(book), encoding="utf-8") as fh:
        lines = fh.readlines()

    done, missing, failed, added = [], [], [], 0
    for ch in chapters(book):
        marked = os.path.join(stage, "%s.%s.xml" % (book, ch))
        if not os.path.exists(marked):
            missing.append(ch)
            continue
        a, b = chapter_bounds(lines, book, ch)
        before = "".join(lines[a:b])
        with open(marked, encoding="utf-8") as fh:
            after = fh.read()
        bad = check(before, after)
        if bad:
            failed.append((ch, bad))
            continue
        if not after.endswith("\n"):
            after += "\n"
        added += len(spans(after)) - len(spans(before))
        lines[a:b] = [after]
        done.append(ch)

    for ch, bad in failed:
        print("FAIL %s %s" % (book, ch))
        for line in bad:
            print("   %s" % line)

    if failed:
        print("%s NOT BUILT -- %d chapter(s) failed the check" % (book, len(failed)))
        return 1

    os.makedirs(OUT, exist_ok=True)
    with open(out_path(book), "w", encoding="utf-8", newline="") as fh:
        fh.writelines(lines)
    print("%s -> osis/nt-italics/%s.xml -- %d of %d chapters marked, %d italics added"
          % (book, book, len(done), len(chapters(book)), added))
    if missing:
        print("   not yet marked, copied through unchanged: %s" % ", ".join(missing))
    return 0


def cmd_report(book):
    path = out_path(book) if os.path.exists(out_path(book)) else book_path(book)
    print("(reading %s)" % os.path.relpath(path, REPO))
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    seen = {}
    for s in spans(text):
        s = re.sub(r"\s+", " ", s).strip()
        seen[s] = seen.get(s, 0) + 1
    print("%s -- %d italic spans, %d distinct" % (book, sum(seen.values()), len(seen)))
    for s, n in sorted(seen.items(), key=lambda kv: (-kv[1], kv[0])):
        print("%5d  %s" % (n, s))
    return 0


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd = argv[0]
    if cmd == "report":
        return cmd_report(argv[1])
    if cmd == "build":
        if len(argv) != 3:
            sys.exit(__doc__)
        return cmd_build(argv[1], argv[2])
    if len(argv) != 4:
        sys.exit(__doc__)
    book, chapter, path = argv[1], argv[2], argv[3]
    if cmd == "extract":
        return cmd_extract(book, chapter, path)
    if cmd == "verify":
        return cmd_verify(book, chapter, path)
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
