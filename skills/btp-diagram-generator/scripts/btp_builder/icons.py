"""Icon lookup with alias resolution + substring fuzzy fallback.

Public API:
    lookup_icon(query, level="L1") -> {"key": str, "style": str, "width": int, "height": int}
    list_icons() -> list[str]                # all canonical keys
    list_aliases() -> dict[str, str]         # alias → canonical key
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .svg import patch_style_size

_REF = Path(__file__).resolve().parents[2] / "reference"

with open(_REF / "icon-index.json") as _f:
    _RAW = json.load(_f)
_ICONS: dict[str, dict] = {k: v for k, v in _RAW.items() if not k.startswith("_")}

with open(_REF / "icon-aliases.json") as _f:
    _ALIASES: dict[str, str] = json.load(_f)["aliases"]

_FONT_STYLE_RE = re.compile(r"fontStyle=\d+;?")
_FONT_SIZE_RE = re.compile(r"fontSize=\d+;?")
_FONT_COLOR_RE = re.compile(r"fontColor=#?[0-9A-Fa-f]+;?")


class IconNotFound(KeyError):
    pass


def list_icons() -> list[str]:
    return sorted(_ICONS.keys())


def list_aliases() -> dict[str, str]:
    return dict(_ALIASES)


def _resolve_key(query: str) -> str:
    q = query.strip().lower()
    # 1. exact canonical key match (case-insensitive against canonical lower-set)
    for k in _ICONS:
        if k.lower() == q:
            return k
    # 2. exact alias match
    if q in _ALIASES:
        return _ALIASES[q]
    # 3. substring against aliases (e.g. "task center icon" → "task center")
    for alias, key in _ALIASES.items():
        if alias in q or q in alias:
            return key
    # 4. substring against canonical keys
    matches = [k for k in _ICONS if q in k.lower()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise IconNotFound(
            f"ambiguous icon query {query!r}: matched {len(matches)} canonical keys: {matches[:5]}{'...' if len(matches) > 5 else ''}"
        )
    raise IconNotFound(
        f"no icon found for {query!r}. Try one of: {sorted(_ALIASES.keys())[:10]}..."
    )


def lookup_icon(
    query: str,
    level: str = "L1",
    *,
    bold_label: bool | None = None,
    label_pt: int | None = None,
) -> dict:
    """Find an icon by short name, alias, or canonical key.

    Returns dict with keys: key, style, width, height. The style string is
    upscaled to match the level's cell size and has font attributes set.
    """
    from .styles import level_size, level_label_pt, level_label_bold

    key = _resolve_key(query)
    entry = _ICONS[key]

    size = level_size(level)
    pt = label_pt if label_pt is not None else level_label_pt(level)
    bold = bold_label if bold_label is not None else level_label_bold(level)

    style = entry["style"]
    style = patch_style_size(style, size)
    style = _FONT_STYLE_RE.sub("", style)
    style = _FONT_SIZE_RE.sub("", style)
    style = _FONT_COLOR_RE.sub("", style)
    style = style.rstrip(";") + ";"
    style += f"fontStyle={1 if bold else 0};fontSize={pt};fontColor=#1D2D3E;"

    return {"key": key, "style": style, "width": size, "height": size}
