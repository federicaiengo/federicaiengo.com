"""Regression guards for public-facing business evidence and scope.

These are source-text checks, not rendered browser tests, customer outcomes,
security assessments, or measurement of job applications/SEO performance.
"""
from __future__ import annotations

import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGES = ROOT / "src" / "pages"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class BusinessEvidenceSourceTests(unittest.TestCase):
    def test_homepage_keeps_primary_position_and_secondary_link(self):
        content = read("src/pages/index.astro")
        self.assertIn("I make complex data simple.", content)
        self.assertIn('href="/projects/cyber-risk-assessment/"', content)
        self.assertIn("Data Engineering", content)

    def test_projects_are_business_readable_without_hiding_sources(self):
        page = read("src/pages/projects.astro")
        self.assertIn("DECISION_BRIEF.md", page)
        self.assertIn("Inspect synthetic source and tests", page)
        self.assertIn('href="/projects/cyber-risk-assessment/"', page)

    def test_cyber_study_discloses_fictional_scope_and_test_limits(self):
        page = read("src/pages/projects/cyber-risk-assessment.astro")
        self.assertIn("No real supplier was assessed.", page)
        self.assertIn("51 of 51 unittest methods", page)
        self.assertIn("not an external audit", page)
        self.assertIn("not deployed IAM controls", page)
        self.assertIn("DECISION_BRIEF.md", page)

    def test_ecommerce_actions_are_proposals_not_proven_losses(self):
        page = read("src/pages/projects/ecommerce-technical-evidence.astro")
        self.assertIn("303 mismatches are a", page)
        self.assertIn("not 303 proven errors or financial losses", page)
        self.assertIn("not investigations performed with a client", page)

    def test_insurance_evidence_discloses_historical_limits_and_uses_file_links(self):
        page = read("src/pages/projects/insurance-claims-evidence.astro")
        self.assertIn("raw source files are not currently distributed", page)
        self.assertIn("provenance and redistribution rights remain unverified", page)
        self.assertIn("11 locally passing tests on synthetic inputs", page)
        self.assertIn("not a fresh reproduction", page)
        self.assertIn("data-analytics-portfolio/blob/main/projects/insurance-claims-analytics", page)
        for path in (
            "/reports/BUSINESS_FINDINGS.md",
            "/reports/KPI_REPORT.md",
            "/reports/RAW_SOURCE_KPI_SPOT_CHECK_2026-10-09.md",
            "/python/verify_public_kpis.py",
            "/tests/test_verify_public_kpis.py",
            "/docs/business_rejected_findings.md",
        ):
            with self.subTest(file=path):
                self.assertIn(f"repoFiles + '{path}'", page)
        self.assertIn("repo + '/sql'", page)

    def test_no_private_checkpoint_references_on_selected_public_pages(self):
        for relative in (
            "src/pages/index.astro",
            "src/pages/projects.astro",
            "src/pages/projects/cyber-risk-assessment.astro",
            "src/pages/projects/ecommerce-technical-evidence.astro",
            "src/pages/projects/insurance-claims-evidence.astro",
        ):
            with self.subTest(page=relative):
                page = read(relative)
                self.assertNotIn("federica-private-checkpoints", page)
                self.assertNotIn("GossmereHQ", page)
                self.assertNotIn("/mnt/data/", page)

    def test_research_ledger_never_invents_outcome_measurements(self):
        with (ROOT / "data/visibility/change-ledger-v1.csv").open(
            encoding="utf-8", newline=""
        ) as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), len({r["change_id"] for r in rows}))
        expected = {f"SITE-{index:03d}" for index in range(10, 16)}
        relevant = {r["change_id"]: r for r in rows if r["change_id"] in expected}
        self.assertEqual(set(relevant), expected)
        for change_id, row in relevant.items():
            with self.subTest(change_id=change_id):
                self.assertEqual(row["measured_outcome"], "NOT_MEASURED")
                self.assertEqual(row["source_verified"], "yes")
                self.assertTrue(row["source_commit"])
                self.assertIn("github_actions_", row["deployed_version_verified"])
                self.assertTrue(row["limitations"])
                self.assertTrue(row["next_test"])


if __name__ == "__main__":
    unittest.main()
