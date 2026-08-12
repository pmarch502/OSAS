# Neutral Reading Run -- Instructions

> **Completed run record.** All 260 NT chapters are done. Kept as the record of
> that run — the checklist below is history, not a work queue. For current
> procedure see `CLAUDE.md`, "Running Pass 1". Two filenames below are stale:
> the prompt is now `prompts/neutral_reading.md`, and `agent_prompt.md` was
> deleted long ago.

## What We're Doing

Running all 260 New Testament chapters through the neutral reading prompt (`neutral_reading_pass1.md`) to produce first-century textual analyses free of post-first-century theological frameworks. This is Pass 1 of a two-stage process. Pass 2 (OSAS assessment) will be built on these results later.

## How to Run

- Read the prompt from `neutral_reading_pass1.md`
- Run 2-3 agents at a time (to manage credit usage)
- Each agent gets the full prompt text with "Analyze {Book} {Chapter}" appended
- Each agent writes one file: `{Book}_{ChapterPadded}.md` (e.g., `Romans_08.md`, `1John_02.md`)
- Use model: opus
- Do NOT add format instructions, OSAS framing, or output structure -- just the prompt + "Analyze {Book} {Chapter}. Write your full analysis to a file called {filename} in the current working directory."

## File Naming Convention

- Book names match standard abbreviations with no spaces
- Chapter numbers are zero-padded to two digits
- Examples: `Matthew_01.md`, `1Corinthians_16.md`, `Revelation_22.md`

## Important

- Do NOT use the old long prompt (agent_prompt.md) -- it was deleted
- Do NOT add OSAS/eternal security/conditionality framing to the agent prompt
- The prompt's power comes from its simplicity -- don't add to it
- Agents should NOT be told what to conclude or what to look for beyond what the prompt says

## Chapter Checklist

Mark each chapter [x] as it completes successfully. Review output before marking complete.

### Matthew (28)
- [x] Matthew 1
- [x] Matthew 2
- [x] Matthew 3
- [x] Matthew 4
- [x] Matthew 5
- [x] Matthew 6
- [x] Matthew 7
- [x] Matthew 8
- [x] Matthew 9
- [x] Matthew 10
- [x] Matthew 11
- [x] Matthew 12
- [x] Matthew 13
- [x] Matthew 14
- [x] Matthew 15
- [x] Matthew 16
- [x] Matthew 17
- [x] Matthew 18
- [x] Matthew 19
- [x] Matthew 20
- [x] Matthew 21
- [x] Matthew 22
- [x] Matthew 23
- [x] Matthew 24
- [x] Matthew 25
- [x] Matthew 26
- [x] Matthew 27
- [x] Matthew 28

### Mark (16)
- [x] Mark 1
- [x] Mark 2
- [x] Mark 3
- [x] Mark 4
- [x] Mark 5
- [x] Mark 6
- [x] Mark 7
- [x] Mark 8
- [x] Mark 9
- [x] Mark 10
- [x] Mark 11
- [x] Mark 12
- [x] Mark 13
- [x] Mark 14
- [x] Mark 15
- [x] Mark 16

### Luke (24)
- [x] Luke 1
- [x] Luke 2
- [x] Luke 3
- [x] Luke 4
- [x] Luke 5
- [x] Luke 6
- [x] Luke 7
- [x] Luke 8
- [x] Luke 9
- [x] Luke 10
- [x] Luke 11
- [x] Luke 12
- [x] Luke 13
- [x] Luke 14
- [x] Luke 15
- [x] Luke 16
- [x] Luke 17
- [x] Luke 18
- [x] Luke 19
- [x] Luke 20
- [x] Luke 21
- [x] Luke 22
- [x] Luke 23
- [x] Luke 24

### John (21)
- [x] John 1
- [x] John 2
- [x] John 3
- [x] John 4
- [x] John 5
- [x] John 6
- [x] John 7
- [x] John 8
- [x] John 9
- [x] John 10
- [x] John 11
- [x] John 12
- [x] John 13
- [x] John 14
- [x] John 15
- [x] John 16
- [x] John 17
- [x] John 18
- [x] John 19
- [x] John 20
- [x] John 21

### Acts (28)
- [x] Acts 1
- [x] Acts 2
- [x] Acts 3
- [x] Acts 4
- [x] Acts 5
- [x] Acts 6
- [x] Acts 7
- [x] Acts 8
- [x] Acts 9
- [x] Acts 10
- [x] Acts 11
- [x] Acts 12
- [x] Acts 13
- [x] Acts 14
- [x] Acts 15
- [x] Acts 16
- [x] Acts 17
- [x] Acts 18
- [x] Acts 19
- [x] Acts 20
- [x] Acts 21
- [x] Acts 22
- [x] Acts 23
- [x] Acts 24
- [x] Acts 25
- [x] Acts 26
- [x] Acts 27
- [x] Acts 28

