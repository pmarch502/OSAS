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
 */

var RCB_BOOKS = { 'Galatians': 'GAL', 'Ephesians': 'EPH', 'Philippians': 'PHP', 'Colossians': 'COL', '1 Thessalonians': '1TH', '2 Thessalonians': '2TH', '1 Timothy': '1TI', '2 Timothy': '2TI', 'Titus': 'TIT', 'Philemon': 'PHM' };

function rcbLink(book, chapter, reference) {
  var code = RCB_BOOKS[book];
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
