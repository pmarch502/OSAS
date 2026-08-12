# Restored Context Bible Prompt — Translation + Restoration

You are producing an original English translation from the Greek New Testament (NA28/UBS5 critical text, noting major variants) with contextual restorations woven into it. Translation and restorations are produced together, chapter by chapter. Read the neutral reading in `exegesis/nt/{Book}_{Ch}.md` first — it is the primary reference for what the restorations say. Do not introduce a historical, cultural, or linguistic claim it does not support, and do not let any post-first-century theology into either layer.

`RCB-decisions.md` governs. Where it settles a question, follow it. Where it is silent, follow `usfm/nt/GAL.usfm`, the proof of concept and reference example. If you must decide something neither one covers, make the decision, apply it consistently through the chapter, and report it when you finish so it can be added to the decision log. Do not edit the decision log yourself.

The two layers do different jobs and must not do each other's. The base text is formal-leaning but not wooden, keeps complex sentence structure wherever English can carry it, preserves Greek ambiguities rather than resolving them, and does no interpretive smoothing — it says what the Greek says. The restorations carry the context. When you are tempted to smooth an ambiguity in the translation, that is a restoration's work.

Translate key terms consistently as much as possible but allow for varying when required by the context. Example exceptions are named in the decision log: πίστις, νόμος, and χάρις each span a genuine semantic range in Greek — faith / faithfulness / trust / loyalty; law / Torah / principle; grace / favor. Render each by the sense the context requires, and let a restoration clarify which sense is in play.

A restoration supplies what the first-century hearer already knew and the modern reader has lost. It is not commentary, not application, and not a conclusion the text does not reach on its own.

If it completes the thought, it goes inline. If the reader has to stop and process it, it goes in a footnote. Use the decision log's production categories as your completeness check: definitional, rhetorical, morphological, audience ID, and historical restorations typically run inline; cross-references, source IDs, editorial notes, and alternative renderings typically become footnotes.

Restorations are written in the author's own voice, completing the argument he is already making. Match the reference example — step into an editorial voice only for cultural, historical, or linguistic background the author could not have said about himself.

Output USFM 3.x to `usfm/nt/{BOOK}.usfm`. Match the markup, bracket usage, and register of `usfm/nt/GAL.usfm`.
