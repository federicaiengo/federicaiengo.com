"""Source-level Astro ID, fragment, accessibility and link-security checks.

Only literal HTML attributes are checked. This does not compile Astro, verify
rendered DOM, fetch URLs or make claims about indexing and accessibility.
"""
from __future__ import annotations

import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from audit_site_source import ROOT, route_for


class LiteralAttributes(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, dict(attrs)))

    handle_startendtag = handle_starttag


def parse_source(source: Path) -> LiteralAttributes:
    content = source.read_text(encoding="utf-8")
    # Astro frontmatter isn't rendered HTML. Avoid parsing JS comparisons as tags.
    if content.startswith("---\n"):
        _, marker, content = content.partition("\n---\n")
        if not marker:
            raise ValueError(f"Unclosed Astro frontmatter in {source}")
    parsed = LiteralAttributes()
    parsed.feed(content)
    parsed.close()
    return parsed


def literal(value: str | None) -> bool:
    return value is not None and "{" not in value and "}" not in value


def audit(root: Path = ROOT) -> dict:
    root = Path(root)
    pages_dir = root / "src/pages"
    pages = sorted(pages_dir.rglob("*.astro")) if pages_dir.is_dir() else []
    if not pages:
        raise ValueError("No Astro pages to audit")
    shared = root / "src/layouts/Base.astro"
    shared_tags = parse_source(shared).tags if shared.is_file() else []
    routes = {route_for(p.relative_to(pages_dir)): p for p in pages}
    tag_map = {route: shared_tags + parse_source(page).tags for route, page in
               routes.items()}
    ids_by_route: dict[str, set[str]] = {}
    errors: list[str] = []
    checked_fragments = checked_aria = checked_blank = excluded_dynamic = 0

    for route, tags in tag_map.items():
        ids = [attrs["id"] for _, attrs in tags if literal(attrs.get("id"))]
        counts = Counter(ids)
        ids_by_route[route] = set(ids)
        for item, count in counts.items():
            if count > 1:
                errors.append(f"{route}: duplicate literal id '{item}' ({count} times)")

    for route, tags in tag_map.items():
        for tag, attrs in tags:
            aria = attrs.get("aria-labelledby")
            if aria is not None:
                if literal(aria):
                    for reference in aria.split():
                        checked_aria += 1
                        if reference not in ids_by_route[route]:
                            errors.append(f"{route}: {tag} aria-labelledby unresolved '{reference}'")
                else:
                    excluded_dynamic += 1
            if tag != "a":
                continue
            target = attrs.get("target")
            if "target" in attrs and target is None:
                errors.append(f"{route}: a target attribute without a value")
            if target is not None and target.lower() == "_blank":
                checked_blank += 1
                rel = attrs.get("rel")
                if rel is None:
                    errors.append(f"{route}: target=_blank without noopener/noreferrer")
                elif literal(rel):
                    tokens = rel.lower().split()
                    if not ({"noopener", "noreferrer"} & set(tokens)):
                        errors.append(f"{route}: target=_blank without noopener/noreferrer")
                else:
                    excluded_dynamic += 1
            href = attrs.get("href")
            if href is None:
                continue
            if not literal(href):
                excluded_dynamic += 1
                continue
            url = urlsplit(href)
            if not url.fragment or url.scheme or url.netloc:
                continue
            if not href.startswith("/") and not href.startswith("#"):
                # Relative paths depend on the final generated route.
                excluded_dynamic += 1
                continue
            destination = url.path if url.path else route
            if destination not in ids_by_route:
                # The route validator in audit_site_source handles bad paths.
                continue
            checked_fragments += 1
            target = unquote(url.fragment)
            if target not in ids_by_route[destination]:
                errors.append(f"{route}: unresolved href fragment '#{target}' at {destination}")
    return {
        "pages": len(pages),
        "fragments_checked": checked_fragments,
        "aria_idrefs_checked": checked_aria,
        "blank_links_checked": checked_blank,
        "dynamic_or_unresolved_context_excluded": excluded_dynamic,
        "errors": errors,
        "scope": "Literal Astro source attributes only; shared Base layout assumed; no rendered DOM/build",
    }


def main() -> int:
    result = audit(ROOT)
    for error in result["errors"]:
        print("FAIL:", error)
    print("Source reference audit:", result)
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
