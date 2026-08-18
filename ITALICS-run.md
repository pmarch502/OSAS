# The italics pass — state and how to resume

Marking the commentary's transliterated Greek, Hebrew and Aramaic, its Latin
scholarly terms, and the titles of ancient works, so a reader can see at a
glance which words are not English.

**This is a typographic pass over finished prose. It never edits the
commentary.** The rule is enforced mechanically, not trusted — see "The
check" below.

## Promoted, 2026-08-18

**The marked books replaced `osis/nt/`, and `docs/commentary/data/` was
regenerated from them.** The italics are now the commentary. The author's
call, made once the whole NT was marked and the peel-and-compare check
came back clean on all 27 books.

`osis/nt-italics/` and `preview/` were deleted with it -- the first had
become a byte-for-byte duplicate of the source, the second described a
staging step that no longer exists.

**What that means for the scripts below.** `italics.py build`,
`italics_preview.py` and `italics_unmark.py` all write to or read from
`osis/nt-italics/`, which is gone. They are kept as the record of the method
and would need that path changed to run again -- which is what an OT
commentary would want. `italics.py verify` and `italics_sweep.py` still work
as written, since both compare against `osis/nt/`. Note that `verify` now
compares a marked book against itself, so it is only meaningful on a fresh
pass.

Everything below describes the run as it was done.

## Where the output goes

`osis/nt/` is the source and is opened **read-only, always**. The author's
instruction, 2026-08-17: *"as this works, it should write new and separate
files - no changing the originals."*

```
osis/nt/{BOOK}.xml              SOURCE, never written
        |  one agent per chapter, prompts/italics.md
        v
{scratch}/stage/{BOOK}.{CH}.xml one chapter, marked
        |  python scripts/italics.py build {BOOK} {scratch}/stage
        v
osis/nt-italics/{BOOK}.xml      the marked book
        |  python scripts/italics_preview.py {BOOK}
        v
preview/italics-{BOOK}.html     a single local page, for reading
```

Nothing promotes `nt-italics/` over `nt/`, and nothing regenerates
`docs/commentary/data/`. Both decisions are the author's and neither has been
made. The preview page exists so the work can be read without putting it on
the live site.

## Progress

**COMPLETE — all 27 NT books, 260 chapters, marked and verified.** Finished
2026-08-18.

| Book | Chapters | Italics |
|------|---------:|--------:|
| MAT |       28 |   3,744 |
| MRK |       16 |   1,279 |
| LUK |       24 |   2,782 |
| JHN |       21 |   3,801 |
| ACT |       28 |   4,994 |
| ROM |       16 |   4,436 |
| 1CO |       16 |   3,785 |
| 2CO |       13 |   2,536 |
| GAL |        6 |   1,102 |
| EPH |        6 |   2,091 |
| PHP |        4 |   1,415 |
| COL |        4 |   1,474 |
| 1TH |        5 |     961 |
| 2TH |        3 |     660 |
| 1TI |        6 |   1,807 |
| 2TI |        4 |   1,315 |
| TIT |        3 |   1,254 |
| PHM |        1 |     312 |
| HEB |       13 |   2,207 |
| JAS |        5 |   1,252 |
| 1PE |        5 |   1,196 |
| 2PE |        3 |     838 |
| 1JN |        5 |   1,014 |
| 2JN |        1 |     211 |
| 3JN |        1 |     185 |
| JUD |        1 |     180 |
| REV |       22 |   4,798 |
| **27** | **260** | **51,629** |

Counts are total spans in `osis/nt-italics/{BOOK}.xml`, so GAL's and MAT's
include the italics the commentary already had.

Every chapter passed `italics.py verify` individually, and a final pass peeled
every italic span off all 27 books and compared them to `osis/nt/` --
**27 of 27 identical, zero mismatches**. The commentary's prose is untouched.

A preview page for each book sits in `preview/italics-{BOOK}.html`.

**What is still the author's call**, and neither has been decided: whether
`osis/nt-italics/` ever replaces `osis/nt/`, and whether
`docs/commentary/data/` is ever regenerated from it. Nothing does either
automatically.

## Running a book

```
python scripts/italics.py extract {BOOK} {CH} {scratch}/stage/{BOOK}.{CH}.xml
```

Then one agent per chapter, up to six at a time. Give the agent exactly this,
nothing more:

> Read the file `prompts/italics.md` in the working directory. It is your
> complete brief. Follow it exactly.
>
> Mark this file: {absolute path to the staged chapter}
>
> Working directory: C:\Users\Paul March\AI\BibleStudy\RCB

Passing the path to the brief rather than pasting its text matters: the rules
changed four times during Romans and Galatians, and every agent that read the
file picked the change up for free.

Then, per chapter as it lands:

```
python scripts/italics.py verify {BOOK} {CH} {scratch}/stage/{BOOK}.{CH}.xml
```

and when every chapter passes:

```
python scripts/italics.py build   {BOOK} {scratch}/stage
python scripts/italics_preview.py {BOOK}
```

`{scratch}` is any scratch directory. The staged files are disposable once
the book is built.

## The check

`verify` peels every italic wrapper off both the staged chapter and the
original, and the two must come out **byte-for-byte identical** — same words,
same punctuation, same `<p>`, same `<hi type="bold">`, same indentation, same
line breaks. `build` runs it on every chapter and refuses to write the book if
one fails.

Proven against five deliberately broken files: a reworded word, a dropped
bold tag, an invented tag, a changed indent, and a space added before a full
stop. All five were rejected; a correct chapter was accepted.

**Do not take an agent's word that its chapter is clean.** Several reported a
byte-for-byte verification they had not done. Run `verify` yourself, always.

Two traps already paid for:

