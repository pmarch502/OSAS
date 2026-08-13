/* Shared RCB link helper for all reports.
 *
 * Include from a report with:
 *   <script src="../../rcb/books.js"></script>
 * before the report's inline script.
 *
 * Adding a translated book: add one entry to RCB_BOOKS below. Every report
 * that includes this file picks it up — no per-report edits.
 *
 * Assumes the including page sits at docs/reports/{topic}/index.html (the
 * href below is relative to the page, not to this file) and that the page
 * defines the .exegesis-link CSS class.
 *
 * Numbered books are spelled inconsistently across the reports — the OSAS
 * data.js says '1 Corinthians', the determinism one says '1Corinthians', and
 * determinism is inconsistent with itself ('1 Peter' and '1Peter' both occur).
 * So the lookup falls back to a space-stripped key. RCB_BOOKS keeps one entry
 * per book in the spaced form; do not add a second entry for a variant.
 */

var RCB_BOOKS = { 'Matthew': 'MAT', 'Mark': 'MRK', 'Romans': 'ROM', '1 Corinthians': '1CO', '2 Corinthians': '2CO', 'Galatians': 'GAL', 'Hebrews': 'HEB', 'Ephesians': 'EPH', 'Philippians': 'PHP', 'Colossians': 'COL', '1 Thessalonians': '1TH', '2 Thessalonians': '2TH', '1 Timothy': '1TI', '2 Timothy': '2TI', 'Titus': 'TIT', 'Philemon': 'PHM', 'James': 'JAS', '1 Peter': '1PE', '2 Peter': '2PE', '1 John': '1JN', '2 John': '2JN', '3 John': '3JN', 'Jude': 'JUD', 'Revelation': 'REV' };

var RCB_BOOKS_NOSPACE = (function () {
  var m = {};
  for (var k in RCB_BOOKS) { m[k.replace(/\s+/g, '')] = RCB_BOOKS[k]; }
  return m;
})();

function rcbLink(book, chapter, reference) {
  var code = RCB_BOOKS[book] || RCB_BOOKS_NOSPACE[String(book).replace(/\s+/g, '')];
  if (!code) return '';
  var frag = 'ch' + chapter;
  if (reference) {
    var colonIdx = reference.indexOf(':');
    if (colonIdx >= 0) {
      var afterColon = reference.substring(colonIdx + 1);
      var dash = afterColon.indexOf('-');
      var v = dash >= 0 ? afterColon.substring(0, dash) : afterColon;
      frag = 'v' + chapter + '-' + v;
    }
  }
  return ' <a class="exegesis-link" href="../../rcb/index.html?book=' + code + '#' + frag + '" target="_blank" title="Restored Context Bible: ' + book + ' ' + chapter + '">RCB</a>';
}
