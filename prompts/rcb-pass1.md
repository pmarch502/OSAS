# RCB Pass 1 — Translation

You are translating the Greek New Testament into English (NA28/UBS5), one whole book at a time. This is the first of two passes. Add no context, explanation, or interpretation — a later pass does that.

Read the whole book before you translate any of it. Where a word carries more than one sense, choose the sense the passage requires — having seen every place the author uses that word, not just this one.

Every NT writer except Luke thinks like a Hebrew and writes in Greek. Greek is the container, not the content. Translate the thought, not the container.

**Words.** When a Greek word is carrying a Hebrew idea, translate the Hebrew idea. Ask what Hebrew word stands behind it and what that word means. Where a Greek reading and a Hebrew reading pull apart, take the Hebrew one. Where nothing Hebrew stands behind it, translate the Greek plainly.

**Sentences.** Hebrew thinking has a shape, and it survives into the Greek. Keep it:
- Concrete, not abstract. If it says "walk," write "walk," not "behave."
- The whole person, not a body with a soul inside it.
- Verbs where English would reach for a noun.
- Repeated and parallel lines — leave them, don't tidy them.
- Physical words for inner states: heart, bowels, face, hand.

**Leave open what the Greek leaves open.** Where a first-century hearer could honestly have taken a phrase more than one way, write English that stays open the same way. Don't resolve it and don't explain it.

**Luke is the exception.** He thinks in Greek; translate his Greek as Greek. Except where he quotes the Old Testament or writes in deliberate Septuagint style — Luke 1–2, the speeches in Acts — where the rules above apply.

Write plain, natural English. Raw doesn't mean clumsy. If a sentence read smoothly to its first hearers, your English should read smoothly too — it just must not say more than the Greek said.

**Break the text into paragraphs where the argument turns.** Put a `\p` at each movement of the thought, not only at the start of a chapter. You have read the whole book; you are the one who knows where it turns. A short letter needs this as much as a long one — a book delivered as a single unbroken paragraph is not finished.

Output USFM 3.x to `usfm/nt/{BOOK}-pass1.usfm`. The `\id` line reads `\id {BOOK} - Restored Context Bible (RCB)`. No pass label.

## What the next pass cannot see

Write a second file, `usfm/nt/{BOOK}-pass1-notes.md`, listing what a reader of your translation will need told and your translation itself cannot show. One line per item, each beginning with the chapter and verse. Nothing else belongs in this file — it is not a report on your work.

Three kinds of thing go in it:

- **A reading that differs from what most English versions have**, where you followed the critical text and they do not. Say what you rendered and what they render.
- **Words a reader knows by heart that are not in the critical text** — a clause or a familiar ending absent from NA28. Whole verses missing from the numbering will be obvious to the next pass; a phrase dropped from inside a verse is invisible once you have written it, so it must be listed here.
- **A place where the Greek held two readings open and English forced you to pick one.** Say which you took and what the other was.

If a book has none of these, write the file and say so.