- **Do not diff the tag sequence.** The first checker did, and it failed a
  chapter that was perfect: an inserted italic sits between existing `<p>`
  tags and `difflib` lines the two lists up differently rather than calling
  it a clean insertion. Peeling and comparing is the correct test.
- `words()` deletes `<hi>` tags rather than spacing them out. Spacing them
  turns `(sarx)` into `( sarx )` and reports a prose change that never
  happened.

## The settled rules

All four were decided by the author during the Romans and Galatians runs and
are written into `prompts/italics.md`.

- **Greek, Hebrew, Aramaic, Latin, German** get italics. The English gloss
  beside them does not.
- **Bold is not exempt.** A foreign word in a `<hi type="bold">` lead-in is
  italicised *nested inside* the bold. This was the biggest single finding:
  Galatians has 718 bold lead-ins to Romans' 68 and keeps its key terms in
  them, so the first pass left *hypo nomon*, *erga nomou*, *paidagogos*, *ta
  stoicheia tou kosmou*, the vice list and the fruit list all unmarked. The
  top-up added 292 spans to a book that had 627. `docs/commentary/osis.js`
  renders the nesting correctly — it recurses into children.
- **Titles of ancient works** get italics: *Antiquities*, *Mishnah*,
  *Institutio Oratoria*, *Metamorphoses*, *Jubilees*, *Psalms of Solomon*.
  Author names stay plain.
- **Bible book names never get italics**, and deuterocanonical books cited
  with chapter and verse are treated the same way — *Wisdom of Solomon*,
  *Maccabees*, *Sirach*, *Tobit* stay plain. Works that were never scripture
  in any canon are italicised.

- **A rabbinic tractate name stays plain; only the collection is
  italicised.** `Mishnah` and `Didache` are titles. `Berakhot`, `Avot`,
  `Shabbat`, `Bava Metzia` and the rest are books *within* the collection, so
  they follow the Bible-book rule, along with the numbers after them.
  `Talmud` and `Shema` are plain too — English now, like `Torah`. Decided by
  the author 2026-08-17, after Matthew came back marking four tractates and
  leaving ten plain, and the three finished books disagreed with each other.

Naturalised borrowings stay plain: `chiasm`, `diatribe`, `hendiadys`,
`litotes`, `via`, `versus`, `genre`, `Torah`, `Messiah`, `LXX`, `rabbi`.

`scripts/italics_unmark.py` applied that ruling to the four books already
built. It only ever deletes an italic wrapper around a named word, and it
refuses to write a book unless the prose still matches `osis/nt/` and every
pre-existing italic survives. Reach for it if another such ruling lands; add
the words to its `PLAIN` list rather than generalising the match.

**Mixed-script transliterations in `osis/nt/` — reported, not fixed.** 79
words across 6 books mix Latin letters with Cyrillic or Greek ones that look
identical on screen: REV 61, 1TH 10, COL 4, LUK 2, JHN 1, MAT 1. Most are
Cyrillic `о е а у с м н` standing in for Latin, almost always where a macron
vowel belongs — `ekklесiais`, `thysiastеrion`, `dyне`, `hypokatо`. A few are
real Greek letters instead: `Simon Ioannου` in JHN 21. The words look right
and are unsearchable.

Find them with a mixed-script scan, not a Cyrillic-only one — the first pass
looked for Cyrillic alone and missed the Greek variety entirely:

```python
CYR, GRK = 'Ѐ-ӿ', 'Ͱ-Ͽἀ-῿'
# a word is suspect when it holds BOTH a Latin letter and one of these
```

Related but separate: dropped macrons that are plain ASCII, so no scan will
find them — JHN 15 transliterates θῇ as `the`, and the commentary then writes
"The verb *the*". Those read as English words and can only be caught by
reading.

This is a defect in the commentary itself, so the italics pass marked every
one exactly as written and changed nothing. Fixing it is the author's call and
belongs in the correction workflow, not here.

**Strip italics from both sides when checking against the source.** `GAL` and
`MAT` carry italics in `osis/nt/` already (GAL has 189), so comparing a marked
book against the raw source file fails a book that is in fact untouched.
`italics.py check()` gets this right; the first draft of `italics_unmark.py`
did not, and its guard caught it.

## Checking a finished book

Beyond `verify`, the sweep that caught every real problem so far:

- titles from the list still sitting outside an italic span
- `<hi type="bold">` runs still containing unmarked Greek
- Bible book names *inside* an italic span
- italic spans containing English function words (`the`, `of`, `and`, `word`,
  `verb`, `aorist`) — a span that swallowed its own gloss

The last one is worth keeping: it caught 2 suspects in 1,297 spans, both
false alarms (`adokimon noun` is Greek), which is the result you want.

**The sweep that actually earns its keep**, added on Acts: collect every
single word the book italicises *somewhere*, then look for those same words
sitting unmarked *anywhere else* in the prose. It needs no guess about what
Greek looks like, and it found the one real miss in 4,996 spans — `hoi
adelphoi` left plain twice in Acts 17. Read the list rather than trusting it:
most of it is correct by design (`Life` the Josephus title vs. "life" the
English word, a name italicised only inside a Greek phrase, a term the agent
deliberately left plain in its English sense), so the job is to spot the one
line that has no such explanation.

Do not bother grepping bold runs for "Greek-looking" endings. That was tried
on Acts and every one of its ~40 hits was an English word ending in `-ion` or
`-os`. The word-set sweep above covers the same ground and does not lie.

**A pre-existing italic is not this pass's work.** Galatians already had 189
italic spans, some of them whole English sentences used as lead-ins. Check
`osis/nt/{BOOK}.xml` before treating one as a mistake.
