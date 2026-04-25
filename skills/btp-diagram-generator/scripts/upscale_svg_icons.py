#!/usr/bin/env python3
"""Upscale SVG intrinsic dimensions in BTP icon styles inside a .drawio file.

The SAP BTP shape library ships icons with width="16" height="16" on the root
<svg> element. draw.io rasterizes at the intrinsic size before scaling to the
cell geometry, producing blurry icons. This script decodes each base64 SVG in
shape=image styles, patches its root width/height to the target size (keeping
viewBox unchanged), and re-encodes.

Usage:
    python3 upscale_svg_icons.py <file.drawio> [--size 48]
    python3 upscale_svg_icons.py <file.drawio> --size 32 --in-place

Exit codes:
    0  success
    1  no .drawio file or parse error
"""
from __future__ import annotations

import argparse
import base64
import re
import sys
from pathlib import Path

SVG_DATA_RE = re.compile(r"image=data:image/svg\+xml,([A-Za-z0-9+/=]+)")
ROOT_SVG_RE = re.compile(r"<svg\b[^>]*>", re.DOTALL)
WIDTH_ATTR_RE = re.compile(r'\bwidth="[^"]*"')
HEIGHT_ATTR_RE = re.compile(r'\bheight="[^"]*"')


def upscale_svg_b64(b64: str, target_w: int, target_h: int) -> tuple[str, bool]:
    """Decode, patch root <svg> width/height, re-encode. Returns (new_b64, changed)."""
    try:
        svg = base64.b64decode(b64).decode("utf-8")
    except Exception:
        return b64, False

    m = ROOT_SVG_RE.search(svg)
    if not m:
        return b64, False

    root = m.group(0)
    new_root = WIDTH_ATTR_RE.sub(f'width="{target_w}"', root, count=1)
    new_root = HEIGHT_ATTR_RE.sub(f'height="{target_h}"', new_root, count=1)
    if new_root == root:
        return b64, False

    svg = svg[: m.start()] + new_root + svg[m.end() :]
    return base64.b64encode(svg.encode("utf-8")).decode("utf-8"), True


def patch_diagram(content: str, target_w: int, target_h: int) -> tuple[str, int]:
    """Patch every base64 SVG image in the diagram. Returns (new_content, count_changed)."""
    changed = 0

    def repl(match: re.Match) -> str:
        nonlocal changed
        new_b64, did_change = upscale_svg_b64(match.group(1), target_w, target_h)
        if did_change:
            changed += 1
        return f"image=data:image/svg+xml,{new_b64}"

    return SVG_DATA_RE.sub(repl, content), changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("file", help="Path to .drawio file")
    parser.add_argument("--size", type=int, default=48, help="Target SVG dimension (default: 48)")
    parser.add_argument("--in-place", action="store_true", help="Overwrite input file (default: write .drawio.patched)")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        print(f"error: {path} not found", file=sys.stderr)
        return 1

    content = path.read_text(encoding="utf-8")
    new_content, count = patch_diagram(content, args.size, args.size)

    out = path if args.in_place else path.with_suffix(path.suffix + ".patched")
    out.write_text(new_content, encoding="utf-8")
    print(f"Upscaled {count} SVG icon(s) to {args.size}x{args.size}. Wrote: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
