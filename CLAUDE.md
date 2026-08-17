# CLAUDE.md — Project Operations Guide

## What this project is

A neutral first-century exegetical study of every NT chapter (260 total), with topic-specific assessments built on top. The exegesis is the shared foundation; assessments and reports are per-topic. All analysis is produced by Claude Opus. The project author reviews output for factual errors and overlooked textual evidence.

See `project_structure.md` for full directory layout and design rationale.

## Data pipeline

```
exegesis/nt/{Book}_{Ch}.md          ← Pass 1: neutral reading (SOURCE)
        ↓
docs/exegesis/nt/{Book}_{Ch}.html   ← HTML version for the site
        ↓
assessments/nt-{topic}/{Book}_{Ch}.json  ← Pass 2: structured assessment
        ↓
docs/reports/{topic}/data.js        ← Aggregated JS array (MUST REGENERATE)
        ↓
docs/reports/{topic}/index.html     ← Interactive report (reads data.js)
        ↓
docs/rcb/data/topics.js             ← Compact index for the RCB commentary pane
                                      (MUST REGENERATE — see below)
```

**Critical**: The report reads from `data.js`, NOT from the assessment JSONs. Any change to an assessment JSON requires regenerating `data.js` or the report will show stale data.

**Also critical, and easy to forget**: the RCB commentary pane reads `docs/rcb/data/topics.js`, which is derived from *both* reports' `data.js`. Regenerating `data.js` without also running `python scripts/gen_topics_index.py` leaves the pane showing the old verdicts. Nothing errors — it just goes quietly stale.

## Regenerating data.js

After any change to files in `assessments/nt-osas/`:

```python
python -c "
import json, glob
sections = []
for f in sorted(glob.glob('assessments/nt-osas/*.json')):
    if 'combined' in f:
        continue
    with open(f, encoding='utf-8-sig') as fh:
        data = json.loads(fh.read())
    book, chapter = data['book'], data['chapter']
    for s in data['sections']:
        s['book'] = book
        s['chapter'] = chapter
        for key in ['conventional_use','relevance','key_phrases','confidence']:
            if key not in s:
                s[key] = '' if key != 'key_phrases' else []
        sections.append(s)
with open('docs/reports/osas/data.js', 'w', encoding='utf-8') as out:
    out.write('const DATA = ')
    json.dump(sections, out, indent=4, ensure_ascii=False)
    out.write(';\n')
print(f'Wrote {len(sections)} sections')
"
```

Notes:
- Use `utf-8-sig` to handle BOM in some JSON files
- Skip `combined.json` (legacy pre-flattened file)
- Same pattern applies for future `nt-determinism` reports

## Restored Context Bible (RCB)

Original English translation from Greek with inline contextual restorations (`\add`) and footnotes (`\f`) in USFM 3.x format. See `RCB-decisions.md` for format, markup, translation philosophy, and key term decisions.

### RCB pipeline

Produced in two passes. The translation is made first, on its own, and is frozen before any amplification touches it.

```
prompts/rcb-pass1.md               ← Pass 1: translation only
        ↓
usfm/nt/{BOOK}-pass1.usfm          ← Intermediate (gitignored)
usfm/nt/{BOOK}-pass1-notes.md      ← Intermediate (gitignored) — see below
        ↓
prompts/rcb-pass2.md               ← Pass 2: amplification, intro, headings
        ↓
usfm/nt/{BOOK}.usfm                ← The finished book (COMMITTED)
        ↓
docs/rcb/data/{BOOK}.js            ← JS data file (MUST REGENERATE)
        ↓
docs/index.html                    ← The viewer, and the site's front door
```

Pass 1 renders the Greek with the Hebrew thinking behind it intact and resolves nothing. Pass 2 adds `\add`, `\f`, `\s1`, `\imt`, and `\ip` and may change nothing else — the base text is frozen. Pass 2 writes the finished book directly; there is no separate merge step.

