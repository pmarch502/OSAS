# Corrections Log

Record of passages returned to Claude for re-analysis. Each entry documents what was flagged, the question sent, and the outcome.

---

## Format

```
### [Book Chapter]:[Verse(s)] — [Short description]
**Date:** YYYY-MM-DD
**File:** exegesis/nt/[filename].md — or usfm/nt/[BOOK].usfm for an RCB correction
**Problem:** [What the original analysis got wrong or missed]
**Question sent:** [The specific textual question given to Claude via the correction prompt]
**Outcome:** [What Claude's re-analysis concluded — corrected / revised / original reading upheld]
**Ripple fixes:** [Other files referencing the corrected passage that needed updating, or "checked, none needed"]
**Assessment impact:** [Whether the Pass 2 assessment for this chapter needed to be re-run, and if the category changed]
**RCB impact:** [Whether the book has an RCB translation and whether its EAs or footnotes needed updating — or "no RCB translation"]
```

---

## Corrections

### Hebrews 9:3-4 — chrysoun thymiaterion (censer vs. altar)
**Date:** 2026-08-07
**File:** exegesis/nt/Hebrews_09.md
**Problem:** The analysis identifies chrysoun thymiaterion as a "golden altar of incense" and then treats the censer reading as a secondary alternative. Please reconsider which items belonged in which place. Follow the author's own argument: he is cataloguing what belongs to the inner sanctuary.
**Outcome:** Corrected. Re-analysis determined thymiaterion is the LXX's word for a portable censer (2 Chronicles 26:19, Ezekiel 8:11), not the altar of incense (which the LXX consistently calls thysiastērion thymiamatos). The censer reading resolves the inventory problem: the outer room list is complete without the altar, and the inner room contains items the high priest encountered on Yom Kippur. The revised section also connects the censer to the Leviticus 16:12-13 ritual and Mishnah Yoma tradition of a distinctive golden censer for the Day of Atonement.
**Ripple fixes:** The context summaries in Hebrews 8 and Hebrews 10 (both md and html) referenced "golden altar of incense" when summarizing 9:1-5; updated to "golden censer."
**Assessment impact:** Checked. Hebrews 9:1-5 summary updated ("golden altar of incense" → "golden censer"). Hebrews 10 assessment does not reference 9:4 furnishings; no change needed. Category unchanged (NOT_APPLICABLE).

### Romans 8:28-30 — the aorist chain and Israel's history
**Date:** 2026-08-07
**File:** exegesis/nt/Romans_08.md
**Problem (pass 1):** The analysis treats the sequence in 8:29-30 (foreknew → predestined → called → justified → glorified) primarily as a description of God's purpose going forward. But the prompt's own rule requires determining whether God's actions have precedent or fulfillment in Israel's recorded history before considering any abstract reading. The analysis already connects proegno to 11:2 and identifies it as corporate and relational. Re-examine whether the remaining aorist verbs in the chain also have concrete referents in Israel's recorded history, and what that would mean for Paul's argument.
**Problem (pass 2):** The revised analysis of 8:28-30 references "the original reading" — remove this self-referential language. The treatment of edikaiosen is good on its own. Consider if there is an additional way in which Israel was justified (righteous-ified) among the nations. The analysis also grounds every verb in Israel's past but does not address why Paul is reciting this history to his audience — what is the rhetorical purpose of the chain in the context of Paul's argument?
**Outcome:** Corrected in two passes. First pass grounded every verb in Israel's history: foreknew (Amos 3:2, covenant with Abraham), predestined (Exodus 19:5-6, Deuteronomy 7:6, 32:8-9), called (Isaiah 51:2, 43:1, 41:9, 42:6; Hosea 11:1), justified (Genesis 15:6, Isaiah 45:25, 50:8), glorified (Exodus 40:34, 1 Kings 8:10-11, Isaiah 55:5). Second pass (same date) addressed three remaining issues: (1) removed self-referential language about "the original reading"; (2) strengthened edikaiosen by adding Torah-based justification — God constituted Israel as righteous among the nations through the gift of dikaiomata (Deuteronomy 4:8, cf. Paul's own use of dikaioma in 8:4 and 2:26), and the Day of Atonement as ongoing corporate justification (Leviticus 16:30, cf. hilasterion in 3:25); (3) added analysis of the rhetorical purpose of the chain — Paul recites God's completed acts to ground the confidence of an audience that is suffering (8:17-18), groaning (8:23), and too weak to pray (8:26), showing that the purpose has never depended on the believers' comprehension but on God's demonstrated faithfulness at every stage.
**Ripple fixes:** Checked. Romans 9 (context summary), Romans 11 (proginosko cross-reference), 1 Peter 1 (foreknowledge cross-reference), and 1 Corinthians 2 (proorisen cross-reference) all reference 8:29-30 in ways compatible with the corrected reading. No changes needed.
**Assessment impact:** Checked. Category changed from LEANS_PERMANENT to MISAPPLIED (high confidence). The corrected reading reveals the chain is a recitation of God's corporate historical acts with Israel, not an individual soteriological guarantee. The passage is conventionally cited for permanence but the neutral reading shows it addresses God's covenant faithfulness to his people as a people.

