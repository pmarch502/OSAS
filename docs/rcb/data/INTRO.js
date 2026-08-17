/* The introduction to the Restored Context Bible.
 *
 * Loaded by the viewer as ?book=INTRO and injected into the reading column, so
 * it uses the same shell, theme and measure as the text. Hand-written -- unlike
 * the book data files, nothing generates this.
 *
 * Plain HTML in a template literal: no backticks and no dollar-brace inside.
 */
var INTRO = `
<h1 class="book-title">Restored Context Bible</h1>

<div class="intro">
<p>A first-century reader of Paul's letters knew things we do not. He knew what a
household guardian was, what a covenant meal implied, what it meant to be cut off
from a synagogue. The letters were written to people who already had that in their
heads, so the writers never stopped to explain it &mdash; and two thousand years
later the explanation is exactly what is missing.</p>
<p>This translation puts it back, inside the sentence, where the first hearers
would have supplied it themselves.</p>
</div>

<h2 class="rcb-intro-h">What the brackets are</h2>

<p>Text in <span class="rcb-intro-eg">[square brackets and lighter type]</span> is not
in the Greek. It is context restored &mdash; what the writer assumed his readers
already knew, written into the sentence so it reads as one thought rather than as
a verse followed by an explanation. The technique is old: this is a modern English
targum, doing for a modern reader what the Aramaic targums did for synagogue
listeners who had stopped speaking Hebrew.</p>

<p>The test each one has to pass is that the sentence still reads naturally &mdash;
as though the writer had said it that way from the start. There is no target
number of them. Some chapters take many, some almost none.</p>

<p><strong>Turn them off any time.</strong> The <em>Restorations</em> button in the
toolbar hides every one of them and leaves the bare translation.</p>

<h2 class="rcb-intro-h">Footnotes, commentary, and the assessments</h2>

<p>Raised letters open footnotes: cross-references, textual notes, and alternative
renderings &mdash; the material that would break the reading if it were set inline.</p>

<p>The <em>Commentary</em> button opens a panel beside the text carrying a
verse-by-verse commentary on whatever passage you are reading, drawn from a study of
all 260 chapters of the New Testament. At the top of that panel one line reports
whether either topical assessment has anything to say about the passage in front of
you; opening it shows the verdict and links to the full report.</p>

<p>There are two assessments, each evaluating all 260 chapters:</p>

<ul>
<li><a href="reports/osas/index.html"><strong>Once Saved, Always Saved</strong></a>
&mdash; passage by passage, on the permanence or conditionality of a believer's
standing before God.</li>
<li><a href="reports/determinism/index.html"><strong>Determinism and Free
Will</strong></a> &mdash; passage by passage, on divine determinism versus human
agency in salvation.</li>
</ul>

<h2 class="rcb-intro-h">The text behind the translation</h2>

<p>This is an original translation from the Greek. It is not a revision of any
existing English version and carries no debt to one.</p>

<p>The base text is the NA28/UBS5 critical text, and this edition follows it
rather than the later tradition. That has visible consequences, and they are worth
knowing before you meet one:</p>

<p><strong>Sixteen verses of the traditional numbering are not here.</strong> They
are absent from the critical text, so the numbering skips them rather than
supplying them:</p>

<p class="rcb-intro-list">Matthew 17:21, 18:11, 23:14 &middot; Mark 7:16, 9:44, 9:46,
11:26, 15:28 &middot; Luke 17:36, 23:17 &middot; John 5:4 &middot; Acts 8:37,
15:34, 24:7, 28:29 &middot; Romans 16:24</p>

<p><strong>Passages the edition prints but marks as doubtful are included</strong>,
each with a footnote saying so at the point where it begins: the longer ending of
Mark (16:9&ndash;20), the woman taken in adultery (John 7:53&ndash;8:11), and in
Luke the angel in Gethsemane (22:43&ndash;44) and the word from the cross
(23:34). The principle is simply to follow the printed edition in both directions
&mdash; what it omits is omitted, what it brackets is kept and footnoted.</p>

<p>Where a familiar phrase is missing from inside a verse rather than a whole verse
being gone, a footnote marks it. In total the New Testament here runs to 7,943
verses.</p>

<h2 class="rcb-intro-h">How it was translated</h2>

<p>Every New Testament writer except Luke thinks like a Hebrew and writes in Greek.
Greek is the container, not the content. So where a Greek word is carrying a Hebrew
idea, this translation renders the idea rather than the container, and keeps the
shape of the thinking with it: concrete rather than abstract, the whole person
rather than a body with a soul inside it, verbs where English would reach for a
noun, parallel lines left untidied.</p>

<p>Luke is the exception &mdash; he thinks in Greek, and his Greek is translated as
Greek. Except where he writes in deliberate Septuagint style or quotes the Old
Testament, in Luke 1&ndash;2 and in the speeches in Acts, where the rest of the
rules apply again.</p>

<p>Where the Greek holds two readings open, the English tries to hold them open
too. Where English cannot, the translation picks one and a footnote carries the
other.</p>

<p>Translation and restoration are done separately, and in that order. A whole book
is translated first, with no context added and nothing resolved; that text is then
frozen, and a second pass adds the brackets, footnotes and headings without being
permitted to change a word of it. The separation is deliberate: a translator who
knows he can rescue a hard sentence later with a bracket will lean on it. All 27
books were translated whole rather than in pieces, because what a word means for a
writer can only be judged across everything he wrote.</p>

<h2 class="rcb-intro-h">The commentary</h2>

<p>Every chapter of the New Testament receives a first-century textual reading:
what does the text say, and what would its original audience have heard? The
readings use first-century tools only &mdash; the Septuagint, Second Temple
literature, the author's own usage across their writings &mdash; and do not import
any post-first-century theological framework.</p>

<p>These readings form a shared foundation. Topic-specific assessments then
evaluate the readings through a particular lens without re-reading or
reinterpreting the source text.</p>

<p>The readings are reviewed for factual errors and overlooked textual evidence.
Where a problem is identified, the passage is re-examined against the specific
textual question.</p>

<h2 class="rcb-intro-h">Who made this</h2>

<p>The translation, the restorations, the commentary and the assessments were all
produced by Claude, an AI model made by Anthropic, working from the Greek text and
from the prompts and method recorded in the project repository. They are reviewed
by the project's author for factual error and overlooked evidence, and corrected
where he finds either &mdash; but they have not been through the scrutiny a
published translation receives, and no committee stands behind them.</p>

<p>Read it as what it is: a serious attempt at restoring first-century context to
the New Testament, published openly so the method and every source can be checked.
The method, the prompts, the corrections log and all source materials are at
<a href="https://github.com/pmarch502/RCB">github.com/pmarch502/RCB</a>.</p>

<div class="rcb-intro-start">
<p>Choose a book from the toolbar to begin reading.</p>
</div>
`;
