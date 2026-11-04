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
        self.assertIn("58/58 Python unittest methods passed", page)
        self.assertIn("11/11 synthetic DuckDB QA scripts passed separately", page)
        self.assertIn("15 original SQL models", page)
        self.assertIn("21/21 Python unittest methods passed in GitHub Actions", page)
        self.assertIn("CLOSURE_REVIEW_2026-11-03.md", page)
        self.assertIn("fictional observations, not measured AI Search performance", page)

    def test_cyber_study_discloses_fictional_scope_and_test_limits(self):
        page = read("src/pages/projects/cyber-risk-assessment.astro")
        self.assertIn("No real supplier was assessed.", page)
        self.assertIn("58 Python unittest methods", page)
        self.assertIn("GitHub Actions regression run", page)
        self.assertIn("41565390636", page)
        self.assertIn("CLOSURE_REVIEW_2026-11-03.md", page)
        self.assertIn("NOT ASSESSED", page)
        self.assertIn("not an external audit", page)
        self.assertIn("not deployed IAM controls", page)
        self.assertIn("DECISION_BRIEF.md", page)

    def test_ecommerce_actions_are_proposals_not_proven_losses(self):
        page = read("src/pages/projects/ecommerce-technical-evidence.astro")
        self.assertIn("303 mismatches are a", page)
        self.assertIn("not 303 proven errors or financial losses", page)
        self.assertIn("not investigations performed with a client", page)
        self.assertIn("data-analytics-portfolio/blob/main/projects/ecommerce-revenue-operations-analytics", page)
        self.assertNotIn("data-analytics-portfolio/tree/main/projects/ecommerce-revenue-operations-analytics", page)
        self.assertIn("/local_validation/README.md", page)
        self.assertIn("11 Python validation scripts", page)
        self.assertIn("41926351713", page)
        self.assertIn("15 of the original 28 dbt models", page)
        self.assertIn("order and item-grain fact tables", page)
        self.assertIn("three monthly marts", page)
        self.assertIn("still counts that anomalous order as on time", page)
        self.assertIn("2/3 on time (66.67%)", page)
        self.assertIn("1/2 (50%)", page)
        self.assertIn("do not rerun the historical 249 dbt checks", page)
        self.assertIn("do not establish production safety", page)

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

    def test_hr_analysis_preserves_observational_and_excel_qa_limits(self):
        page = read("src/pages/projects/hr-attrition-evidence.astro")
        self.assertIn("not a live employer's workforce", page)
        self.assertIn("not proof that overtime itself caused anyone to leave", page)
        self.assertIn("Desktop Excel compatibility and verified XLSX regeneration remain pending", page)

    def test_ai_search_does_not_present_protocol_as_measured_results(self):
        hub = read("src/pages/ai-search.astro")
        study = read("src/pages/projects/ai-search-competitive-intelligence.astro")
        self.assertIn("not observed model outputs or measured results", hub)
        self.assertIn("not client work for any benchmarked company", study)
        self.assertIn("actual AI mentions, citations, recommendations or performance differences", study)
        self.assertIn("Passing software tests is not evidence of product visibility", study)

    def test_no_private_checkpoint_references_on_selected_public_pages(self):
        for relative in (
            "src/pages/index.astro",
            "src/pages/projects.astro",
            "src/pages/projects/cyber-risk-assessment.astro",
            "src/pages/projects/ecommerce-technical-evidence.astro",
            "src/pages/projects/insurance-claims-evidence.astro",
            "src/pages/projects/hr-attrition-evidence.astro",
            "src/pages/projects/ai-search-competitive-intelligence.astro",
            "src/pages/ai-search.astro",
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
