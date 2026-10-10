"""Read-only source preflight for the Astro portfolio website.

Checks traceable SEO/accessibility basics without network access, npm or
deploying. This is NOT an Astro build, rendered HTML audit or indexing test.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
HREF = re.compile(r"""\bhref\s*=\s*["'](/[^"'<>]*)["']""")
BASE_TITLE = re.compile(r'<Base\s+[^>]*\btitle="([^"]+)"', re.S)
BASE_DESC = re.compile(r'<Base\s+[^>]*\bdescription="([^"]+)"', re.S)
IMAGE_TAG = re.compile(r"<img\b[^>]*>", re.I | re.S)
H1_TAG = re.compile(r"<h1(?:\s|>)", re.I)


def route_for(relative: Path) -> str:
    parts = list(relative.with_suffix("").parts)
    if parts[-1] == "index":
        parts.pop()
    return "/" + "/".join(parts) + ("/" if parts else "")


def audit(root: Path = ROOT) -> dict:
    root = Path(root)
    pages_dir = root / "src/pages"
    if not pages_dir.is_dir():
        raise ValueError("Astro source pages directory missing")
    pages = sorted(p for p in pages_dir.rglob("*.astro") if p.is_file())
    if not pages:
        raise ValueError("No Astro pages to audit")
    routes: dict[str, Path] = {}
    errors: list[str] = []
    for page in pages:
        route = route_for(page.relative_to(pages_dir))
        if route in routes:
            errors.append(f"Duplicate public route {route}: {routes[route]} and {page}")
        routes[route] = page

    public = root / "public"
    assets = {
        "/" + p.relative_to(public).as_posix()
        for p in public.rglob("*") if p.is_file()
    } if public.is_dir() else set()
    targets = set(routes) | assets
    all_sources = pages + ([root / "src/layouts/Base.astro"] if
                           (root / "src/layouts/Base.astro").is_file() else [])
    static_links = dynamic_links = 0
    titles: dict[str, str] = {}

    for source in all_sources:
        content = source.read_text(encoding="utf-8")
        label = str(source.relative_to(root))
        if source in pages:
            titles_found = BASE_TITLE.findall(content)
            desc_found = BASE_DESC.findall(content)
            if len(titles_found) != 1 or not titles_found[0].strip():
                errors.append(f"{label}: expected one literal nonempty Base title")
            else:
                title = titles_found[0]
                if title in titles:
                    errors.append(f"{label}: duplicate page title shared with {titles[title]}")
                titles[title] = label
            if len(desc_found) != 1 or len(desc_found[0].strip()) < 40:
                errors.append(f"{label}: Base description missing/under 40 chars")
            if len(H1_TAG.findall(content)) != 1:
                errors.append(f"{label}: expected exactly one source h1")
        for match in HREF.finditer(content):
            literal = match.group(1)
            path = urlsplit(literal).path
            static_links += 1
            if path not in targets:
                errors.append(f"{label}: unresolved internal href {literal}")
        # Expressions need Astro compilation to resolve and are not audited.
        dynamic_links += len(re.findall(r"\bhref\s*=\s*\{", content))
        for tag in IMAGE_TAG.findall(content):
            if not re.search(r"\balt\s*=", tag):
                errors.append(f"{label}: image with missing alt attribute")

    config = root / "astro.config.mjs"
    robots = public / "robots.txt"
    cname = public / "CNAME"
    if not config.is_file() or "site: 'https://federicaiengo.com'" not in config.read_text(encoding="utf-8"):
        errors.append("Configured canonical Astro site URL missing or changed")
    if not robots.is_file() or "Sitemap: https://federicaiengo.com/sitemap-index.xml" not in robots.read_text(encoding="utf-8"):
        errors.append("Expected sitemap discovery instruction absent from robots.txt")
    if not cname.is_file() or cname.read_text(encoding="utf-8").strip() != "federicaiengo.com":
        errors.append("Public CNAME does not match expected domain")

    return {
        "pages": len(pages),
        "distinct_routes": len(routes),
        "literal_links_checked": static_links,
        "dynamic_links_not_audited": dynamic_links,
        "errors": errors,
        "scope": "Source-only; no build, rendered DOM, accessibility scanner, external URL checking, deployment, Search Console or GA4 data",
    }


def main() -> int:
    report = audit(ROOT)
    print(f"Pages={report['pages']}; literal links={report['literal_links_checked']}; "
          f"dynamic links excluded={report['dynamic_links_not_audited']}")
    for error in report["errors"]:
        print("FAIL:", error)
    print("Scope:", report["scope"])
    if report["errors"]:
        return 1
    print("PASS: source-only checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