### Matthew 5:38-42 — Power dynamics in the four examples
**Date:** 2026-08-07
**File:** exegesis/nt/Matthew_05.md
**Problem:** The analysis correctly identifies the backhanded blow (v. 39b) as an insult from a superior to an inferior, and notes that the four responses go beyond mere compliance. Consider how each prescribed response functions within its first-century social context — specifically, how each response alters the power dynamic.
**Outcome:** Corrected. Re-analysis traced each scenario through its first-century social mechanics: (1) turning the left cheek makes a second backhanded blow physically impossible, forcing the aggressor to strike as an equal or stop; (2) stripping naked in court shifts shame onto the creditor per Jewish moral tradition (Genesis 9:20-27, Habakkuk 2:15); (3) the voluntary second mile puts the Roman soldier at risk of appearing to violate conscription limits; (4) giving/lending without calculating return strips the patronage transaction of its power to bind (Proverbs 22:7, Deuteronomy 15:7-11). The closing paragraph now identifies the pattern precisely: each response targets a specific mechanism of control and forces the oppressor into a dilemma they cannot resolve without conceding ground.
**Ripple fixes:** Checked. 1 Corinthians 6 (cross-reference to Matthew 5:39-40) already describes the response as "not passivity but a deliberate choice" — compatible with corrected reading. Mark 15 (angareuein cross-reference) notes the verb only. No changes needed.
**Assessment impact:** Checked. Category unchanged (NOT_APPLICABLE). Assessment summary updated to reflect corrected reading.

### Jude 14 — the aorist elthen, a coming stated as past
**Date:** 2026-08-12
**File:** usfm/nt/JUD.usfm — RCB correction, footnote only
**Problem:** Pass 1 rendered elthen literally as "the Lord came" — a Hebrew prophetic perfect, a still-future coming spoken of as already accomplished. Pass 1 flagged that the tense needed a footnote; pass 2 footnoted the 1 Enoch 1:9 source and the Deuteronomy 33:2 scene but never explained the tense, leaving a reader to meet a past-tense verb for a future judgment with nothing to go on.
**Outcome:** The existing Deuteronomy 33:2 footnote on the clause was extended rather than a second footnote added mid-clause. It now opens by naming the tense, explains the prophetic perfect as the prophets' way of speaking about what God has settled, notes that English would say "comes" or "will come" at the cost of the certainty the tense itself claims, and then keeps the Deuteronomy 33:2 court scene as before. Base text untouched.
**Ripple fixes:** Checked. No other footnote or EA in Jude depends on the tense of verse 14. The verse 6 footnote on the angels held until the judgment is compatible and needed no change. Markers balanced (25 add, 34 f, 18 tl), 25 verses. Regenerated docs/rcb/data/JUD.js.
**Assessment impact:** None. The exegesis of Jude is not affected — the correction is in the translation layer, and the underlying reading was already sound.

