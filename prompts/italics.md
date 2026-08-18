# Italicising the original languages

You are marking one chapter of a commentary so that foreign words appear in
italics: transliterated Greek, Hebrew, and Aramaic, and Latin scholarly
terms. This is a typographic pass. It is not an editing pass, a correction
pass, or a review pass.

## The one rule that outranks everything else

**Do not change a single word of the prose.** Not a word, not a punctuation
mark, not a heading, not a quotation. You are inserting markup around text
that already exists and touching nothing else. Every change is verified
mechanically afterwards: the file is stripped of all markup and compared
word for word against the original. If one word differs, the whole chapter
is thrown away.

The same holds for the existing markup. `<p>`, `<title>`, `<div>`,
`<hi type="bold">`, `<list>`, `<item>`, `<table>` and everything else stay
exactly where they are, spelled exactly as they are.

## What to italicise

Wrap it in `<hi type="italic">` and `</hi>`.

Transliterated Greek, Hebrew, and Aramaic — the original language written
out in Latin letters. Examples of the shapes it takes:

- A bare word in the prose: `the word doulos means` → `the word <hi type="italic">doulos</hi> means`
- A word before its meaning: `"Servant" (doulos) — the word means`
- A phrase inside brackets: `(ho dikaios ek pisteos zesetai)`
- A word with a macron, the bar over a vowel: `pisteōs`, `dikaiosynē`
- A grammatical form named in the original: `aphorizo`, `kletos apostolos`

Latin scholarly terms, the words a commentary borrows from Latin because
English has no single word for them: `inclusio`, `a fortiori`, `ad hominem`,
`catena`, `sensus plenior`, `ex nihilo`, `in toto`, `pace`, `qal wahomer`,
`captatio benevolentiae`, `sitz im leben` (German, and treat German the same
way). Mark the whole term as one span: `<hi type="italic">a fortiori</hi>`,
not two.

Titles of ancient works other than the Bible, whatever language they are in:
Quintilian's `Institutio Oratoria`, Ovid's `Metamorphoses`, Euripides'
`Medea`, Columella's `De Re Rustica`, Josephus' `Antiquities` and `Jewish
War`, Philo's `On the Life of Moses`, the `Mishnah`, the `Didache`, `1
Enoch`, `Jubilees`. The author's name beside the title stays plain.

**Never italicise the name of a book of the Bible.** Romans, Galatians,
Isaiah, Genesis, Psalms and the rest stay plain, always, including in
citations. The same goes for `LXX` and `MT`.

**A rabbinic tractate name is plain; only the collection is italicised.** The
`Mishnah` and the `Didache` are titles and get italics. `Berakhot`, `Avot`,
`Shabbat`, `Sanhedrin`, `Bava Metzia`, `Pesachim` and the rest are books
*within* the collection, so they follow the Bible-book rule and stay plain,
along with the chapter and verse after them — `the <hi type="italic">Mishnah</hi>
(Berakhot 3:1)`. `Talmud`, `Shema` and `menorah` are plain too; they read as English now,
like `Torah`.
Settled 2026-08-17 after Matthew came back marking four tractates and leaving
ten plain.

**Mark a phrase as one span, not word by word.** `(ho dikaios ek pisteos
zesetai)` becomes one `<hi type="italic">ho dikaios ek pisteos zesetai</hi>`,
never five separate spans. The brackets themselves stay outside the italics.

## What to leave alone

- **The English meaning.** In `doulos ("slave, bondservant")`, only `doulos`
  is italicised. The quoted English is not.
- **English words.** Some Greek particles are spelled like English words —
  `de`, `men`, `nous`, `hos`, `on`. Italicise them only where the sentence is
  plainly talking about the Greek. When in doubt, leave it plain.
- **Ordinary English names.** Jesus, Paul, Moses, Isaiah, Rome, Torah,
  Messiah, Pharisee, Sadducee, LXX, rabbi. These are English now.
- **Latin and Greek that has become ordinary English.** `via`, `versus`,
  `per`, `status quo`, `data`, `forum`, `agenda`, `index`, `genre`,
  `chiasm`, `chiasmus`, `diatribe`, `hendiadys`, `litotes`, `diptych`,
  `apocalyptic`, and the abbreviations `e.g.`, `i.e.`, `cf.`, `etc.`, `AD`,
  `BCE`. If an English speaker would not notice it is borrowed, leave it
  plain. The test is whether the word still reads as foreign.
- **Anything already inside `<hi type="italic">`.** Some are marked already.
  Leave them exactly as they are.
- **Bold text is not exempt.** A foreign word inside a `<hi type="bold">`
  lead-in gets italics like any other, nested inside the bold:
  `<hi type="bold">The phrase <hi type="italic">hypo nomon</hi> governs
  the argument.</hi>`. Some books put their key terms almost entirely in
  bold headings, and skipping those leaves the most important words in the
  book unmarked. Never nest the other way round -- bold inside italic.
- **Scripture references and verse numbers.**

## Borderline cases

A transliterated name inside a Greek phrase goes in the italics with the rest
of the phrase: `(Christou Iesou)` is one italic span. The same name standing
alone in English prose as "Christ Jesus" is not italicised.

Where a Greek word has been given an English plural or ending, italicise the
Greek and leave the ending outside if that reads correctly; otherwise
italicise the whole token. Either is acceptable. Do not agonise.

If you genuinely cannot tell whether something is a transliteration, leave it
plain. A missed word costs nothing. A wrongly italicised English word is a
visible error on the page.

## How to work

1. Read the file you have been given. It is one chapter of OSIS XML.
2. Edit that same file in place, using the Edit tool, one insertion at a
   time. Use `replace_all` where the same wrapped string occurs more than
   once and every occurrence should be marked.
3. Do not rewrite the whole file. Do not create any other file.
4. When you are finished, report only the count of spans you added and any
   case you decided to leave plain because you were unsure. Nothing else.
