# Restored Context Bible (RCB) — Decision Log

## Product
- **Name**: Restored Context Bible (RCB)
- **Technique name**: Contextual restoration (inline restorations woven into base text)
- **Heritage**: Modern English targum — same function as ancient targumim (bridging temporal/cultural gap)
- **Target platforms**: Bible Gateway, YouVersion, Bible apps, SWORD-based apps, web, print

## Format
- **Data format**: USFM (Unified Standard Format Markers, 3.x)
- **Derivative formats**: USX → Digital Bible Library; OSIS XML → SWORD modules; HTML → web
- **Restoration markup**: `\add [bracketed text]\add*` — plain `\add` marker, brackets baked into text
- **Brackets in text**: Yes — always visible regardless of platform support level
- **Morphological restorations**: `faith\add [fulness]\add*` — base word intact, extension marked

## Base Text
- **Original translation** from Greek (NT) — not derived from any copyrighted English translation
- **Source text basis**: NA28/UBS5 critical text, noting major variants
- **Translation philosophy**: Formal-leaning, not wooden (ESV range, not NASB-stiff or NIV-smooth)
  - Preserve Greek ambiguities — let restorations resolve them, not the translation
  - Keep complex sentence structure when intelligible in English
  - Translate key terms consistently rather than contextually varying
  - No interpretive smoothing — base text says what the Greek says, restorations add context
- **Key term decisions**:
  - ἐκκλησία (ekklēsia) → always "assembly" (no restoration needed)
  - Χριστός (Christos) → "the Christ" (title, not surname)
  - πίστις (pistis) → vary by context (faith / faithfulness / trust / loyalty); EA clarifies
  - νόμος (nomos) → vary by context (law / Torah / principle); EA clarifies
  - χάρις (charis) → vary by context (grace / favor); EA clarifies
  - More terms to be decided as Galatians translation proceeds

## Restoration Conventions
- All inline restorations render identically to the reader: bracketed text within `\add`
- No type distinctions in the product — it's all contextual restoration
- **Inline `\add [brackets]`** — restorations that make the text read fluidly without stopping
- **`\f` footnotes** — material that's important but would break reading flow:
  - Cross-references (`see Jeremiah 31:31-34`)
  - Textual/manuscript notes (`This verse is omitted in...`)
  - Alternative renderings (`better: ...`)
  - Deeper explanations that don't fit inline
- **Rule of thumb**: if it completes the thought, it's inline. If the reader has to stop and process, it's a footnote.
- **Production categories** (completeness checklist, not exposed to reader):
  - Definitional, Rhetorical, Morphological, Audience ID, Historical — typically inline
  - Cross-reference, Source ID, Editorial, Alternative rendering — typically footnotes

## Production Process
- Translation and restorations are produced together, chapter by chapter
- Primary reference: exegesis files in `exegesis/nt/` (260 chapters of first-century contextual analysis)
- Output: USFM files in TBD location
- Galatians is the proof of concept and reference example

## Scope & Sequence
- **Start with**: Galatians (translation + restorations, full proof of concept)
- **Then**: TBD (likely Romans, then remaining Pauline epistles)
- **Ultimate scope**: Full NT (27 books, 260 chapters)

## Rendering
- **USFM**: No special rendering — `\add` with brackets; platforms render as they will
- **HTML (our site)**: Custom styling, decisions deferred until we build it
- Brackets in the text guarantee restorations are always distinguishable regardless of platform

## Open Questions
- Remaining key term decisions (as they arise in translation)