### Romans (16)
- [x] Romans 1
- [x] Romans 2
- [x] Romans 3
- [x] Romans 4
- [x] Romans 5
- [x] Romans 6
- [x] Romans 7
- [x] Romans 8
- [x] Romans 9
- [x] Romans 10
- [x] Romans 11
- [x] Romans 12
- [x] Romans 13
- [x] Romans 14
- [x] Romans 15
- [x] Romans 16

### 1 Corinthians (16)
- [x] 1 Corinthians 1
- [x] 1 Corinthians 2
- [x] 1 Corinthians 3
- [x] 1 Corinthians 4
- [x] 1 Corinthians 5
- [x] 1 Corinthians 6
- [x] 1 Corinthians 7
- [x] 1 Corinthians 8
- [x] 1 Corinthians 9
- [x] 1 Corinthians 10
- [x] 1 Corinthians 11
- [x] 1 Corinthians 12
- [x] 1 Corinthians 13
- [x] 1 Corinthians 14
- [x] 1 Corinthians 15
- [x] 1 Corinthians 16

### 2 Corinthians (13)
- [x] 2 Corinthians 1
- [x] 2 Corinthians 2
- [x] 2 Corinthians 3
- [x] 2 Corinthians 4
- [x] 2 Corinthians 5
- [x] 2 Corinthians 6
- [x] 2 Corinthians 7
- [x] 2 Corinthians 8
- [x] 2 Corinthians 9
- [x] 2 Corinthians 10
- [x] 2 Corinthians 11
- [x] 2 Corinthians 12
- [x] 2 Corinthians 13

### Galatians (6)
- [x] Galatians 1
- [x] Galatians 2
- [x] Galatians 3
- [x] Galatians 4
- [x] Galatians 5
- [x] Galatians 6

### Ephesians (6)
- [x] Ephesians 1
- [x] Ephesians 2
- [x] Ephesians 3
- [x] Ephesians 4
- [x] Ephesians 5
- [x] Ephesians 6

### Philippians (4)
- [x] Philippians 1
- [x] Philippians 2
- [x] Philippians 3
- [x] Philippians 4

### Colossians (4)
- [x] Colossians 1
- [x] Colossians 2
- [x] Colossians 3
- [x] Colossians 4

### 1 Thessalonians (5)
- [x] 1 Thessalonians 1
- [x] 1 Thessalonians 2
- [x] 1 Thessalonians 3
- [x] 1 Thessalonians 4
- [x] 1 Thessalonians 5

### 2 Thessalonians (3)
- [x] 2 Thessalonians 1
- [x] 2 Thessalonians 2
- [x] 2 Thessalonians 3

### 1 Timothy (6)
- [x] 1 Timothy 1
- [x] 1 Timothy 2
- [x] 1 Timothy 3
- [x] 1 Timothy 4
- [x] 1 Timothy 5
- [x] 1 Timothy 6

### 2 Timothy (4)
- [x] 2 Timothy 1
- [x] 2 Timothy 2
- [x] 2 Timothy 3
- [x] 2 Timothy 4

### Titus (3)
- [x] Titus 1
- [x] Titus 2
- [x] Titus 3

### Philemon (1)
- [x] Philemon 1

### Hebrews (13)
- [x] Hebrews 1
- [x] Hebrews 2
- [x] Hebrews 3
- [x] Hebrews 4
- [x] Hebrews 5
- [x] Hebrews 6
- [x] Hebrews 7
- [x] Hebrews 8
- [x] Hebrews 9
- [x] Hebrews 10
- [x] Hebrews 11
- [x] Hebrews 12
- [x] Hebrews 13

### James (5)
- [x] James 1
- [x] James 2
- [x] James 3
- [x] James 4
- [x] James 5

### 1 Peter (5)
- [x] 1 Peter 1
- [x] 1 Peter 2
- [x] 1 Peter 3
- [x] 1 Peter 4
- [x] 1 Peter 5

### 2 Peter (3)
- [x] 2 Peter 1
- [x] 2 Peter 2
- [x] 2 Peter 3

### 1 John (5)
- [x] 1 John 1
- [x] 1 John 2
- [x] 1 John 3
- [x] 1 John 4
- [x] 1 John 5

### 2 John (1)
- [x] 2 John 1

### 3 John (1)
- [x] 3 John 1

### Jude (1)
- [x] Jude 1

### Revelation (22)
- [x] Revelation 1
- [x] Revelation 2
- [x] Revelation 3
- [x] Revelation 4
- [x] Revelation 5
- [x] Revelation 6
- [x] Revelation 7
- [x] Revelation 8
- [x] Revelation 9
- [x] Revelation 10
- [x] Revelation 11
- [x] Revelation 12
- [x] Revelation 13
- [x] Revelation 14
- [x] Revelation 15
- [x] Revelation 16
- [x] Revelation 17
- [x] Revelation 18
- [x] Revelation 19
- [x] Revelation 20
- [x] Revelation 21
- [x] Revelation 22