The freeze breaks in practice, so it is verified on every book. Two failure modes have recurred: pass 2 inserting a `\p` to carry an `\s1` where pass 1 had no paragraph break, and punctuation displaced when a footnote is appended to the end of a sentence. Both are repaired by restoring what pass 1 said — remove the invented `\p` (and the heading that depended on it), or put the mark back. That is not a content edit and does not need the author's approval; anything beyond it does.

The `-pass1` file is a build intermediate, gitignored, and can be deleted after the book is published. The final `{BOOK}.usfm` reproduces it by stripping markers, and the viewer's "Restorations: OFF" toggle already shows a reader the un-amplified translation.

**Pass 1 also writes `{BOOK}-pass1-notes.md`, and pass 2 reads it.** It carries the three things a finished translation cannot show on its own: a reading that departs from what most English versions have, words a reader knows by heart that the critical text does not contain, and a place where the Greek held two senses open and English forced a choice. Every item in it must end up footnoted.

The file exists because pass 2 can only footnote what the text in front of it reveals. A whole verse absent from the critical text shows up as a gap in the numbering; a clause dropped from *inside* a verse is invisible once the verse is written. Pass 1 used to report these to the orchestrating session, which pass 2 never sees, and they were missed on 1 Corinthians and again on Matthew. It is a second build intermediate — gitignored, and deleted with the `-pass1` file when the book is published.

### Running the RCB passes

- Model: opus, one agent per pass
- Give the agent the prompt file's text **verbatim**, plus the minimal instruction naming the book (e.g. "Translate Ephesians." / "Amplify Ephesians.") and the working directory. Add nothing else — no "report back on your choices," no extra constraints, no invented output path
- Run pass 2 only after pass 1 is finished; it reads pass 1's file
- After pass 2: check that markers are balanced (`\add`, `\f`, `\tl`), that every `\s1` is followed by a `\p`, that the `\p` count equals pass 1's, and that verse counts match standard versification with the critical-text omissions subtracted
- Confirm no `\add` sits inside a footnote and no footnote inside an `\add` — an agent has used `\add` as emphasis in note text, which would render as a restoration
- Check that **every item** in `{BOOK}-pass1-notes.md` carries a footnote. Match on the `\fr` reference, and allow for a note anchored on the adjacent verse (when the verse itself is absent) or on a verse range such as `\fr 15:16-18`
- **Then verify the freeze**: `python scripts/check_freeze.py {BOOK}`. It must report `0`. Run it *before* deleting the pass-1 intermediate — that file is the only baseline, and once it is gone the check is impossible. Do not take pass 2's word for it; an agent has reported a book clean that was not
- Parse USFM in Python from a script file, never with a shell one-liner. Backslash-heavy patterns do not survive shell quoting and fail silently, reporting everything clean or everything broken
- Then follow "Publishing a finished book" in `RCB-decisions.md`

### How much to run at once

Whole book wherever it fits. That is the point of the design: key terms and the senses a word carries can only be judged across the whole of what an author wrote, and chapter-at-a-time runs drift.

Where a book is too long to hold in one pass, the split is a judgment call made book by book, not a fixed rule. Split at a structural seam in the argument, never at an arbitrary chapter count, and carry the term decisions forward from one piece to the next. Among the NT books, pass 2 is the constraint — Matthew, Luke, John, Acts, and Revelation are the likely candidates.

This will matter far more in the OT, where several books are longer than anything in the NT. Assume chunking will be normal there and decide it per book.

### RCB links in reports

Every report links each passage row to the RCB viewer when that book has been translated.

`docs/rcb/books.js` is the single source for this. It holds the `RCB_BOOKS` map (full book name as it appears in `data.js` → three-letter code) and `rcbLink()`, which returns an empty string for books not in the map, so untranslated books silently render nothing.

A report wires it up in two places:

1. `<script src="../../rcb/books.js"></script>` after the `data.js` tag and before the inline script
2. `rcbLink(s.book, s.chapter, s.reference)` appended after `exegesisLink(...)` in every table-row builder

To add a translated book, follow "Publishing a finished book" in `RCB-decisions.md`. Those steps live there, not here.

Note `books.js` builds its href relative to the *including page*, assuming `docs/reports/{topic}/index.html`. A page at a different depth would need the path adjusted.

