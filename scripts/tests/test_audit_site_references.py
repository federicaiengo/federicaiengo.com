"""Fixture tests for literal source-reference and target security audit."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_site_references import audit


class ReferenceAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "src/pages").mkdir(parents=True)
        (self.root / "src/layouts").mkdir(parents=True)
        (self.root / "src/layouts/Base.astro").write_text(
            '<main id="main-content"><a href="#main-content">Skip</a></main>', encoding="utf-8")
        self.page("index.astro", '<a href="#main-content">Top</a>')

    def page(self, path: str, body: str):
        p = self.root / "src/pages" / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("---\nconst variable = a < b;\n---\n" + body, encoding="utf-8")

    def test_valid_layout_fragment_aria_and_blank(self):
        self.page("index.astro", '<h2 id="intro">Intro</h2><section aria-labelledby="intro">'
                  '<a href="#main-content">Skip</a><a href="#intro">Local</a>'
                  '<a href="https://example.com" target="_blank" rel="noopener noreferrer">External</a></section>')
        r = audit(self.root)
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["fragments_checked"], 3)
        self.assertEqual(r["aria_idrefs_checked"], 1)

    def test_duplicate_id_on_same_page(self):
        self.page("index.astro", '<div id="dup"></div><p id="dup"></p>')
        self.assertTrue(any("duplicate literal id" in e for e in audit(self.root)["errors"]))

    def test_duplicate_across_pages_is_not_error(self):
        self.page("index.astro", '<h2 id="same">A</h2>')
        self.page("other.astro", '<h2 id="same">B</h2>')
        self.assertEqual(audit(self.root)["errors"], [])

    def test_missing_local_fragment(self):
        self.page("index.astro", '<a href="#missing">Broken</a>')
        self.assertTrue(any("unresolved href fragment" in e for e in audit(self.root)["errors"]))

    def test_cross_page_fragment_resolution(self):
        self.page("index.astro", '<a href="/other/#found">Go</a>')
        self.page("other.astro", '<h2 id="found">There</h2>')
        self.assertEqual(audit(self.root)["errors"], [])
        self.page("other.astro", '<h2 id="different">Oops</h2>')
        self.assertTrue(any("unresolved href fragment" in e for e in audit(self.root)["errors"]))

    def test_unresolved_aria_idref(self):
        self.page("index.astro", '<section aria-labelledby="missing"></section>')
        self.assertTrue(any("aria-labelledby unresolved" in e for e in audit(self.root)["errors"]))

    def test_blank_without_rel(self):
        self.page("index.astro", '<a href="https://example.com" target="_blank">Offsite</a>')
        self.assertTrue(any("without noopener" in e for e in audit(self.root)["errors"]))

    def test_valueless_target_reports_error_without_crashing(self):
        self.page("index.astro", '<a target href="/">Malformed target</a>')
        self.assertTrue(any("target attribute without a value" in e
                            for e in audit(self.root)["errors"]))

    def test_dynamic_expressions_are_not_false_claims(self):
        self.page("index.astro", '<a href={source + "/x/#unknown"} target="_blank" '
                  'rel="noopener noreferrer">Dynamic</a><div id={variable}></div>')
        r = audit(self.root)
        self.assertEqual(r["errors"], [])
        self.assertGreater(r["dynamic_or_unresolved_context_excluded"], 0)

    def test_multi_token_aria_and_percent_encoded_fragment(self):
        self.page("index.astro", '<div id="first"></div><div id="with space"></div>'
                  '<section aria-labelledby="first second"></section>'
                  '<a href="#with%20space">Here</a>')
        r = audit(self.root)
        self.assertTrue(any("unresolved 'second'" in e for e in r["errors"]))
        self.assertFalse(any("href fragment" in e for e in r["errors"]))


if __name__ == "__main__":
    unittest.main()
