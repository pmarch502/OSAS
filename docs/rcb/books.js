/* Shared link helpers for all reports: out to the Bible, and out to the
 * commentary.
 *
 * Include from a report with:
 *   <script src="../../rcb/books.js"></script>
 * before the report's inline script.
 *
 * Adding a translated book: add one entry to RCB_BOOKS below. Every report
 * that includes this file picks it up — no per-report edits.
 *
 * Assumes the including page sits at docs/reports/{topic}/index.html (the
 * hrefs below are relative to the page, not to this file) and that the page
 * defines the .ref-link CSS class.
 *
 * The viewer lives at docs/index.html — it is the site's front door, and the
 * data it loads is what stayed behind in docs/rcb/. The link opens in the same
 * tab: the viewer remembers the reader's place, so Back and Home both work.
 *
 * Numbered books are spelled inconsistently across the reports — the OSAS
 * data.js says '1 Corinthians', the determinism one says '1Corinthians', and
 * determinism is inconsistent with itself ('1 Peter' and '1Peter' both occur).
 * So the lookup falls back to a space-stripped key. RCB_BOOKS keeps one entry
 * per book in the spaced form; do not add a second entry for a variant.
 */

var RCB_BOOKS = { 'Matthew': 'MAT', 'Mark': 'MRK', 'Luke': 'LUK', 'John': 'JHN', 'Acts': 'ACT', 'Romans': 'ROM', '1 Corinthians': '1CO', '2 Corinthians': '2CO', 'Galatians': 'GAL', 'Hebrews': 'HEB', 'Ephesians': 'EPH', 'Philippians': 'PHP', 'Colossians': 'COL', '1 Thessalonians': '1TH', '2 Thessalonians': '2TH', '1 Timothy': '1TI', '2 Timothy': '2TI', 'Titus': 'TIT', 'Philemon': 'PHM', 'James': 'JAS', '1 Peter': '1PE', '2 Peter': '2PE', '1 John': '1JN', '2 John': '2JN', '3 John': '3JN', 'Jude': 'JUD', 'Revelation': 'REV' };

var RCB_BOOKS_NOSPACE = (function () {
  var m = {};
  for (var k in RCB_BOOKS) { m[k.replace(/\s+/g, '')] = RCB_BOOKS[k]; }
  return m;
})();

function bookCode(book) {
  return RCB_BOOKS[book] || RCB_BOOKS_NOSPACE[String(book).replace(/\s+/g, '')] || '';
}

/* A few passages start in the previous chapter — John 7:53-8:11 sits on a row
 * whose chapter is 8, and 2 Corinthians 6:14-7:1 on a row whose reference is
 * '7:1'. The reference names the verse the passage opens on, so take the
 * chapter from it too rather than from the row. */
function refChapter(chapter, reference) {
  if (!reference) return chapter;
  var colonIdx = reference.indexOf(':');
  if (colonIdx < 0) return chapter;
  var refCh = parseInt(reference.substring(0, colonIdx), 10);
  return isNaN(refCh) ? chapter : refCh;
}

function rcbLink(book, chapter, reference) {
  var code = bookCode(book);
  if (!code) return '';
  var frag = 'ch' + chapter;
  if (reference) {
    var colonIdx = reference.indexOf(':');
    if (colonIdx >= 0) {
      var afterColon = reference.substring(colonIdx + 1);
      var dash = afterColon.indexOf('-');
      var v = dash >= 0 ? afterColon.substring(0, dash) : afterColon;
      frag = 'v' + refChapter(chapter, reference) + '-' + v;
    }
  }
  return ' <a class="ref-link" href="../../index.html?book=' + code + '#' + frag + '" title="Restored Context Bible: ' + book + ' ' + chapter + '">RCB</a>';
}

/* Out to the commentary, at the section this row is about.
 *
 * The anchor is the part of the reference after the colon — '12:13-18' becomes
 * '#13-18' — which is what Commentary.sectionId() produces on the other end.
 * That has been the contract since the commentary was 260 HTML files with
 * hand-written ids, and it survived the move to OSIS unchanged. */
function commentaryLink(book, chapter, reference) {
  var code = bookCode(book);
  if (!code) return '';
  var frag = '';
  if (reference) {
    var colonIdx = reference.indexOf(':');
    if (colonIdx >= 0) frag = '#' + reference.substring(colonIdx + 1);
  }
  return '<a class="ref-link" href="../../commentary/index.html?book=' + code +
         '&amp;ch=' + refChapter(chapter, reference) + frag +
         '" title="Commentary on ' + book + ' ' + chapter + '">Commentary</a>';
}