### Regenerating RCB data

After any change to a USFM source file:

```
python scripts/gen_rcb_data.py GAL
```

The script reads `usfm/nt/{BOOK}.usfm`, escapes for a JS template literal, and writes `docs/rcb/data/{BOOK}.js`.

### The site's front door

**The viewer is `docs/index.html`.** The Bible is the front page; the exegesis and the reports hang off it. Its data stayed behind in `docs/rcb/` (`data/{BOOK}.js`, `data/index.js`, `data/topics.js`, `books.js`), so the viewer loads `rcb/data/...` from its new depth.

What this rests on: **every Home link in the project already pointed at `docs/index.html`** — all 260 exegesis chapters (`../../index.html`) and both reports. So the move re-aimed 262 links at the Bible without editing any of them.

- `docs/rcb/index.html` is now a **redirect stub**, kept for links and bookmarks made while the viewer lived there. It carries `?book=` and the fragment across.
- Links out of the viewer — the pane's "Full chapter exegesis" and the topic badges — and the `RCB` links in reports all open in the **same tab**, not a new one. That is what makes Back and Home work, and it matters most on a phone. Don't reintroduce `target="_blank"`.
- The exegesis chapter list that used to be `docs/index.html` is gone. The exegesis is reached through the commentary pane, and each chapter page carries its own prev/next nav, so nothing needs a table of contents.

### The introduction

`?book=INTRO` loads `docs/rcb/data/INTRO.js` and injects it into the reading column. It is **hand-written** — nothing generates it, unlike every other file in `rcb/data/`. Plain HTML in a template literal, so no backticks and no `${` in the prose.

It is a page, not a book: no verses, so `currentBook` is left null, `body.rcb-intro` hides the pane, the divider and both toggles, and the reading column narrows to 720px (1100px is right for verse text and too long a line for prose). Nothing is bookmarked while reading it.

A first visit with no saved place lands here rather than on Matthew 1. Two ways back to it: the toolbar title, and the picker's head row.

Its classes are prefixed `rcb-intro-`, not `intro-`, because **`.intro` already belongs to the `\ip` book introductions** — the paragraphs at the head of each USFM book. Keep them apart.

Don't call this "front matter" in reader-facing text. The author's objection, 2026-08-13: it reads as markdown/AI jargon.

**Keep it true.** It states the textual basis to the reader — the sixteen verses absent from the numbering, the doubtful passages included and footnoted, the 7,943-verse total. Verify against the USFM before changing any of it (`scripts/` has no checker for this; a gap scan over `\c`/`\v` is what produced the list). It also discloses that the translation and analysis are AI-produced and not committee-reviewed; that paragraph is deliberate and should not be softened without the author's say-so.

### The reader's place

The viewer remembers where the reader was, in `localStorage` under `rcb-place` (`ROM.14.12`). A visit with no `?book=` and no hash returns there; a first-ever visit opens at Matthew 1:1. **An explicit `?book=` or `#verse` always wins**, so RCB links from the reports still land exactly where they point — the bookmark only ever fills in a bare visit to the front door.

It exists because the front door needs to put the reader back where they were: Home from an exegesis chapter would otherwise drop them at a default book rather than the passage they left. It also survives closing the tab, which is what a physical ribbon does.

It is a bookmark, **not history** — read Romans 8, jump to John 3, then come back to the front door and you land at John 3.

Two things that are easy to break:

- `savePlace()` rides the scroll handler, which used to `return` early when the pane was off. The bookmark is a property of reading, not a commentary feature, so the `paneOn` guard now sits *inside* the frame callback, around `updatePane()` only.
- `bootAnchor()` returns early when there is no hash, so it needs its own `savePlace()` on that branch — the settling loop below it never runs for a bare visit.

### The commentary pane

`docs/index.html` can show the exegesis beside the text, synced to whatever passage the reader is in, with the topical verdicts for that passage above it. The "Commentary" toolbar toggle shows and hides it; the choice is remembered in `localStorage`, defaulting on above 1100px and off below, where the pane becomes a bottom sheet.

