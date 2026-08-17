/* Reading the RCB's USFM in the browser.
 *
 * The Bible's twin of commentary/osis.js, and extracted for the same reason
 * that file exists: a parser kept in two copies is a parser that will disagree
 * with itself. This lived inline in docs/index.html until the collaborative
 * editor needed the same rendering for its preview pane -- a preview drawn by
 * an imitation of the viewer is a preview that quietly lies about what the
 * reader will see.
 *
 * The source of truth is usfm/nt/{BOOK}.usfm at the repo root, carried into
 * docs/rcb/data/{BOOK}.js by scripts/gen_rcb_data.py. Source outside docs/, a
 * thin wrapper inside it, the real markup parsed here.
 *
 * Nothing here touches the DOM of the host page. parse() returns the book
 * title alongside the HTML rather than writing it into the toolbar itself,
 * which is the one behavioural difference from the inline version.
 *
 * It does emit onclick/onmouseenter attributes naming showNote, showNoteHover
 * and hideNoteHover. Those are the host page's to define -- the viewer has
 * them, and any other page embedding this must supply them or footnote markers
 * will do nothing.
 */
/* Named Bible, not USFM: the data files declare `const USFM` for the raw text,
 * mirroring the commentary's `const OSIS`, and the two must not collide. */
var Bible = (function() {
  'use strict';

  function slugify(text) {
    return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
  }

  var noteCounter = 0;

  /* USFM markup within a verse: footnotes to clickable markers, \add to the
   * bracketed restorations the toggle hides, \tl to italics. */
  function renderInline(text) {
    text = text.replace(/\\u([0-9a-fA-F]{4})/g, function(_, hex) { return String.fromCharCode(parseInt(hex, 16)); });

    text = text.replace(/\\f \+ \\fr ([^ ]+) \\ft (.*?)\\f\*/g, function(match, ref, noteText) {
      noteCounter++;
      var letter = String.fromCharCode(96 + ((noteCounter - 1) % 26) + 1);
      var safeText = noteText.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;');
      safeText = safeText.replace(/\\tl\s+(.*?)\\tl\*/g, '<em>$1</em>');
      return '<span class="note-marker" data-note="' + safeText + '" onclick="showNote(event, this)" onmouseenter="showNoteHover(event, this)" onmouseleave="hideNoteHover()">' + letter + '</span>';
    });

    text = text.replace(/\\add\s+(.*?)\\add\*/g, '<span class="restoration">$1</span>');
    text = text.replace(/\\tl\s+(.*?)\\tl\*/g, '<em>$1</em>');

    return text;
  }

  /* A whole book of USFM -> { html, title }.
   *
   * The caller places the title; this used to set #toolbar-book directly,
   * which meant the renderer could only ever run on the one page that had a
   * toolbar. */
  function parse(usfm) {
    var lines = usfm.split('\n');
    var html = '';
    var bookTitle = '';
    var inIntro = false;
    var introHtml = '';
    var inParagraph = false;
    var currentChapter = 0;

    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].trim();
      if (!line) continue;

      if (line.startsWith('\\id ') || line.startsWith('\\toc')) continue;
      if (line.startsWith('\\h ')) {
        bookTitle = line.substring(3).trim();
        continue;
      }
      if (line.startsWith('\\mt1 ')) {
        html += '<div class="book-title">' + line.substring(5).trim() + '</div>';
        continue;
      }

      if (line.startsWith('\\imt ')) {
        inIntro = true;
        introHtml = '';
        continue;
      }
      if (line.startsWith('\\ip ')) {
        introHtml += '<p>' + renderInline(line.substring(4).trim()) + '</p>';
        continue;
      }

      if (line.startsWith('\\c ')) {
        if (inIntro) {
          html += '<div class="intro">' + introHtml + '</div>';
          inIntro = false;
        }
        if (inParagraph) {
          html += '</div>';
          inParagraph = false;
        }
        currentChapter = parseInt(line.substring(3).trim());
        noteCounter = 0;
        html += '<span class="chapter-num" id="ch' + currentChapter + '">' + currentChapter + '</span>';
        continue;
      }

      if (line.startsWith('\\s1 ')) {
        if (inParagraph) {
          html += '</div>';
          inParagraph = false;
        }
        var headingText = line.substring(4).trim();
        var id = 'ch' + currentChapter + '-' + slugify(headingText);
        html += '<div class="section-heading" id="' + id + '">' + renderInline(headingText) + '</div>';
        continue;
      }

      if (line === '\\p') {
        if (inParagraph) {
          html += '</div>';
        }
        html += '<div class="paragraph">';
        inParagraph = true;
        continue;
      }

      if (line.startsWith('\\v ')) {
        var rest = line.substring(3).trim();
        var spaceIdx = rest.indexOf(' ');
        var verseNum = rest.substring(0, spaceIdx);
        var verseText = rest.substring(spaceIdx + 1);
        html += '<span class="verse-num" id="v' + currentChapter + '-' + verseNum + '">' + verseNum + '</span>' + renderInline(verseText) + ' ';
        continue;
      }
    }

    if (inParagraph) html += '</div>';
    if (inIntro) html += '<div class="intro">' + introHtml + '</div>';

    return { html: html, title: bookTitle };
  }

  return { parse: parse, renderInline: renderInline, slugify: slugify };
})();
