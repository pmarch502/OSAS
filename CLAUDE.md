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
- Same pattern applies for future `nt-predestination` reports

## Correction workflow

When the project author identifies a factual error or overlooked evidence:

1. **Fill in the correction prompt** (`prompts/correction.md`) with chapter, verse range, and problem statement. The problem flags what to re-examine — it does NOT give the answer.
2. **Run an agent** with the neutral reading prompt + filled correction prompt + current section text. Model: opus.
3. **Replace the section** in both `exegesis/nt/{Book}_{Ch}.md` and `docs/exegesis/nt/{Book}_{Ch}.html`.
4. **Check for ripple references**: grep other exegesis files for references to the corrected passage. Fix context summaries in adjacent chapters if needed.
5. **Update the corrections log** (`prompts/corrections_log.md`) with the problem, question sent, outcome, ripple fixes, and assessment impact.
6. **Re-run the assessment** for the affected section if the correction changes OSAS-relevant content. Update the assessment JSON, then regenerate `data.js`.

## Running Pass 1 (neutral reading)

- Prompt: `prompts/neutral_reading.md`
- Agent instruction: prompt text + "Analyze {Book} {Chapter}. Write your full analysis to a file called {filename}."
- Output: `exegesis/nt/{Book}_{Ch}.md`
- Model: opus
- Pacing: 2-3 agents at a time max
- Do NOT add topic framing, output structure, or conclusions to the prompt
- See `run_instructions.md` for the full 260-chapter checklist

## Running Pass 2 (assessment)

- Prompt: `prompts/osas.md` (or `prompts/predestination.md` for that topic)
- Input: the complete Pass 1 neutral reading for a single chapter
- Output: `assessments/nt-{topic}/{Book}_{Ch}.json`
- Model: opus
- Pacing: 2-3 agents at a time max
- After all chapters are done: regenerate `data.js` and verify the report

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
