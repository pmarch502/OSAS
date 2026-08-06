# Assessment Prompt — Pass 2

You are evaluating a neutral first-century textual reading for its bearing on one specific question: **Does the believer's standing before God, once established, remain permanent regardless of subsequent conduct — or is it conditional on ongoing faithfulness?**

You are NOT re-reading the biblical text. The neutral reading has already been done. Your job is to assess what that reading implies for this question.

## Input

You will be given the complete Pass 1 neutral reading for a single New Testament chapter. The reading is divided into sections, each covering a pericope (a coherent unit of the author's argument).

## Categories

Classify each section into exactly one category:

1. **NOT_APPLICABLE** — The text does not touch the question of the believer's standing before God in any meaningful way.

2. **MISAPPLIED** — The passage is conventionally cited in debates about eternal security or conditional security, but the neutral reading reveals it is actually about something else (corporate election, vocational calling, Israel's covenant faithfulness, eschatological hope, etc.). You must state what it is conventionally cited to prove and what the neutral reading shows it actually addresses.

3. **LEANS_CONDITIONAL** — The text has implications favoring conditionality, but either (a) it is not directly addressing the believer's standing, or (b) it addresses it with some ambiguity.

4. **LEANS_PERMANENT** — The text has implications favoring permanence, but either (a) it is not directly addressing the believer's standing, or (b) it addresses it with some ambiguity.

5. **STRONG_CONDITIONAL** — The text directly addresses whether a believer's standing can be lost, AND does so as part of the author's own argument (not an illustration, aside, or assumption).

6. **STRONG_PERMANENT** — The text directly addresses whether a believer's standing is guaranteed/permanent, AND does so as part of the author's own argument (not an illustration, aside, or assumption).

## Conventional proof-texts to watch for

The following passages are frequently cited in the eternal security / conditional security debate. When the neutral reading covers any of these, pay special attention to the `conventional_use` and `category` fields — especially whether the neutral reading supports the conventional use or reveals the passage is about something else (MISAPPLIED).

### Commonly cited FOR permanence (eternal security / OSAS)
- John 3:16, 36 — "shall not perish," "has eternal life"
- John 5:24 — "has passed from death to life"
- John 6:37-40 — "I will never cast out," "lose nothing," "raise it up"
- John 10:27-29 — "no one will snatch them out of my hand"
- John 17:11-12 — Jesus's prayer for the disciples' preservation
- Romans 5:9-10 — "saved by his life"
- Romans 8:1 — "no condemnation"
- Romans 8:28-30 — the "golden chain" (foreknew, predestined, called, justified, glorified)
- Romans 8:35-39 — "nothing can separate us"
- Romans 11:29 — "the gifts and calling of God are irrevocable"
- 1 Corinthians 1:8-9 — "will sustain you to the end"
- 1 Corinthians 3:15 — "saved, yet so as through fire"
- 2 Corinthians 1:22; 5:5 — the Spirit as "guarantee" (arrabōn)
- Ephesians 1:3-14 — election, predestination, sealed with the Spirit
- Ephesians 2:8-9 — "by grace through faith, not of works"
- Ephesians 4:30 — "sealed for the day of redemption"
- Philippians 1:6 — "he who began a good work will complete it"
- 2 Timothy 1:12 — "he is able to guard what I have entrusted"
- 2 Timothy 2:13 — "if we are faithless, he remains faithful"
- 1 Peter 1:3-5 — "kept by the power of God"
- 1 John 2:19 — "they went out because they were not of us"
- 1 John 5:13 — "that you may know you have eternal life"
- Jude 24 — "able to keep you from stumbling"

### Commonly cited FOR conditionality (against eternal security)
- Matthew 7:21-23 — "I never knew you"
- Matthew 10:22; 24:13 — "the one who endures to the end will be saved"
- Matthew 24:45-51; 25:1-13, 14-30 — parables of readiness (faithful/unfaithful servant, virgins, talents)
- Luke 8:13 — "they believe for a while and in time of testing fall away"
- John 15:1-6 — the vine and branches ("thrown away," "burned")
- Romans 11:17-22 — "you will be cut off"
- 1 Corinthians 9:27 — "lest I myself should be disqualified"
- 1 Corinthians 10:1-12 — Israel's example, "let anyone who thinks he stands take heed"
- Galatians 5:4 — "you have fallen from grace"
- Colossians 1:21-23 — "if indeed you continue in the faith"
- 1 Timothy 4:1 — "some will depart from the faith"
- 2 Timothy 2:12 — "if we deny him, he will deny us"
- Hebrews 2:1-3 — "how shall we escape if we neglect"
- Hebrews 3:6, 14 — "if we hold fast"
- Hebrews 6:4-8 — "impossible to restore again to repentance"
- Hebrews 10:26-31 — "if we go on sinning deliberately"
- Hebrews 10:35-39 — "do not throw away your confidence"
- James 5:19-20 — "whoever brings back a sinner from wandering will save his soul from death"
- 2 Peter 2:20-22 — "worse for them than the beginning"
- Revelation 2-3 — conditional promises in the letters to the churches
- Revelation 3:5 — "I will never blot out his name from the book of life"
- Revelation 22:19 — "God will take away his share in the tree of life"

This list is not exhaustive. If the neutral reading covers a passage you recognize as part of the debate but not listed here, still flag it appropriately.

## Rules

- Work ONLY from the neutral reading provided. Do not re-exegete the biblical text. Do not import any post-first-century theological framework.
- For MISAPPLIED: state what the passage is conventionally cited to prove and what the neutral reading shows it actually addresses. Note which side conventionally cites it.
- A passage that warns about consequences for behavior WITHIN the believing community is relevant to the question — do not dismiss warnings simply because they are addressed to believers.
- A passage that describes God's faithfulness or promises is relevant — do not dismiss permanence language simply because it is corporate or covenantal.
- Do not conflate "election to purpose/service" with "election to eternal salvation." If the neutral reading distinguishes these, respect that distinction.
- Be honest about ambiguity. If a passage genuinely supports both readings, say so, explain why, then make your best judgment call on category.
- The question is narrow: the believer's STANDING before God — not general themes of God's character, ethics, eschatology, or church order unless they directly bear on whether that standing is permanent or conditional.

## Output

Produce valid JSON — no markdown fencing, no commentary outside the JSON. The structure:

```
{
  "book": "Matthew",
  "chapter": 5,
  "sections": [
    {
      "reference": "5:13-16",
      "section_title": "Salt and Light",
      "category": "LEANS_CONDITIONAL",
      "conventional_use": "not_in_debate | cited_for_permanence | cited_for_conditionality | cited_by_both",
      "summary": "What the neutral reading found this passage is about — one sentence.",
      "relevance": "Why this bears on the permanence/conditionality question — one to three sentences.",
      "key_phrases": ["if salt has lost its taste", "no longer good for anything except to be thrown out"],
      "confidence": "high | medium | low"
    }
  ]
}
```

For NOT_APPLICABLE sections, only `reference`, `section_title`, `category`, and `summary` are required.

### Field definitions

- **reference**: Verse range for this section.
- **section_title**: Brief description of what this section covers (use the section heading from the neutral reading if available).
- **category**: One of the six categories above.
- **conventional_use**: Whether this passage is conventionally cited in the eternal security debate, and by which side. Use your knowledge of the theological debate for this field only.
- **summary**: One sentence stating what the neutral reading determined this passage is about. Do not editorialize.
- **relevance**: Why this passage bears on the question. Required for all categories except NOT_APPLICABLE.
- **key_phrases**: The specific words or phrases from the text that drive your categorization. Required for all categories except NOT_APPLICABLE.
- **confidence**: Your confidence in the categorization. "high" = the category is clear from the neutral reading. "medium" = reasonable people could disagree on category but not on relevance. "low" = the passage's bearing on the question is debatable.
