import test from 'node:test';
import assert from 'node:assert/strict';
import { rewriteLink, sourceForGeneratedFile } from '../source-links.mjs';
test('repository Markdown resolves below GitHub Pages base, retaining fragment', () => {
  assert.equal(rewriteLink('ARCHITECTURE.md#进程与数据流', 'docs/INSTALL.md'), '/EinkOS/architecture/#进程与数据流');
  assert.equal(rewriteLink('OVERVIEW.md', 'docs/INSTALL.md'), '/EinkOS/');
});
test('source and image links preserve their distinct targets', () => {
  assert.equal(rewriteLink('../src/main.c', 'docs/FEATURES.md'), 'https://github.com/dshanpi/EinkOS/blob/main/src/main.c');
  assert.equal(rewriteLink('screenshots/01-home.png', 'docs/GALLERY.md'), '/EinkOS/screenshots/01-home.png');
});
test('shared static assets resolve to the site base', () => {
  assert.equal(rewriteLink('public/casts/demo.cast', 'docs/SITE.md'), '/EinkOS/casts/demo.cast');
  assert.equal(rewriteLink('assets/casts/flash.cast', 'docs/INSTALL.md'), '/EinkOS/casts/flash.cast');
});
test('anchors and external protocols are unchanged', () => {
  for (const url of ['#检查版本', 'https://github.com/dshanpi/EinkOS', 'mailto:docs@example.com']) {
    assert.equal(rewriteLink(url, 'docs/INSTALL.md'), url);
  }
});
test('Windows and POSIX generated paths map to the same canonical source', () => {
  assert.equal(sourceForGeneratedFile('G:\\codex\\einkos\\docs\\src\\content\\docs\\install.md'), 'docs/INSTALL.md');
  assert.equal(sourceForGeneratedFile('/repo/docs/src/content/docs/install.md'), 'docs/INSTALL.md');
});
test('traversal outside the repository is rejected', () => {
  assert.throws(() => rewriteLink('../../outside.md', 'docs/INSTALL.md'), /escapes repository/);
});