### Hebrews 9:4 — thymiaterion, base text against the corrected exegesis
**Date:** 2026-08-12
**File:** usfm/nt/HEB.usfm — RCB correction, base text and footnote
**Problem:** Pass 1 rendered thymiaterion "the golden altar of incense" — the reading the 2026-08-07 correction to exegesis/nt/Hebrews_09.md had already rejected. Pass 2 spotted the conflict but the base text was frozen to it, so it left the wording and argued the censer case in a footnote, leaving the book stating one reading and its own footnote calling the other likelier. The cause is structural, not an agent error: pass 1 translates blind and never reads the exegesis, so it has no access to the project's exegetical determinations, and pass 2 cannot apply them without breaking the freeze. Expect this wherever a logged correction turned on a lexical choice.
**Outcome:** Base text changed to "the golden censer," applying the project's own settled correction rather than a new judgment. The footnote was rewritten at the author's direction to present "the altar of incense" as the popular translation rather than as an alternative reading — it is technically incorrect and does not qualify as a live option. It now gives the censer of Leviticus 16:12-13, notes that the altar stood in the outer room (Exodus 30:6; 40:26), names the LXX's own word for that altar (thysiasterion thymiamatos), and closes on the author's argument: he is listing what belongs to the inner room.
**Ripple fixes:** Checked. check_freeze.py HEB reports exactly one differing line, the intended one — nothing else drifted from pass 1. No other footnote or EA in Hebrews depends on the 9:4 furnishing; the Uzziah footnote elsewhere is about presumption in priesthood, not the inventory. Markers balanced (60 add, 130 f, 13 tl), 303 verses across 13 chapters.
**Assessment impact:** None. The exegesis was already corrected in 2026-08-07 and the assessment updated then; this brings the translation into line with it.

### 1 Corinthians 15:49 — phoresomen, a variant with no note
**Date:** 2026-08-12
**File:** usfm/nt/1CO.usfm — RCB correction, footnote only
**Problem:** Pass 1 followed NA28 and rendered the subjunctive phoresomen "let us also wear the image of the heavenly man" — a summons where nearly every English version has the future indicative "we shall also bear." Pass 1 flagged it as the most visible of its NA28 readings and a good candidate for a variant footnote; pass 2 supplied none, so the verse shipped with an unusual reading and nothing to explain it. Not the Hebrews 9:4 case: there is no logged correction on 15:49, and the exegesis (1Corinthians_15.md) states the verb is future without mentioning that the manuscripts divide, so the base text is not defying a project determination. It falls under the RCB-decisions convention that the translation picks a reading and a footnote carries the other.
**Outcome:** Footnote added at the end of 15:49. It gives the manuscript split (nearly every early manuscript has the subjunctive, a few the future), says the future is what most English translations print, and explains that one letter separates them and that the two were pronounced alike in the first century, so a scribe writing from dictation could not have heard which was said. Written in the corpus register, without sigla. The argument that the declarative context favors the future was deliberately left out as commentary. Base text untouched.
**Ripple fixes:** Checked. Nothing else in 1 Corinthians references 15:49 or the image-of-Adam language; the 15:45 footnote is on Genesis 2:7 and needed no change. check_freeze.py cannot run post-publication (the pass-1 baseline is deleted), so the equivalent check was a strip-and-diff against the committed file: with footnotes removed, zero base-text differences. Markers balanced (181 add, 161 f, 43 tl), 437 verses. Regenerated docs/rcb/data/1CO.js.
**Assessment impact:** None. The correction is in the translation layer.

