# Assessment Prompt — Determinism / Free Will

You are evaluating a neutral first-century textual reading for its bearing on one specific question: **Does the text present God as unilaterally determining who will be saved and who will not — or does it present human beings as genuine agents whose choices affect their standing before God?**

You are NOT re-reading the biblical text. The neutral reading has already been done. Your job is to assess what that reading implies for this question.

## Input

You will be given the complete Pass 1 neutral reading for a single New Testament chapter. The reading is divided into sections, each covering a pericope (a coherent unit of the author's argument).

## Categories

Classify each section into exactly one category:

1. **NOT_APPLICABLE** — The text does not touch the question of divine determination versus human agency in any meaningful way.

2. **MISAPPLIED** — The passage is conventionally cited in debates about predestination or free will, but the neutral reading reveals it is actually about something else (corporate election, vocational calling, Israel's covenant role, historical events, etc.). You must state what it is conventionally cited to prove and what the neutral reading shows it actually addresses.

3. **LEANS_DETERMINISTIC** — The text has implications favoring divine determination of salvation outcomes, but either (a) it is not directly addressing who determines salvation, or (b) it addresses it with some ambiguity.

4. **LEANS_LIBERTARIAN** — The text has implications favoring genuine human agency in salvation outcomes, but either (a) it is not directly addressing who determines salvation, or (b) it addresses it with some ambiguity.

5. **STRONG_DETERMINISTIC** — The text directly addresses God as the one who determines salvation outcomes, AND does so as part of the author's own argument (not an illustration, aside, or assumption).

6. **STRONG_LIBERTARIAN** — The text directly addresses human beings as genuine agents whose choices determine their salvation outcome, AND does so as part of the author's own argument (not an illustration, aside, or assumption).

## Conventional proof-texts to watch for

The following passages are frequently cited in the predestination / free will debate. When the neutral reading covers any of these, pay special attention to the `conventional_use` and `category` fields — especially whether the neutral reading supports the conventional use or reveals the passage is about something else (MISAPPLIED).

### Commonly cited FOR determinism (Calvinist / predestinarian)
- John 1:12-13 — "born not of the will of the flesh nor of the will of man, but of God"
- John 6:37, 44, 65 — "all that the Father gives me," "no one can come unless the Father draws him"
- John 10:26 — "you do not believe because you are not among my sheep"
- John 15:16 — "you did not choose me, but I chose you"
- Acts 13:48 — "as many as were appointed to eternal life believed"
- Romans 8:28-30 — foreknew, predestined, called, justified, glorified
- Romans 9:10-24 — Jacob and Esau, potter and clay, vessels of wrath/mercy
- Romans 11:5-7 — "a remnant chosen by grace"
- 1 Corinthians 1:27-28 — "God chose the foolish"
- Galatians 1:15 — "set me apart before I was born"
- Ephesians 1:3-14 — election, predestination, "according to the purpose of his will"
- Ephesians 2:1-5 — "dead in trespasses," "made us alive"
- Philippians 1:29 — "it has been granted to you to believe"
- 2 Thessalonians 2:13 — "God chose you … to be saved"
- 2 Timothy 1:9 — "called us … not because of our works but because of his own purpose"
- 1 Peter 1:1-2 — "elect … according to the foreknowledge of God"
- 1 Peter 2:8 — "they stumble … as they were destined to do"
- Revelation 13:8; 17:8 — names written in the book of life "before the foundation of the world"

### Commonly cited FOR human agency (Arminian / free will)
- Matthew 11:28-30 — "come to me, all who labor"
- Matthew 23:37 — "how often would I have gathered … and you were not willing"
- Mark 16:15-16 — "whoever believes … whoever does not believe"
- John 1:12 — "to all who did receive him, who believed in his name"
- John 3:16, 18 — "whoever believes"
- John 5:40 — "you refuse to come to me"
- John 7:17 — "if anyone's will is to do God's will"
- John 12:32 — "I will draw all people to myself"
- Acts 2:21 — "everyone who calls upon the name of the Lord shall be saved"
- Acts 7:51 — "you always resist the Holy Spirit"
- Acts 17:30 — "commands all people everywhere to repent"
- Romans 1:16 — "to everyone who believes"
- Romans 10:9-13 — "if you confess … you will be saved … everyone who calls"
- 1 Timothy 2:3-4 — "God desires all people to be saved"
- 1 Timothy 4:10 — "Savior of all people, especially of those who believe"
- 2 Peter 3:9 — "not wishing that any should perish"
- Revelation 3:20 — "if anyone hears my voice and opens the door"
- Revelation 22:17 — "let the one who is thirsty come; let the one who desires take"

This list is not exhaustive. If the neutral reading covers a passage you recognize as part of the debate but not listed here, still flag it appropriately.

## Rules

- Work ONLY from the neutral reading provided. Do not re-exegete the biblical text. Do not import any post-first-century theological framework.
- For MISAPPLIED: state what the passage is conventionally cited to prove and what the neutral reading shows it actually addresses. Note which side conventionally cites it.
- Do not conflate "election to purpose/service/covenant role" with "election to individual eternal salvation." If the neutral reading distinguishes these, respect that distinction.
- Do not conflate "God initiates" with "God unilaterally determines." A text that says God calls, invites, or draws does not automatically imply determinism — it implies determinism only if human response is excluded or rendered irrelevant.
- Do not conflate "human response" with "human merit." A text that presents faith as a genuine human response does not automatically imply works-righteousness.
- Be honest about ambiguity. If a passage genuinely supports both readings, say so, explain why, then make your best judgment call on category.
- The question is narrow: who determines salvation outcomes — not general themes of God's sovereignty, providence, ethics, eschatology, or church order unless they directly bear on whether God unilaterally determines who is saved or humans genuinely choose.

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
      "category": "LEANS_LIBERTARIAN",
      "conventional_use": "not_in_debate | cited_for_determinism | cited_for_agency | cited_by_both",
      "summary": "What the neutral reading found this passage is about — one sentence.",
      "relevance": "Why this bears on the determinism/agency question — one to three sentences.",
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
- **conventional_use**: Whether this passage is conventionally cited in the predestination/free will debate, and by which side. Use your knowledge of the theological debate for this field only.
- **summary**: One sentence stating what the neutral reading determined this passage is about. Do not editorialize.
- **relevance**: Why this passage bears on the question. Required for all categories except NOT_APPLICABLE.
- **key_phrases**: The specific words or phrases from the text that drive your categorization. Required for all categories except NOT_APPLICABLE.
- **confidence**: Your confidence in the categorization. "high" = the category is clear from the neutral reading. "medium" = reasonable people could disagree on category but not on relevance. "low" = the passage's bearing on the question is debatable.
