# RCB — Directory Structure

## Overview

This project builds a neutral first-century exegetical foundation for the entire Bible, then runs topic-specific assessments against that foundation to produce interactive public reports. The neutral readings are the shared investment; assessments and reports are per-topic and reusable.

## Directory Layout

```
RCB/
├── prompts/
│   ├── neutral_reading.md              Shared prompt for all commentary
│   ├── osas.md                         OSAS assessment prompt
│   ├── determinism.md                  Determinism/free will assessment prompt
│   ├── correction.md                   Filled in when a factual error is found
│   ├── corrections_log.md              Record of every correction made
│   ├── rcb-pass1.md                    RCB pass 1 — translation
│   ├── rcb-pass2.md                    RCB pass 2 — amplification, intro, headings
│   ├── whole_book_pass.md              EXPERIMENTAL — repair method, not approved
│   └── chapter_exegesis.md             EXPERIMENTAL — repair method, not approved
│
├── osis/                               SOURCE — the commentary, in OSIS
│   ├── nt/
│   │   ├── MAT.xml                     one file per book, named for the USFM code
│   │   └── ... (27 files)
│   └── ot/                             (not yet written)
│
├── assessments/                        Per-topic structured JSON from assessment prompts
│   ├── nt-osas/
│   │   ├── Matthew_01.json
│   │   └── ... (260 files)
│   ├── nt-determinism/
│   │   └── ...
│   ├── ot-osas/
│   │   └── ...
│   └── ot-determinism/
│       └── ...
│
├── usfm/                               SOURCE — Restored Context Bible USFM files
│   └── nt/
│       └── GAL.usfm                    Galatians (3-letter book codes)
│                                       {BOOK}-pass1.usfm is a gitignored intermediate
│
├── scripts/
│   ├── gen_rcb_data.py                 Regenerate RCB data from USFM source
│   ├── gen_commentary_data.py          Regenerate commentary data from OSIS source
│   ├── check_osis.py                   Structural check on the OSIS
│   └── check_pane_coverage.py          Every RCB verse has commentary behind it
│
├── docs/                               PUBLISHED — Cloudflare Pages build output
│   ├── index.html                      THE SITE. The RCB viewer, and the front door;
│   │                                   loads ?book=CODE, or ?book=INTRO for the
│   │                                   introduction. Every "Home" link lands here
│   ├── commentary/                     The commentary, as the site serves it
│   │   ├── index.html                  Full-chapter view: ?book=ROM&ch=8
│   │   ├── osis.js                     OSIS parsing, shared with the pane
│   │   └── data/{BOOK}.js              Generated wrappers (27 files)
│   ├── rcb/                            The viewer's data — the viewer itself is above
│   │   ├── index.html                  Redirect stub; the viewer used to live here
│   │   ├── books.js                    Shared RCB_BOOKS map + rcbLink(), used by all reports
│   │   └── data/
│   │       ├── MAT.js ... REV.js       Generated from usfm/nt/{BOOK}.usfm (27 books)
│   │       ├── index.js                Book/chapter/verse index for the picker
│   │       ├── topics.js               Both reports, stripped to what the pane shows
│   │       └── INTRO.js                The introduction — hand-written, not generated
│   └── reports/                        Interactive reports, one folder per topic
│       ├── osas/
│       │   ├── index.html              Interactive report
│       │   └── data.js                 Assessment data (JS variable)
│       └── determinism/
│           ├── index.html
│           └── data.js
│
├── CLAUDE.md                           Operations guide — pipelines, workflows, conventions
├── RCB-decisions.md                    Restored Context Bible decision log
├── run_instructions.md                 Checklist and run procedures
├── project_structure.md                This file
└── .gitignore
```

## Key Principles

1. **The commentary is the shared foundation.** The `osis/` folder contains the first-century readings with no theological framework applied. Every topic-specific assessment builds on these same readings. Never modify them for a specific topic.

2. **Source vs. published.** `osis/` and `usfm/` hold the sources; `docs/` holds thin generated wrappers of them for the site. The sources are the truth and the wrappers are regenerated from them. Nothing keeps its only copy under `docs/` — that directory reads as disposable build output, and the author's decision (2026-08-17) is that no source should sit there.

3. **Assessments are per-topic.** Each assessment folder (`nt-osas/`, `nt-determinism/`, etc.) contains JSON files produced by running a topic-specific assessment prompt against the neutral readings. The naming pattern is `{testament}-{topic}/`.

4. **Reports are self-contained.** Each report folder under `docs/reports/` contains an `index.html` and a `data.js`. The report loads its data via a relative `<script>` tag. Both outbound links are built by `../../rcb/books.js`: `commentaryLink()` points at `../../commentary/index.html?book=CODE&ch=N#{section}`, and `rcbLink()` at `../../index.html?book=CODE#vCH-V`.

5. **Cloudflare Pages serves `docs/` only.** It auto-deploys from `main` with `docs/` as the build output directory. Source `.md` files, assessment `.json` files, and prompts are in the repo but not served to the web. GitHub Pages is disabled — it was flaky with 260+ static files.

## File Naming Conventions

- **Book names:** No spaces. Number prefix attached. Examples: `Matthew`, `1Corinthians`, `2Timothy`, `Genesis`, `1Samuel`
- **Chapter numbers:** Zero-padded to two digits. Examples: `_01`, `_08`, `_22`
- **Full pattern:** `{Book}_{Chapter}.{ext}` — e.g., `Romans_08.json`
- **Commentary and Bible are per book, by USFM code:** `ROM.xml`, `ROM.usfm`, `ROM.js`

## Pipeline

```
neutral_reading.md + "Analyze {Book} {Chapter}"
        │
        ▼
  osis/{testament}/{BOOK}.xml                ← Pass 1: the commentary
        │
        ▼
  {topic}_assessment.md + the commentary
        │
        ▼
  assessments/{testament}-{topic}/{Book}_{Ch}.json   ← Pass 2: structured assessment
        │
        ▼
  Aggregate JSONs → docs/reports/{topic}/data.js
        │
        ▼
  docs/reports/{topic}/index.html            ← Interactive report

  osis/{testament}/{BOOK}.xml
        │
        ▼
  python scripts/gen_commentary_data.py {BOOK}
        │
        ▼
  docs/commentary/data/{BOOK}.js             ← what the site reads
```

## Model

All analysis is performed by **Claude Opus (Anthropic)**. The prompts used are in `prompts/`, and the site's own account of this is in the introduction (`docs/rcb/data/INTRO.js`).

## Adding a New Topic

1. Write an assessment prompt in `prompts/{topic}.md`
2. Run it against the neutral readings (2-3 agents at a time)
3. Output goes to `assessments/{testament}-{topic}/`
4. Aggregate JSONs into `docs/reports/{topic}/data.js`
5. Adapt the report template for the topic's categories and question
6. Carry over the link wiring — include `../../rcb/books.js` and call `rcbLink(...)` after `commentaryLink(...)` in each table-row builder. See CLAUDE.md, "RCB links in reports"
7. Introduce the report in `docs/rcb/data/INTRO.js` — that is where a reader
   learns the topical assessments exist. The commentary pane picks the report up
   automatically once `topics.js` is regenerated; it is not linked from the toolbar
   by design (the reports are not the front of the site)
