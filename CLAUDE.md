# CLAUDE.md — Project Operations Guide

## What this project is

A neutral first-century exegetical study of every NT chapter (260 total), with topic-specific assessments built on top. The exegesis is the shared foundation; assessments and reports are per-topic. All analysis is produced by Claude Opus 4.6. The project author reviews output for factual errors and overlooked textual evidence.

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
```

**Critical**: The report reads from `data.js`, NOT from the assessment JSONs. Any change to an assessment JSON requires regenerating `data.js` or the report will show stale data.

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
        ↓
prompts/rcb-pass2.md               ← Pass 2: amplification, intro, headings
        ↓
usfm/nt/{BOOK}.usfm                ← The finished book (COMMITTED)
        ↓
docs/rcb/data/{BOOK}.js            ← JS data file (MUST REGENERATE)
        ↓
docs/rcb/index.html                ← Single viewer (loads ?book={BOOK})
```

Pass 1 renders the Greek with the Hebrew thinking behind it intact and resolves nothing. Pass 2 adds `\add`, `\f`, `\s1`, `\imt`, and `\ip` and may change nothing else — the base text is frozen. Pass 2 writes the finished book directly; there is no separate merge step.

The freeze breaks in practice, so it is verified on every book. Two failure modes have recurred: pass 2 inserting a `\p` to carry an `\s1` where pass 1 had no paragraph break, and punctuation displaced when a footnote is appended to the end of a sentence. Both are repaired by restoring what pass 1 said — remove the invented `\p` (and the heading that depended on it), or put the mark back. That is not a content edit and does not need the author's approval; anything beyond it does.

The `-pass1` file is a build intermediate, gitignored, and can be deleted after the book is published. The final `{BOOK}.usfm` reproduces it by stripping markers, and the viewer's "Restorations: OFF" toggle already shows a reader the un-amplified translation.

### Running the RCB passes

- Model: opus, one agent per pass
- Give the agent the prompt file's text **verbatim**, plus the minimal instruction naming the book (e.g. "Translate Ephesians." / "Amplify Ephesians.") and the working directory. Add nothing else — no "report back on your choices," no extra constraints, no invented output path
- Run pass 2 only after pass 1 is finished; it reads pass 1's file
- After pass 2: check that markers are balanced (`\add`, `\f`, `\tl`), that every `\s1` is followed by a `\p`, and that verse counts match standard versification
- **Then verify the freeze**: `python scripts/check_freeze.py {BOOK}`. It must report `0`. Run it *before* deleting the pass-1 intermediate — that file is the only baseline, and once it is gone the check is impossible. Do not take pass 2's word for it; an agent has reported a book clean that was not
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

### RCB file naming

`{BOOK}.usfm` — three-letter book abbreviation (e.g., `GAL`, `ROM`, `EPH`). Same abbreviation used in the data JS file and the `?book=` query parameter.

`{BOOK}-pass1.usfm` — the pass 1 intermediate for that book. Gitignored, along with `docs/rcb/data/*-pass1.js` and the equivalent `-pass2` names.

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

- The whole-book analysis that `chapter_exegesis.md` requires as input was never saved for Galatians. There is no storage convention for it. Anyone re-running or extending the experiment has to produce one first, and should save it this time.
- Any future correction to a Galatians chapter is being made against a framework that no longer exists in the repo.

## Running Pass 2 (assessment)

- Prompt: `prompts/osas.md` (or `prompts/determinism.md` for that topic)
- Input: the complete Pass 1 neutral reading for a single chapter
- Output: `assessments/nt-{topic}/{Book}_{Ch}.json`
- Model: opus
- Pacing: 2-3 agents at a time max
- After all chapters are done: regenerate `data.js` and verify the report
- New report? Carry over the RCB link wiring — see "RCB links in reports" below. It is easy to ship a report with no RCB links and not notice.

## Converting markdown to HTML

The exegesis HTML files in `docs/exegesis/nt/` are generated from the markdown sources in `exegesis/nt/`. When a markdown file is corrected, the corresponding HTML must be updated with the same changes. Currently this is done manually (edit both files). The HTML uses `&mdash;` for em-dashes and wraps paragraphs in `<p>` tags.

## Hosting

- GitHub repo: `pmarch502/OSAS` (public)
- Hosted on **Cloudflare Pages** at `osas-eu8.pages.dev`
- Auto-deploys from `main` branch, build output directory: `docs/`
- GitHub Pages is disabled (was flaky with 260+ static files)

## Agent pacing

Run 2-3 agents at a time max. Don't flood and burn credits.

## File naming

`{Book}_{Chapter}.{ext}` — Book names have no spaces, number prefix attached, chapters zero-padded to two digits. Examples: `Romans_08.md`, `1Corinthians_16.json`, `Revelation_22.html`.
