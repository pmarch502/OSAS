# Corrections Log

Record of passages returned to Claude for re-analysis. Each entry documents what was flagged, the question sent, and the outcome.

---

## Format

```
### [Book Chapter]:[Verse(s)] — [Short description]
**Date:** YYYY-MM-DD
**File:** exegesis/nt/[filename].md
**Problem:** [What the original analysis got wrong or missed]
**Question sent:** [The specific textual question given to Claude via the correction prompt]
**Outcome:** [What Claude's re-analysis concluded — corrected / revised / original reading upheld]
**Assessment impact:** [Whether the Pass 2 assessment for this chapter needed to be re-run, and if the category changed]
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