### 1 Corinthians 15:49 — the same variant, missing from the exegesis
**Date:** 2026-08-12
**File:** exegesis/nt/1Corinthians_15.md and docs/exegesis/nt/1Corinthians_15.html
**Problem:** The analysis stated flatly that "the verb phoresomen ... is the future tense" and quoted the verse as "we shall also bear," without noting that the manuscripts divide between the future indicative and the aorist subjunctive. Not an error in the reading, but a missing piece of textual history — and the gap was invisible until the RCB translated the other reading.
**Outcome:** Added one paragraph after the existing treatment of the verb, by manual edit at the author's direction, since it adds historical information rather than revising a reading. It gives the split (nearly every early witness has the subjunctive, a smaller group the future), the omega/omicron confusion and the first-century vowel merger that made the two indistinguishable in dictation, which side the external evidence and which side the context favors, and what changes under the subjunctive: the typology stands, but its last step becomes an exhortation — which is where the chapter ends in either case (verse 58). The existing analysis was left intact.
**Ripple fixes:** Checked. No other exegesis chapter references 15:49, phoresomen, or the image-of-Adam language; the apparent hits are karpophoresomen in Romans 7, a different verb. Markdown and HTML updated in parallel, HTML paragraph tags balanced.
**Assessment impact:** Checked, no change. Both the OSAS and determinism assessments cover 15:42-49 and both are NOT_APPLICABLE; neither turns on the mood of the verb. The OSAS summary's "it will bear the image" reflects the future reading, but the category and the relevance judgment stand under either.

### Matthew 6:13, 20:16, 25:13, 27:35 — four omissions left unexplained
**Date:** 2026-08-12
**File:** usfm/nt/MAT.usfm — RCB correction, footnotes only
**Problem:** Pass 1 followed the critical text and handed pass 2 four partial-verse omissions to footnote: the doxology at 6:13, and the additions at 20:16b, 25:13b, 27:35b. Pass 2 footnoted the three whole-verse omissions (17:21, 18:11, 23:14) but none of these four. The doxology is the one that matters — a reader who knows "For thine is the kingdom, and the power, and the glory" by heart meets a prayer that stops at "rescue us from evil" with nothing to go on. Same class of gap as 1 Corinthians 15:49.
**Outcome:** Four footnotes added, all following the formula pass 2 had already established in this book ("Some later copies add ... which the earliest copies do not have"). The doxology note goes further, because the reader's real question is why everyone says it: the Didache already carries a shorter form, Jewish prayer does not end on a bare request, and the words are David's at 1 Chronicles 29:11. The 20:16 note says the line is genuine but belongs at 22:14 and was carried back. The 25:13 note is the bare formula. At 27:35 the existing Psalm 22:18 footnote was extended rather than a second one added (the Jude 14 precedent) — it already made the point that no fulfilment formula is attached and the writer leaves the reader to notice, so the variant belongs on the end of it: later copies attach one and spend the restraint. Manuscripts are not named; the corpus register is plainer, and these are routine liturgical accretions rather than cases turning on external testimony as Mark's longer ending does. Base text untouched.
**Ripple fixes:** Checked. check_freeze.py cannot run post-publication (the pass-1 baseline is deleted), so the equivalent check was a strip-and-diff against the committed file: with footnotes removed, zero base-text differences across all 1484 lines. Markers balanced (235 add, 443 f, 68 tl); footnote count 440 to 443, the fourth being an extension rather than a new note. Regenerated docs/rcb/data/MAT.js.
**Assessment impact:** None. The correction is in the translation layer.

## Titus 2:7-10 — a heading, not a gap (2026-08-13)

**Problem:** `scripts/check_pane_coverage.py` reported Titus 2:7-10 as having no
exegesis section, and the commentary pane told readers so. It had been on the
expected-gaps list as "no section was written."

**What was actually wrong:** nothing in the analysis. `Titus_02` has a section
covering verses 2-10, with subsections `Verses 6-8: Younger Men and Titus as
Model` and `Verses 9-10: Slaves -- Conduct That Adorns the Doctrine`. Only the
`<h2>` was wrong: it read "Verses 2-6". The pane and the checker both take
section ranges from heading text, so the mislabelled heading invented a
four-verse hole in an otherwise complete New Testament.

