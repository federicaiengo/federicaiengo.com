"""Fixture-based unit tests for source-only Astro integrity checks."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_site_source import audit, route_for


class SiteAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "src/pages").mkdir(parents=True)
        (self.root / "src/layouts").mkdir(parents=True)
        (self.root / "public").mkdir()
        (self.root / "astro.config.mjs").write_text(
            "export default { site: 'https://federicaiengo.com' }",
            encoding="utf-8",
        )
        (self.root / "public/CNAME").write_text("federicaiengo.com\n", encoding="utf-8")
        (self.root / "public/robots.txt").write_text(
            "User-agent: *\nAllow: /\nSitemap: https://federicaiengo.com/sitemap-index.xml\n",
            encoding="utf-8",
        )
        (self.root / "src/layouts/Base.astro").write_text(
            '<header><a href="/">Home</a></header>', encoding="utf-8",
        )
        self.page("index.astro", "Home", '<a href="/">Home</a>')

    def page(self, path: str, title: str, body: str, desc: str | None = None):
        output = self.root / "src/pages" / path
        output.parent.mkdir(parents=True, exist_ok=True)
        description = desc or "A detailed and inspectable professional research case study."
        output.write_text(
            f'<Base title="{title}" description="{description}">'
            f"<h1>{title}</h1>{body}</Base>",
            encoding="utf-8",
        )
        return output

    def test_healthy_small_site(self):
        self.page("projects.astro", "Projects", '<a href="/">Home</a>')
        result = audit(self.root)
        self.assertEqual(result["pages"], 2)
        self.assertEqual(result["literal_links_checked"], 3)
        self.assertEqual(result["errors"], [])

    def test_invalid_internal_url(self):
        self.page("index.astro", "Home", '<a href="/not-a-page/">Broken</a>')
        self.assertTrue(any("unresolved internal href" in x
                            for x in audit(self.root)["errors"]))

    def test_routes_match_trailing_slash_convention(self):
        self.assertEqual(route_for(Path("projects.astro")), "/projects/")
        self.assertEqual(route_for(Path("projects/index.astro")), "/projects/")
        self.assertEqual(route_for(Path("index.astro")), "/")
        self.assertEqual(route_for(Path("projects/ai-search.astro")),
                         "/projects/ai-search/")

    def test_duplicate_title_or_route_detected(self):
        self.page("projects.astro", "Home", "<p>Another page</p>")
        self.assertTrue(any("duplicate page title" in x
                            for x in audit(self.root)["errors"]))
        self.page("projects/index.astro", "Nested", "<p>Another project</p>")
        self.assertTrue(any("Duplicate public route" in x
                            for x in audit(self.root)["errors"]))

    def test_missing_h1_or_description_detected(self):
        self.page("index.astro", "Home", '<p>No h1?</p>', desc="short")
        page = self.root / "src/pages/index.astro"
        page.write_text(page.read_text().replace("<h1>Home</h1>", ""),
                        encoding="utf-8")
        errors = audit(self.root)["errors"]
        self.assertTrue(any("exactly one source h1" in x for x in errors))
        self.assertTrue(any("description missing/under" in x for x in errors))

    def test_missing_alt_detected(self):
        self.page("index.astro", "Home", '<img src="/cover.png">')
        self.assertTrue(any("missing alt" in x for x in audit(self.root)["errors"]))

    def test_expression_links_explicitly_excluded(self):
        self.page("index.astro", "Home",
                  '<a href={repo + "/not-checked/"}>Dynamic</a>')
        output = audit(self.root)
        self.assertEqual(output["errors"], [])
        self.assertEqual(output["dynamic_links_not_audited"], 1)

    def test_domain_or_sitemap_mismatch_detected(self):
        (self.root / "public/CNAME").write_text("wrong.example", encoding="utf-8")
        (self.root / "public/robots.txt").write_text("User-agent: *",
                                                     encoding="utf-8")
        errors = audit(self.root)["errors"]
        self.assertTrue(any("CNAME" in x for x in errors))
        self.assertTrue(any("sitemap" in x for x in errors))

    def test_literal_static_asset_is_valid(self):
        (self.root / "public/sheet.css").write_text("body{}", encoding="utf-8")
        self.page("index.astro", "Home", '<link href="/sheet.css" rel="stylesheet">')
        self.assertEqual(audit(self.root)["errors"], [])


if __name__ == "__main__":
    unittest.main()