**The verdicts are pulled, not pushed.** One quiet line sits at the top of the pane — "2 topics discuss this passage" — and opens the list on demand; its state is remembered in `localStorage` (`rcb-topics-open`), collapsed by default. It reads the same way at two topics as it would at twenty, which is the point: a stack of badges pushed at the reader does not survive the topic count growing. **The count is of topics that actually say something**, i.e. excluding `NOT_APPLICABLE` — that is the majority verdict in both reports (1,376 of 1,959 OSAS rows, 1,088 of 1,976 determinism), so counting every covering row would print the same number on nearly every passage. The not-applicable rows are still listed once the line is opened.

**It syncs by verse containment, not by matching headings.** The RCB's `\s1` divisions and the exegesis's divisions usually agree but not always — Romans 8 breaks at v9 in the RCB and v5 in the exegesis. So the pane takes the verse at the reading line and finds the section whose range contains it, which is immune to the mismatch. Do not "fix" this by aligning the two sets of headings.

Two things it reads:

- `docs/exegesis/nt/{Book}_{NN}.html`, fetched per chapter as the reader arrives. The section ranges come from the **heading text** (`Verses 16b-18:`), not the `id`, because the id holds only the first verse token of a split verse (`id="16"`). Parsing ids alone leaves 31 phantom gaps across the NT.
- `docs/rcb/data/topics.js` for the verdict badges, lazy-loaded when the pane is first opened.

**There is no nearest-section fallback**, deliberately. Where no section contains the verse the pane says so, rather than showing a neighbouring passage's commentary as if it applied.

**As of 2026-08-17 that case does not arise: all 7,943 verses of the RCB are covered, 100.00%.** The checker's expected-gap list is empty and should stay empty.

Verify with `python scripts/check_pane_coverage.py`. It walks every verse in every `usfm/nt/{BOOK}.usfm` against the exegesis section ranges and exits non-zero on any uncovered verse not in its expected list — so a new exegesis chapter, or an edit that renames a heading, gets caught. Run it after any change to an exegesis file's `<h2>` headings.

**A reported gap is a suspect, not a finding.** Three times running it has been a heading the checker could not parse, sitting on top of analysis that was written all along:

- **Titus 2:7-10**, until 2026-08-13. The section covered 2-10, with subsections on the younger men (6-8) and on slaves (9-10). Only the `<h2>` said "Verses 2-6".
- **John 7:53-8:11**, until 2026-08-17. `John_08` carries a full reading of the passage — the entrapment between Rome's monopoly on capital sentences and Moses, the missing man of Deuteronomy 22:22, the witnesses casting first at Deuteronomy 17:7. Its heading is "A Note on 7:53-8:11", which did not begin "Verses", so it had no id at all and the pane never looked at it. CLAUDE.md recorded it as a place "the exegesis did not go". It had gone there.

- **Revelation 12:18**, until 2026-08-17. Not a parsing failure but the same kind of mistake one level up: the clause was discussed in `Revelation_13` under "Context and Placement". That is the Textus Receptus framing, where the clause is 13:1a and the one standing is the seer. The RCB follows the earlier witnesses — `estathē`, the *dragon* stands, at the waterline where the beast is about to come up — which makes it the last beat of chapter 12. `Revelation_12`'s closing section now runs 13-18 and carries the exposition, including the note on the variant.

Read the section body before commissioning a re-run, and check the neighbouring chapter's file — analysis of a passage straddling a chapter boundary is written in one file and belongs to both. The assessments are a good cross-check: for Titus both had already assigned the passage (OSAS as `2:2-10`, determinism as `2:6-8` and `2:9-10`), because they read the text rather than the heading.

**What the heading parser accepts**, since a heading that misses it becomes an invisible section. `Verses 13-18:` and `Verse 12:` as always; `Verses 16b-18:` with the part-verse; a chapter-qualified range for a passage that crosses a chapter boundary (`A Note on 7:53-8:11`, `Verses 12:18-13:2:`); and a trailing parenthesised range, which is how Matthew 2 and Luke 15 head every one of their sections (`The Lost Sheep (15:4-7)`). A chapter-qualified range must open or close the heading and must not follow a capitalised word — that is how a cross-reference names its book, so `The Fulfillment of Acts 1:8` inside Acts 10 is correctly *not* read as a section on Acts 1.

