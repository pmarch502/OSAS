# RCB Pass 2 — Explanatory Amplification

You are adding explanatory amplification to a new translation of the New Testament. This is the second of two passes. Your job is to make a modern reader "hear" (i.e. understand) what a 1st century reader would have heard by providing contextual restorations.

You must balance two competing goals. First, you should use the least number of insertions and the least number of words as you possibly can - this isn't a commentary. Second, you must give the modern reader all of the needed explanation so that they actually understand the text as if the writer were here now, speaking in a modern English way and providing the cultural and historical context while he spoke.

Read these two files first:

- `usfm/nt/{BOOK}-pass1.usfm` — the translation you are amplifying.
- `usfm/nt/{BOOK}-pass1-notes.md` — what the translator knew and the translation cannot show: readings that differ from the familiar English, words a reader expects that the critical text does not have, places where English had to pick one of two open readings.
- `osis/nt/{BOOK}.xml` — the commentary on every chapter of the book, in OSIS. This is where your context comes from. Do not supply context it does not support. Each `<div type="section">` names the passage it covers in its `annotateRef`, so you can find the section covering a verse rather than reading the whole book; a section whose reference is a bare chapter (`Rom.8`) is about the chapter as a whole.

Every item in the notes file gets a footnote. It is the one input you may not exercise judgment about leaving out — the reader it serves is the one who knows the familiar wording by heart and meets your text without it. Where the conventional rendering is not merely different but wrong, say that it is what most translations do; do not call it an alternative, which implies a live option. The notes change nothing in the base text, which is frozen exactly as below.

The translation is finished and frozen. Change nothing outside the markers you add — not a word, not a mark of punctuation. It is not yours to judge. Where the wording is hard to follow, that is exactly what your amplification is for — clarify it there.

You may add five markers and no others: `\add`, `\f`, `\s1`, `\imt`, and `\ip`.

Add your amplification using the following format:

**Inline** — bracketed text wrapped in `\add ... \add*`, placed immediately after the words it completes:

```
\v 1 Paul, one sent \add [i.e. carrying the full authority of the one who sent him]\add* — not from men \add [i.e. my commission did not come from any human council]\add* —
```

**Footnote** — `\f + \fr {chapter}:{verse} \ft {text}\f*`, placed immediately after the word or phrase it belongs to:

```
\v 8 let him be under the ban\f + \fr 1:8 \ft Greek \tl anathema\tl*, from Hebrew \tl cherem\tl*, the irrevocable ban of total destruction (Leviticus 27:28-29).\f*
```

Wrap every transliterated Greek or Hebrew word in `\tl ...\tl*`, as above. It renders italic. Only the foreign word goes inside the marker — not the language name, not the surrounding punctuation.

Both markers must be closed. Everything inline goes inside square brackets, and the brackets go inside the `\add`.

Use inline when it completes the thought and the sentence still reads in one breath. Use a footnote when the reader has to stop and process it.

Write every inline amplification in the author's own voice, continuing the sentence he is already writing. Read the amplified sentence aloud with the brackets ignored: it should sound like he wrote it that way from the start, not like someone has interrupted him to explain. Never narrate about him — no "Paul means," no "the term here refers to," no study-note voice. Things that cannot be said in his voice, because he could not have said them about himself — the background of a Greek word, a cross-reference, a manuscript note — go in footnotes.

## Introduction and section headings

Two more things the book needs, both written from the same neutral readings.

**Introduction.** After the `\mt1` line, write `\imt Introduction` followed by two to four `\ip` paragraphs: who wrote to whom, where they were, roughly when, and what situation provoked the letter. A reader who knows nothing should be able to follow the argument after reading it. This is editorial, not the author's voice, and it is not a summary of the book's contents.

**Section headings.** Break the book into the movements of its argument with `\s1` headings. A heading says what the passage does, in plain words, in the fewest that will carry it. Put each on its own line, immediately before the `\p` that opens the section — never inside a paragraph, and always with a `\p` following it.

Output USFM 3.x to `usfm/nt/{BOOK}.usfm`. This is the finished book.

## When you are given a range

You may be given a verse range instead of a whole book — "Amplify Revelation 12:1-22:21." Then:

- Read only your range of `usfm/nt/{BOOK}-pass1.usfm`, and in `osis/nt/{BOOK}.xml` only the chapters your range covers.
- Output to `usfm/nt/{BOOK}-pass2-{n}.usfm`, beginning at your range's first `\c` line. Write no `\id`, `\ide`, `\h`, `\toc`, or `\mt1` — the first range carries those, and the pieces are joined in order.
- Only the range that opens the book writes the `\imt` introduction.
- If `usfm/nt/{BOOK}-handoff.md` exists, read it first: it records what earlier ranges already footnoted, so you neither repeat a key-term note nor leave one unexplained. When you finish, append your own section — every Greek or Hebrew term you footnoted and where, every heading you placed, and anything a later range needs in order to stay consistent with you.
