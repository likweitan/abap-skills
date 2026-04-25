"""Loader for reference/styles.json — named style strings + port-pin helper."""
from __future__ import annotations

import json
from pathlib import Path

_REF = Path(__file__).resolve().parents[2] / "reference"

with open(_REF / "styles.json") as _f:
    _DATA = json.load(_f)

# Public dict of named styles (skips meta keys starting with '_')
STYLES: dict[str, str] = {k: v for k, v in _DATA.items() if not k.startswith("_") and isinstance(v, str)}

_PORT_PINS: dict[str, str] = _DATA["_port_pins"]
LEVELS: dict[str, dict] = _DATA["_levels"]


def port_pins(direction: str) -> str:
    """Return port-pin style fragment for direction in {right, left, down, up}."""
    if direction not in _PORT_PINS or direction.startswith("_"):
        raise ValueError(f"unknown direction: {direction!r}; choose from {sorted(k for k in _PORT_PINS if not k.startswith('_'))}")
    return _PORT_PINS[direction]


def level_size(level: str) -> int:
    return LEVELS[level]["icon"]


def level_label_pt(level: str) -> int:
    return LEVELS[level]["label_pt"]


def level_label_bold(level: str) -> bool:
    return LEVELS[level]["label_bold"]


# SAP logo base64 (cached)
_SAP_LOGO_PATH = _REF / "sap-logo.b64.txt"
SAP_LOGO_B64: str = _SAP_LOGO_PATH.read_text().strip() if _SAP_LOGO_PATH.exists() else ""


def sap_logo_style() -> str:
    """Style string for the SAP corner-logo image cell."""
    return (
        "shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;"
        "verticalAlign=top;aspect=fixed;imageAspect=0;"
        f"image=data:image/svg+xml,{SAP_LOGO_B64};strokeWidth=1.5;"
    )