**Fix:** heading corrected to "Verses 2-10" in `exegesis/nt/Titus_02.md` and
`docs/exegesis/nt/Titus_02.html`; the HTML anchor `id` moved from `2-6` to
`2-10`. Titus removed from `EXPECTED` in the checker, which now reports 13
uncovered verses rather than 17.

**Side effect:** the OSAS report's row for this passage links to
`Titus_02.html#2-10` (the anchor is built from the row's reference, `2:2-10`).
That anchor matched nothing before and now resolves. The determinism rows
`#6-8` and `#9-10` already resolved against the `<h3>` ids.

**Assessment impact:** none. Both assessments had always covered 2:7-10 —
OSAS as one section `2:2-10`, determinism split as `2:6-8` and `2:9-10` —
because they were run against the section text, not its heading. No JSON
changed, so no `data.js` or `topics.js` regeneration was needed.

**Worth carrying forward:** a reported coverage gap is more likely a
mislabelled heading than missing analysis. Read the section body first, and
cross-check the assessments — they read the text.

## Mark's five omitted verses, and Matthew 23:14 (2026-08-13)

**Problem:** an audit of all 16 verses the RCB omits found five with no
footnote anywhere in their book — Mark 7:16, 9:44, 9:46, 11:26, 15:28. A
reader met a jump in the numbering with nothing to explain it. Matthew 23:14
was footnoted but described only ("about devouring widows' houses") without
giving the wording.

**Why it was all Mark:** Mark was published (`4a22807`) before both fixes for
this. Matthew hit the same problem next and was hand-corrected (`61cdc62`),
and the pass-1 notes handoff that prevents it (`4a4e7aa`) came after both.
Every book from Luke onward had the mechanism, and all their omissions are
documented. Mark simply never got the pass Matthew got.

**Fix:** each omission now names the verse, quotes what it says, and states
that the earliest copies lack it — the pattern the other eleven already
follow. Where the preceding verse already carried a footnote (9:43, 11:25,
15:27, and Matthew 23:13) the existing note was **extended**, following the
Jude 14 precedent, rather than hanging a second note mid-sentence. Two notes
are new (7:15, 9:45). Mark's footnote count goes 225 to 227; Matthew's is
unchanged at 443.

Two of them fell out well. At 15:27 the note already quoted Isaiah 53:12
("numbered with the transgressors"), so the added sentence just says later
copies make that explicit as a verse 28. At 9:43 and 9:45 the omitted words
are the genuine line that stands at 9:48, repeated by copyists after each
warning, and the notes say so.

**Verification:** the pass-1 baselines are long gone, so `check_freeze.py`
could not run. Used the strip-and-diff substitute instead — remove every
`\f...\f*` and unwrap every `\add`, and diff against the pre-edit file:
**0 differing lines in the base text** for both books. Markers balanced
(MRK add/f/tl 200/227/50, MAT 235/443/68), no `\add` inside a footnote and no
footnote inside an `\add`, every `\s1` still followed by a `\p`, and the verse
count unchanged at 16 gaps. Regenerated both data files and confirmed the new
note text renders in the viewer.

**Assessment impact:** none — no base text changed.

## Galatians rewritten, and everything downstream rebuilt (2026-08-14)

**Problem:** not a passage correction. All six Galatians chapters were replaced
with new exegesis produced in a prior session. The author accepted them as
better than what they replaced while stating they still do not reflect
everything he argued, and directed that they be integrated as final for this
pass rather than corrected further. Everything downstream of the exegesis was
therefore stale: two sets of assessments, both reports, the commentary pane
index, and the RCB's amplification layer.

**Exegesis:** `docs/exegesis/nt/Galatians_0*.html` regenerated from the
markdown with `scripts/md_to_html.py`; byte-identical to what was already in
the working copy, so md and html agree. `check_pane_coverage.py` reports 0 new
uncovered verses. `check_framing.py` for the whole NT drops from 25 hits in 14
chapters to 18 in 11; Galatians goes from 7 to 2.

**Assessments:** all twelve re-run from the new readings — six OSAS, six
determinism. The section divisions themselves changed, not just the verdicts,
so no verdict could have been carried over: OSAS goes 38 sections to 30,
determinism 35 to 30. Chapter 6 went five sections to three in both. Verse
coverage is contiguous 1:1-6:18 in both topics.

Category changes that carry content, all traceable to the rewrite:

- OSAS 3:10-14, LEANS_PERMANENT to MISAPPLIED. The curse is the covenant
  sanction of Deuteronomy 27-30, and the rewrite judges the "nobody can keep
  it" premise the weakest of three.
- OSAS 4:21-31, LEANS_CONDITIONAL to MISAPPLIED — corporate covenant columns,
  with Paul putting himself in the free one.
- Determinism 3:19-22, LEANS_LIBERTARIAN to MISAPPLIED, on `ta panta` being
  neuter: the confinement is comprehensive, not a claim about individual
  capacity.
- Determinism 4:21-31 likewise to MISAPPLIED.
- OSAS 2:15-21 went LEANS_CONDITIONAL to LEANS_PERMANENT in both halves; the
  old reading took v18's "transgressor" as post-justification conduct, where
  the rewrite has the transgression being the reimposition of the Jew-Gentile
  separation.

Both `data.js` files regenerated (OSAS 1959 to 1951 rows, determinism 1975 to
1970) and `gen_topics_index.py` re-run — 3925 entries, 27 books.

**RCB impact:** the amplification was rebuilt from scratch rather than
repaired, at the author's direction: the EAs and footnotes were written from
the superseded exegesis and nothing in them was judged worth salvaging.

The pass-1 intermediate had been deleted at publication, so it was
reconstructed by stripping the five pass-2 markers out of the published book —
`check_freeze.py GAL` reports 0 against the reconstruction, so it is an exact
baseline and the freeze is verifiable again. One detail worth keeping: the
strip must *not* close up the space before an em-dash, which is spaced in this
text, or every `\add` that preceded one leaves the base text subtly wrong.
`check_freeze.py` normalizes both sides and would not catch it.

Galatians predates the pass-1 notes handoff, so there was no notes file. It
was written to say exactly that, with no mandated items, rather than
fabricating a list. Two facts make the loss small: no Galatians verse is
absent from the critical text, and the superseded book contained no
manuscript or variant footnotes at all.

Pass 2 output: 32 `\s1` headings, 77 `\add`, 119 footnotes, a four-paragraph
introduction. Verified independently of the agent's own report — markers
balanced 77/77, 119/119, 32/32; no `\add` inside a footnote and no footnote
inside an `\add`; every `\s1` followed by a `\p`; `\p` count 39 in both files;
no markers outside the permitted set; all 119 `\fr` references in range; verse
counts 24/21/29/31/26/18 with no numbering gaps. At 0.80 footnotes per verse
Galatians sits fifth of 27 books, inside the band the other short letters
already occupy (2 John 1.38, Jude 1.36, 2 Peter 0.89, Titus 0.76).
Regenerated `docs/rcb/data/GAL.js`.

**Ripple:** 147 references to Galatians across 83 other exegesis chapters. The
ones touching passages whose reading changed were read. One is affected and
was **left alone for the author to decide**: `exegesis/nt/Colossians_02.md`
says the stoicheia in Galatians are "associated with both the pre-Christian
Jewish observance of Torah (4:3-5)" and Gentile worship, and the rewritten
Galatians 4 explicitly refuses the stoicheia/Torah equation. Colossians is now
leaning on Galatians for a reading Galatians no longer holds. The rest are
inert citations — Abba at Romans 8, "by nature not gods" at Ephesians 2,
`kopiaō` at Colossians 1 and 1 Timothy 4, "fallen from grace" at 2 Peter 3 —
and none asserts a reading the rewrite overturned.
