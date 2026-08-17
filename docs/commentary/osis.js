/* Reading the OSIS commentary in the browser.
 *
 * Shared by the two pages that show commentary -- the pane in the Bible viewer
 * (docs/index.html) and the full-chapter page (docs/commentary/index.html) --
 * because a parser kept in two copies is a parser that will disagree with
 * itself. Nothing here touches the DOM of the host page.
 *
 * The source of truth is osis/nt/{BOOK}.xml at the repo root, carried into
 * docs/commentary/data/{BOOK}.js by scripts/gen_commentary_data.py. Same
 * arrangement as the Bible: source outside docs/, a thin wrapper inside it,
 * the real markup parsed here.
 */
/* Named Commentary, not OSIS: the data files declare `const OSIS` for the raw
 * XML, mirroring the Bible's `const USFM`, and the two must not collide. */
var Commentary = (function() {
  'use strict';

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* The passage a section is about, read from its annotateRef.
   *
   * This used to be guessed from heading text, and the guessing is why three
   * sections written years ago were never shown to anyone: a heading that did
   * not begin "Verses" got no id, and a section with no id was one the pane
   * never looked at. OSIS states the range, so nothing is inferred.
   *
   *   'Rom.8.1-Rom.8.4'      -> {sc:8, sv:1, ec:8, ev:4}
   *   'John.7.53-John.8.11'  -> a section crossing a chapter, said outright
   *   'Rom.8'                -> null: the section is about the whole chapter
   */
  function parseRef(ref) {
    var parts = String(ref || '').split('-');
    var a = parts[0].split('.');
    if (a.length < 3) return null;
    var sc = parseInt(a[1], 10), sv = parseInt(a[2], 10);
    if (parts.length === 1) return { sc: sc, sv: sv, ec: sc, ev: sv };
    var b = parts[1].split('.');
    return { sc: sc, sv: sv, ec: parseInt(b[1], 10), ev: parseInt(b[2], 10) };
  }

  /* OSIS -> HTML. The commentary uses a small closed set of elements; anything
   * unrecognised falls through to its children, so an element added later
   * degrades to readable prose instead of disappearing. */
  function children(node) {
    var out = '';
    for (var i = 0; i < node.childNodes.length; i++) out += render(node.childNodes[i]);
    return out;
  }

  function render(n) {
    if (n.nodeType === 3) return esc(n.nodeValue);
    if (n.nodeType !== 1) return '';
    var type = n.getAttribute('type');
    switch (n.localName) {
      case 'p':     return '<p>' + children(n) + '</p>';
      case 'title': return '<h3>' + children(n) + '</h3>';
      case 'hi':    return type === 'italic' ? '<em>' + children(n) + '</em>'
                                             : '<strong>' + children(n) + '</strong>';
      case 'list':  return type === 'x-ordered' ? '<ol>' + children(n) + '</ol>'
                                                : '<ul>' + children(n) + '</ul>';
      case 'item':  return '<li>' + children(n) + '</li>';
      case 'table': return '<table>' + children(n) + '</table>';
      case 'row':   return '<tr>' + children(n) + '</tr>';
      case 'cell':  return '<td>' + children(n) + '</td>';
      case 'div':
        if (type === 'x-blockquote') return '<blockquote>' + children(n) + '</blockquote>';
        if (type === 'x-indent') return '<blockquote class="indent">' + children(n) + '</blockquote>';
        return children(n);
      default:      return children(n);
    }
  }

  /* The whole book flattened to sections. A section records the chapter it was
   * written in as well as the passage it covers, because those differ for a
   * section spanning a chapter boundary. Returns {book, sections, chapters}
   * or null if the XML will not parse. */
  function parse(xml) {
    var doc = new DOMParser().parseFromString(xml, 'application/xml');
    if (doc.getElementsByTagName('parsererror').length) return null;

    var book = '', sections = [], chapters = [];
    var divs = doc.getElementsByTagNameNS('*', 'div');

    for (var i = 0; i < divs.length; i++) {
      var d = divs[i];
      if (d.getAttribute('type') === 'book') {
        for (var t = 0; t < d.children.length; t++) {
          if (d.children[t].localName === 'title') { book = d.children[t].textContent; break; }
        }
        continue;
      }
      if (d.getAttribute('type') !== 'chapter') continue;

      var chapter = parseInt(String(d.getAttribute('osisID')).split('.')[1], 10);
      chapters.push(chapter);

      for (var j = 0; j < d.children.length; j++) {
        var s = d.children[j];
        if (s.localName !== 'div' || s.getAttribute('type') !== 'section') continue;

        var title = '', body = '', seenTitle = false;
        for (var k = 0; k < s.children.length; k++) {
          var c = s.children[k];
          if (!seenTitle && c.localName === 'title') { title = c.textContent; seenTitle = true; }
          else body += render(c);
        }

        var rng = parseRef(s.getAttribute('annotateRef'));
        sections.push({
          chapter: chapter,
          sc: rng ? rng.sc : chapter, sv: rng ? rng.sv : 0,
          ec: rng ? rng.ec : chapter, ev: rng ? rng.ev : 0,
          onVerses: !!rng,
          label: s.getAttribute('n') || '',
          heading: title,
          title: title.replace(/^Verses?\s+[\d\-a-z]+:\s*/i, ''),
          html: body
        });
      }
    }
    return sections.length ? { book: book, sections: sections, chapters: chapters } : null;
  }

  function contains(s, chapter, verse) {
    var after = chapter > s.sc || (chapter === s.sc && verse >= s.sv);
    var before = chapter < s.ec || (chapter === s.ec && verse <= s.ev);
    return after && before;
  }

  /* '8:1-11', '8:12', or '7:53-8:11' when the section crosses a chapter. */
  function label(s) {
    if (!s.onVerses) return String(s.chapter);
    if (s.sc !== s.ec) return s.sc + ':' + s.sv + '-' + s.ec + ':' + s.ev;
    return s.sc + ':' + s.sv + (s.ev !== s.sv ? '-' + s.ev : '');
  }

  /* The anchor a report links to. Both reports build theirs by taking the part
   * of '12:13-18' after the colon, so the bare form is load-bearing: changing
   * it breaks every report link into that section. Dotted when the passage
   * reaches into another chapter, matching what the HTML ids used. */
  function sectionId(s) {
    if (!s.onVerses) return 'ch' + s.chapter;
    // A section splitting a verse carries the author's own label -- Matthew 13
    // runs '1-3a' then '3b-9' -- which annotateRef cannot express and which
    // the reports link to verbatim.
    if (s.label) return s.label;
    if (s.sc !== s.ec) return s.sc + '.' + s.sv + '-' + s.ec + '.' + s.ev;
    return s.sv + (s.ev !== s.sv ? '-' + s.ev : '');
  }

  function span(s) { return (s.ec - s.sc) * 1000 + (s.ev - s.sv); }

  /* The section to show for a verse.
   *
   * Sections can overlap: 2 Corinthians 6 closes with a section on 7:1 and
   * 2 Corinthians 7 opens with one. Prefer the section written in the chapter
   * being read, then the tighter of the two -- the more specific reading of a
   * verse is the more useful one. */
  function findSection(sections, ch, v) {
    var best = null;
    for (var i = 0; i < sections.length; i++) {
      var s = sections[i];
      if (!s.onVerses || !contains(s, ch, v)) continue;
      if (!best) { best = s; continue; }
      var mine = s.chapter === ch, theirs = best.chapter === ch;
      if (mine !== theirs) { if (mine) best = s; }
      else if (span(s) < span(best)) best = s;
    }
    return best;
  }

  /* Sections about the chapter as a whole -- "Context and Placement", the
   * closing summaries. 559 across the NT, and the HTML gave them no id, so
   * the pane could not see a single one. */
  function chapterNotes(sections, ch) {
    var out = [];
    for (var i = 0; i < sections.length; i++) {
      if (!sections[i].onVerses && sections[i].chapter === ch) out.push(sections[i]);
    }
    return out;
  }

  /* Everything written in one chapter, in the order it was written. */
  function ofChapter(sections, ch) {
    var out = [];
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].chapter === ch) out.push(sections[i]);
    }
    return out;
  }

  return {
    parse: parse, contains: contains, label: label, sectionId: sectionId,
    findSection: findSection, chapterNotes: chapterNotes, ofChapter: ofChapter,
    esc: esc
  };
})();