The rule is implemented twice — `scripts/check_pane_coverage.py` and `parseHeadingRange()` in `docs/index.html` — and the two must agree, or the checker and the pane will disagree about what exists. **Ids are now written by hand**, so match them to the heading: bare verses for a range inside its own chapter (`id="13-18"`), dotted when it reaches into another (`id="7.53-8.11"`). The bare form is what the reports build their anchors from — `exegesisHref()` takes the part of `12:13-18` after the colon — so changing it breaks every report link into that section.

### Book identifiers and abbreviations

**The canonical identifier is the USFM 3-letter code** — already the USFM filename, the data filename, and the `?book=` parameter. Settled 2026-08-13 after checking the alternatives against the whole 66-book canon.

**Two characters cannot identify a book.** The leading two letters collide seven ways across the canon:

```
JO -> Joshua, Job, Joel, Jonah, John      MA -> Malachi, Matthew, Mark
EZ -> Ezra, Ezekiel                       PH -> Philippians, Philemon
JU -> Judges, Jude                        ZE -> Zephaniah, Zechariah
HA -> Habakkuk, Haggai
```

Three leading letters collide only twice — `JUD` (Judges/Jude) and `PHI` (Philippians/Philemon) — and the USFM codes exist precisely to break those: `JDG`/`JUD`, `PHP`/`PHM`. `scripts/gen_rcb_index.py` asserts code uniqueness on every run rather than assuming it.

**Short input still works without inventing a scheme.** The viewer's `matchBook()` accepts any *unambiguous* prefix, and 40 of the 66 books resolve in two characters (`ro`, `ga`, `ep`, `ti`). Ambiguous input resolves to nothing rather than to a guess, so `jo` and `ph` simply fail. A small alias table covers common forms that are not prefixes (`jn`, `mt`, `mk`, `lk`, `rv`).

**One case where a code and a natural prefix disagree**: `jud` is Jude's USFM code, so it resolves to Jude, not Judges — exact code match wins over prefix. Judges needs `judg`. The picker's live hint (`→ Jude 1:14`) shows the resolution before Enter, which is what keeps this visible rather than silent.

**Block labels are readable short forms, not codes** (`1 Chron`, `Eccles`), because grid columns are fixed width — a longer label costs no space, and codes like `SNG`/`NAM` only cost legibility.

`scripts/gen_rcb_index.py` holds the full 66-book table (code, label, genre). **Books whose USFM file is missing are skipped**, so an OT book joins the picker as soon as `usfm/ot/{CODE}.usfm` exists — no code change. Genres drive block colour only, and pair across the testaments: Torah with Gospels, OT history with Acts, Wisdom with the epistles, major prophets with the general letters, minor prophets with Revelation.

### Regenerating topics.js

After any change to either report's `data.js`:

```
python scripts/gen_topics_index.py
```

It strips both reports to what the pane shows — book, chapter, reference, category, section title — keyed by USFM code. The full `data.js` pair is ~3.9MB, far too much for a reading page; the index is ~495K.

### RCB file naming

`{BOOK}.usfm` — three-letter book abbreviation (e.g., `GAL`, `ROM`, `EPH`). Same abbreviation used in the data JS file and the `?book=` query parameter.

`{BOOK}-pass1.usfm` — the pass 1 intermediate for that book. Gitignored, along with `docs/rcb/data/*-pass1.js` and the equivalent `-pass2` names.

`{BOOK}-pass1-notes.md` — pass 1's handoff to pass 2. Also gitignored, and deleted with the `-pass1` file at publication.

## Correction workflow

When the project author identifies a factual error or overlooked evidence:

1. **Fill in the correction prompt** (`prompts/correction.md`) with chapter, verse range, and problem statement. The problem flags what to re-examine — it does NOT give the answer.
2. **Run an agent** with the neutral reading prompt + filled correction prompt + current section text. Model: opus.
3. **Replace the section** in both `exegesis/nt/{Book}_{Ch}.md` and `docs/exegesis/nt/{Book}_{Ch}.html`.
4. **Check for ripple references**: grep other exegesis files for references to the corrected passage. Fix context summaries in adjacent chapters if needed.
5. **Update the corrections log** (`prompts/corrections_log.md`) with the problem, question sent, outcome, ripple fixes, and assessment impact.
6. **Re-run the assessment** for the affected section if the correction changes OSAS-relevant content. Update the assessment JSON, then regenerate `data.js`.
7. **Check RCB impact**: if that book has an RCB translation (`usfm/nt/{BOOK}.usfm`), review the EAs and footnotes covering the corrected passage. They were written from the exegesis, so a correction upstream can leave them stating the superseded reading. Fix what the correction invalidates, then regenerate with `python scripts/gen_rcb_data.py {BOOK}`.

### RCB corrections

When the error is in the RCB itself rather than the exegesis — a translation choice, an EA that overreaches or reads awkwardly, a footnote, or something inline that belongs in a footnote:

1. **Check the exegesis first.** If the underlying reading is wrong, run the correction workflow above instead; the RCB fix follows from it. Only proceed here when the exegesis is sound and the problem is in the translation layer.
2. **Consult `RCB-decisions.md`** before editing. The fix must follow the settled conventions, and the governing test is that the amplified sentence reads naturally. Do not edit the decision log — if the fix requires a decision the log does not cover, raise it with the project author.
3. **Edit `usfm/nt/{BOOK}.usfm`.**
4. **Check for ripple within the book**: footnote cross-references to the changed verse, and EAs that depend on a term or framing introduced there.
5. **Regenerate**: `python scripts/gen_rcb_data.py {BOOK}`.
6. **Update the corrections log** (`prompts/corrections_log.md`).

## Running Pass 1 (neutral reading)

- Prompt: `prompts/neutral_reading.md`
- Agent instruction: prompt text + "Analyze {Book} {Chapter}. Write your full analysis to a file called {filename}."
- Output: `exegesis/nt/{Book}_{Ch}.md`
- Model: opus
- Pacing: 2-3 agents at a time max
- Do NOT add topic framing, output structure, or conclusions to the prompt
- See `run_instructions.md` for the full 260-chapter checklist (complete; kept as the record of that run)

## The two exegesis methods — read before touching `exegesis/`

There are two sets of exegesis prompts in `prompts/`. They are not alternatives to choose between. One is the method; the other is an experiment in repairing the method's failures.

**`neutral_reading.md` — the original and approved approach.** This is the method. All 260 NT chapters were produced with it. Use it for any new exegesis. Do not replace it, and do not "upgrade" a chapter to the other method because it looks more thorough.

**`whole_book_pass.md` + `chapter_exegesis.md` — an ongoing experiment, not approved.** A two-pass repair method: a whole-book structural analysis (occasion, argument flow, key terms traced across every occurrence, internal coherence, and "injections" flagging where later theology tends to creep in), then chapter exegesis bound to that framework.

Why it exists: a model's training is so deeply infused with Reformed theology that eliminating it can seem impossible. The original Galatians exegesis was badly off the mark for exactly that reason. These prompts were written to correct it, and Galatians was rewritten with them (commit `942660b`, 2026-08-11).

**Galatians is the only book produced this way, and it is better but still not the answer.** The experiment is unfinished. Treat its output as improved, not as the standard.

Two things to know if you work on this:

- The whole-book analysis that `chapter_exegesis.md` requires as input was never saved for Galatians. It lived in the session and is gone. Any future correction to a Galatians chapter is therefore made without it.
- **CLOSED — do not raise this again.** Whether to re-run `whole_book_pass.md` on Galatians and save the result was put to the author on 2026-08-13 and he said drop it, permanently. The reasoning: a fresh run produces a *different* document, so it recovers nothing, and leaving it in the repo would invite someone later to mistake it for the notes the existing six chapters were actually written from. **Do not propose reconstructing it, and do not treat its absence as an open task.** The Galatians chapters stand as they are.

