# federicaiengo.com

Independent professional portfolio and research hub for Federica Iengo.

**Focus:** Data Analytics, AI Search, SEO, AEO and GEO. Project work must demonstrate inspectable methods, reproducible source checks, measured evidence and the limits of what the data supports. The portfolio itself is an ongoing SEO/AEO/GEO case study—not a claim of achieved search visibility.

## Development

Astro source lives in `src/pages/`, with shared layout in `src/layouts/Base.astro`. Existing `public/robots.txt` and the Astro sitemap integration reference `https://federicaiengo.com`.

```bash
npm install
npm run build
```

**Important:** the current `package.json` specifies `latest` versions without a committed lockfile. Builds are therefore not yet dependency-reproducible, and the most recent commits have not been checked with an Astro build or rendered-browser audit. Dependency pinning/lockfile and actual build verification remain open QA work; avoid asserting a successful production build based on source alone.

### Source-only preflight (no npm or network required)

```bash
python scripts/audit_site_source.py
python scripts/audit_visual_assets.py
python -m unittest discover -s scripts/tests -v
```

The [visual asset audit](scripts/audit_visual_assets.py) also checks active FI raster favicon PNG/ICO paths, declared pixel sizes, a linked Apple touch icon and the PNG social preview when present. It rejects accidentally relinking the legacy flat SVG; checks use only Python's standard library. It does **not** prove visual fidelity, social crawler rendering, or browser caching.

The [audit source](scripts/audit_site_source.py) checks Astro file routes, literal internal links, basic page metadata, exactly one literal `h1`, image `alt` attributes, and domain/robots/sitemap configuration. It **does not** compile Astro, evaluate dynamic links, test external URLs, render a mobile layout, audit performance/accessibility in a browser or measure indexing. The new isolated fixture tests passed **9/9** against exact Git-blob-verified source files; a complete site checkout/source audit with the new Python checker has not yet been executed.

Existing manual GitHub Pages deployment is intentionally triggered only via `workflow_dispatch`. Writing commits **does not** publish the site. Obtain owner authorization before triggering a deployment and check both the workflow and the actual rendered result.

## Evidence-led projects

- [Projects and portfolio code](src/pages/projects.astro)
- [Research and methods](src/pages/research.astro)
- [AI Search measurement](src/pages/ai-search.astro)
- [Competitive benchmark: frozen 35-query protocol](data/ai-search/competitive-protocol-v1.md)
- [Website SEO/AEO/GEO measurement protocol](data/visibility/MEASUREMENT_PROTOCOL.md)
- [Website intervention ledger](data/visibility/change-ledger-v1.csv)

**Measurement state:** Google Search Console/GA4 have not been connected or configured; AI Search observation ledgers do not contain actual verified visibility results. Static source changes are not traffic improvements. The existing detailed FI eclipse identity remains subject to visual signoff; do not replace branding based only on placeholder assets.

## Guardrails

This public repository contains only the source code, research materials and project evidence intended for publication. Do not commit confidential notes, credentials or personal operational records. Check data provenance before publishing examples, and obtain authorization before external account actions or deployment.
