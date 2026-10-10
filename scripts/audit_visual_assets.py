"""Dependency-free, read-only check of the FI portfolio's favicon/social-card wiring.

Source inspection only: this does not build Astro, inspect the public website, or
prove visual quality. Exit nonzero for a missing/malformed referenced icon.
"""
from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_TAG = re.compile(r"<link\b[^>]*>", re.I | re.S)
ATTR = re.compile(r"([\w:-]+)\s*=\s*(['\"])(.*?)\2", re.S)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(file: Path) -> tuple[int, int]:
    data = file.read_bytes()
    if len(data) < 24 or not data.startswith(PNG_SIGNATURE) or data[12:16] != b"IHDR":
        raise ValueError("not a valid PNG header")
    width, height = struct.unpack(">II", data[16:24])
    if not 0 < width <= 16384 or not 0 < height <= 16384:
        raise ValueError("invalid PNG dimensions")
    return width, height


def ico_sizes(file: Path) -> set[tuple[int, int]]:
    data = file.read_bytes()
    if len(data) < 6:
        raise ValueError("ICO header is truncated")
    reserved, kind, count = struct.unpack_from("<HHH", data)
    if reserved or kind != 1 or count == 0 or len(data) < 6 + count * 16:
        raise ValueError("invalid ICO directory")
    sizes = set()
    for i in range(count):
        width, height, _, _, _, _, length, offset = struct.unpack_from(
            "<BBBBHHII", data, 6 + i * 16
        )
        if length == 0 or offset < 6 + count * 16 or offset + length > len(data):
            raise ValueError("invalid ICO image bounds")
        sizes.add((width or 256, height or 256))
    return sizes


def audit(root: Path = ROOT) -> dict:
    root = Path(root)
    layout = root / "src/layouts/Base.astro"
    errors, warnings, validated = [], [], []
    if not layout.is_file():
        return {"errors": ["Missing src/layouts/Base.astro"], "warnings": [], "validated": []}
    text = layout.read_text(encoding="utf-8")
    links = [{k.lower(): v for k, _, v in ATTR.findall(tag)} for tag in LINK_TAG.findall(text)]
    icons = [link for link in links if "icon" in link.get("rel", "").lower().split()]
    sizes_seen = set()
    for link in icons:
        href = link.get("href", "")
        if not href.startswith("/") or any(c in href for c in "?#"):
            errors.append(f"Icon href must be a literal root-relative path: {href!r}")
            continue
        file = root / "public" / href.lstrip("/")
        if not file.is_file():
            errors.append(f"Referenced icon missing: {href}")
            continue
        if file.suffix.lower() == ".svg":
            errors.append(f"Old/simplified SVG linked in icon metadata: {href}")
            continue
        try:
            if file.suffix.lower() == ".png":
                width, height = png_dimensions(file)
                declared = link.get("sizes", "")
                if declared and declared != f"{width}x{height}":
                    errors.append(f"Icon sizes mismatch: {href}, declared {declared}, actual {width}x{height}")
                if link.get("rel") == "icon":
                    sizes_seen.add((width, height))
            elif file.suffix.lower() == ".ico":
                found = ico_sizes(file)
                if (16, 16) not in found or (32, 32) not in found:
                    errors.append(f"ICO lacks 16x16/32x32 sizes: {href}")
            else:
                errors.append(f"Unsupported linked favicon type: {href}")
                continue
            validated.append(href)
        except (OSError, ValueError, struct.error) as exc:
            errors.append(f"Cannot read icon {href}: {exc}")
    for needed in ((16, 16), (32, 32)):
        if needed not in sizes_seen:
            errors.append(f"Missing an explicit rel=icon PNG of size {needed[0]}x{needed[1]}")
    if not any(link.get("rel") == "shortcut icon" for link in links):
        warnings.append("No explicit shortcut icon; browsers may choose a fallback")
    for link in links:
        if link.get("rel", "").lower() != "apple-touch-icon":
            continue
        file = root / "public" / link.get("href", "").lstrip("/")
        if not file.is_file():
            errors.append("Referenced Apple touch icon missing")
        else:
            try:
                if png_dimensions(file) != (180, 180):
                    errors.append("Apple touch icon must be 180x180 PNG")
                else:
                    validated.append(link["href"])
            except (OSError, ValueError) as exc:
                errors.append(f"Invalid Apple touch icon: {exc}")
    if "/social-preview.svg" in text:
        warnings.append("Open Graph/Twitter card still uses SVG; PNG preview compatibility not checked")
    if "/social-preview.png" in text:
        preview = root / "public/social-preview.png"
        if not preview.is_file():
            errors.append("Referenced social preview PNG missing")
        else:
            try:
                if png_dimensions(preview) != (1200, 630):
                    errors.append("Social preview must be 1200x630 PNG")
                else:
                    validated.append("/social-preview.png")
            except (OSError, ValueError) as exc:
                errors.append(f"Invalid social preview PNG: {exc}")
        if 'content="image/png"' not in text:
            warnings.append("Check og:image:type matches PNG content")
    return {"errors": errors, "warnings": warnings, "validated": validated}


def main() -> int:
    report = audit(ROOT)
    for line in report["errors"]:
        print("FAIL:", line)
    for line in report["warnings"]:
        print("PENDING:", line)
    print(f"Validated {len(report['validated'])} linked raster assets; source-only, NOT a build.")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