The one thing that carries forward: **if these prompts are ever used on another book, save the whole-book analysis to a file as part of the run.** That is the whole lesson, and it costs nothing at the time.

## The framing audit

An experiment in QC-ing the exegesis for Reformed framing drift, agreed 2026-08-13. **It reports; it never edits.** The author decides what, if anything, follows.

Two instruments, cheap before expensive:

**1. `python scripts/check_framing.py`** — greps all 260 chapters for vocabulary with no first-century referent (`legalism`, `antinomian`, `sola fide`, the medieval moral/ceremonial division of Torah). Instant, always exits 0. Run it on any new chapter. Current NT state: 25 hits in 14 chapters, and reading every one, they are the category being *refused*, quoted, or translated — not one asserts a Reformed reading as the plain sense. **It cannot see framing drift**, which lives in emphasis and in which options go unmentioned. That is what the second instrument is for.

**2. `prompts/framing_audit.md`** — one agent per chapter, opus, output to `audits/framing/{Book}_{Ch}.md`. Give it the prompt text verbatim plus "Audit {Book} {Chapter}." and the working directory. Pace 2-3 at a time per the standing rule.

The sample to run first — the twelve chapters where a Reformed framework has the most to gain, so a null result across them is real evidence:

```
Romans 3, 4, 8, 9, 10, 11     justification, election
Galatians 2, 3                the book that failed before
Ephesians 2                   grace and works
Hebrews 8                     covenant superseded
John 6                        drawing and giving
James 2                       the counter-case
```

**The null result is the point.** The prompt says a clean chapter is a real finding and that padding destroys the report's value. If the audit comes back mostly clean across the twelve worst chapters, that is strong evidence the drift is rarer than the Galatians experience suggested — and it means no 260-chapter sweep is owed. If it finds real things, it scales. Either way twelve runs answers it.

Do not let the audit edit exegesis. A finding goes through the normal correction workflow, with the author's approval, or nowhere.

## Running Pass 2 (assessment)

- Prompt: `prompts/osas.md` (or `prompts/determinism.md` for that topic)
- Input: the complete Pass 1 neutral reading for a single chapter
- Output: `assessments/nt-{topic}/{Book}_{Ch}.json`
- Model: opus
- Pacing: 2-3 agents at a time max
- After all chapters are done: regenerate `data.js` and verify the report
- New report? Carry over the RCB link wiring — see "RCB links in reports" below. It is easy to ship a report with no RCB links and not notice.

## Converting markdown to HTML

The exegesis HTML files in `docs/exegesis/nt/` correspond to the markdown sources in `exegesis/nt/`. When a markdown file is corrected, the HTML must get the same change. **This is done by hand — edit both files.**

There was briefly a `scripts/md_to_html.py`, written for the Galatians rewrite and deleted on 2026-08-17. It did not reproduce the published HTML: running it over all 260 chapters rewrote far more than it was asked to (Acts 12 alone shifted 55 lines), so it was a trap for anyone who reached for it to update a single chapter. The commentary is moving to OSIS, which will replace this step rather than automate it, so it was not worth repairing.

House format, for hand edits:

- `&mdash;` for em-dashes, `<p>` around paragraphs, `<strong>` for the bolded lead phrase of an exposition paragraph
- transliterated Greek as literal UTF-8 (`estathē`, `ediōxen`), never numeric entities
- section headings are `<h2>` and **must carry an id**, because the commentary pane queries `h2[id]` and silently ignores anything without one

## Hosting

- GitHub repo: `pmarch502/OSAS` (public)
- Hosted on **Cloudflare Pages** at `osas-eu8.pages.dev`
- Auto-deploys from `main` branch, build output directory: `docs/`
- GitHub Pages is disabled (was flaky with 260+ static files)

## Agent pacing

Run 2-3 agents at a time max. Don't flood and burn credits.

## File naming

`{Book}_{Chapter}.{ext}` — Book names have no spaces, number prefix attached, chapters zero-padded to two digits. Examples: `Romans_08.md`, `1Corinthians_16.json`, `Revelation_22.html`.
