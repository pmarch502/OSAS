"""Peel the italics off named words in a book already marked.

Written for the tractate ruling of 2026-08-17: the collection (Mishnah,
Didache) keeps its italics, the tractate inside it (Berakhot, Avot, Bava
Metzia) does not, because a tractate is a book of the collection and the
project's settled rule leaves book names plain. Talmud and Shema go plain for
the same reason -- they read as English now, like Torah.

    python scripts/italics_unmark.py ROM GAL ACT MAT

It only ever deletes an italic wrapper. It never touches prose, and it proves
that: after the edit, stripping every italic from the result must reproduce
osis/nt/{BOOK}.xml byte for byte, exactly as scripts/italics.py verify does.
A book that fails is left on disk unchanged.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from italics import book_path, out_path, spans, unitalic  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

# Tractates of the Mishnah and Talmud, plus the two collection-level words the
# earlier runs treated inconsistently. Add to this list, do not generalise it:
# a name here is unmarked wherever it stands alone in a span.
PLAIN = [
    "Berakhot", "Peah", "Demai", "Kilayim", "Sheviit", "Terumot", "Maasrot",
    "Challah", "Orlah", "Bikkurim", "Shabbat", "Eruvin", "Pesachim",
    "Shekalim", "Yoma", "Sukkah", "Beitzah", "Rosh Hashanah", "Taanit",
    "Megillah", "Moed Katan", "Chagigah", "Yevamot", "Ketubot", "Nedarim",
    "Nazir", "Sotah", "Gittin", "Kiddushin", "Bava Qamma", "Bava Kamma",
    "Bava Metzia", "Bava Batra", "Sanhedrin", "Makkot", "Shevuot", "Eduyot",
    "Avodah Zarah", "Avot", "Horayot", "Zevachim", "Menachot", "Chullin",
    "Bekhorot", "Arakhin", "Temurah", "Keritot", "Meilah", "Tamid", "Middot",
    "Kinnim", "Kelim", "Oholot", "Negaim", "Parah", "Tohorot", "Mikvaot",
    "Niddah", "Makhshirin", "Zavim", "Yadayim", "Uktzin",
    "Talmud", "Shema",
    # Naturalised in English exactly as Torah is, and the books bear that out:
    # Revelation leaves menorah plain 10 times and marked it once.
    "menorah", "Menorah",
]


def unmark(text, words):
    """Delete the wrapper where a span is exactly one of these words.

    The span must be the whole of what was italicised. A tractate inside a
    longer title -- were one ever marked that way -- is left alone rather than
    silently cut in half.
    """
    hit = {}

    def drop(m):
        inner = m.group(1)
        bare = re.sub(r"\s+", " ", inner).strip()
        if bare in words:
            hit[bare] = hit.get(bare, 0) + 1
            return inner
        return m.group(0)

    return re.sub(r'<hi type="italic">(.*?)</hi>', drop, text, flags=re.S), hit


def main(books):
    if not books:
        sys.exit(__doc__)
    bad = 0
    for book in books:
        path = out_path(book)
        if not os.path.exists(path):
            print("%s -- not marked yet, skipped" % book)
            continue
        with open(path, encoding="utf-8") as fh:
            before = fh.read()
        after, hit = unmark(before, set(PLAIN))

        if not hit:
            print("%s -- nothing to unmark" % book)
            continue

        with open(book_path(book), encoding="utf-8") as fh:
            source = fh.read()
        # Strip italics from BOTH sides. Galatians and Matthew carry italics
        # in osis/nt/ already, so comparing against the raw source fails a
        # book that is in fact untouched.
        if unitalic(after) != unitalic(source):
            print("%s -- REFUSED: the result no longer matches osis/nt/%s.xml"
                  % (book, book))
            bad = 1
            continue
        # An italic the commentary already had must survive. GAL has 189.
        lost = set(spans(source)) - set(spans(after))
        if lost:
            print("%s -- REFUSED: it would drop a pre-existing italic: %s"
                  % (book, sorted(lost)[:5]))
            bad = 1
            continue

        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(after)
        total = sum(hit.values())
        print("%s -- %d span(s) unmarked: %s"
              % (book, total, ", ".join("%s x%d" % (w, n)
                                        for w, n in sorted(hit.items()))))
    return bad


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
