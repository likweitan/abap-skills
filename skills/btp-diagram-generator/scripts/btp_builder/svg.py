"""SVG helpers — upscale intrinsic <svg width/height> to fix blurry icons."""
from __future__ import annotations

import base64
import re

ROOT_SVG_RE = re.compile(r"<svg\b[^>]*>", re.DOTALL)
WIDTH_ATTR_RE = re.compile(r'\bwidth="[^"]*"')
HEIGHT_ATTR_RE = re.compile(r'\bheight="[^"]*"')
SVG_DATA_RE = re.compile(r"image=data:image/svg\+xml,([A-Za-z0-9+/=]+)")


def upscale_svg_b64(b64: str, target_w: int, target_h: int) -> tuple[str, bool]:
    """Decode, patch root <svg width/height>, re-encode. Returns (new_b64, changed)."""
    if b64.startswith("data:image/svg+xml;base64,"):
        b64 = b64[len("data:image/svg+xml;base64,"):]
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
    svg = svg[: m.start()] + new_root + svg[m.end():]
    return base64.b64encode(svg.encode("utf-8")).decode("utf-8"), True


def patch_style_size(style: str, size: int) -> str:
    """Upscale every base64 SVG inside a style string to (size × size)."""
    def repl(m: re.Match) -> str:
        new_b64, _ = upscale_svg_b64(m.group(1), size, size)
        return f"image=data:image/svg+xml,{new_b64}"
    return SVG_DATA_RE.sub(repl, style)
