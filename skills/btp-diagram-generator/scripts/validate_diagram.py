#!/usr/bin/env python3
"""Validate a BTP-style .drawio file against the SKILL.md / example-patterns.md checklist.

Public Python API:
    from validate_diagram import validate_xml, validate_path
    errors, warnings = validate_xml(xml_string)
    errors, warnings = validate_path(Path("file.drawio"))

CLI:
    python3 validate_diagram.py <file.drawio>
    python3 validate_diagram.py <file.drawio> --strict-palette --strict-waypoints
    python3 validate_diagram.py <file.drawio> --quality showcase --json

Checks:
    - Root cells <mxCell id="0"/> and <mxCell id="1" parent="0"/> present
    - All cell IDs are unique
    - No cell has both vertex="1" and edge="1"
    - No style contains "shape=mxgraph.sap." (that stencil family does not exist)
    - Every edge has source and target referring to existing IDs
    - Every base64 SVG icon's intrinsic <svg> width/height matches its cell geometry (no blur)
    - Every directional edge with source+target has exitX/exitY/entryX/entryY port pins
    - Every edge has empty <Array as="points"/> (no manual waypoints)
    - All stroke/fill hex colors come from the SAP Fiori Horizon palette
    - Page size is 1169x827 (A4 landscape)

Exit codes:
    0  all checks passed (warnings allowed)
    1  one or more errors
    2  cannot read file
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

PALETTE = {
    "#0070F2", "#EBF8FF", "#475E75", "#F5F6F7", "#1D2D3E", "#556B82",
    "#188918", "#F5FAE5", "#266F3A",
    "#C35500", "#FFF8D6",
    "#D20A0A", "#FFEAF4",
    "#07838F", "#DAFDF5",
    "#5D36FF", "#F1ECFF",
    "#CC00DC", "#FFF0FA",
    "#FFFFFF", "#EAECEE", "#793802",
}
PALETTE_LC = {c.lower() for c in PALETTE}

HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")
SVG_DATA_RE = re.compile(r"image=data:image/svg\+xml,([A-Za-z0-9+/=]+)")
ROOT_SVG_RE = re.compile(r"<svg\b[^>]*>", re.DOTALL)
WH_ATTR_RE = re.compile(r'\b(width|height)="([^"]*)"')

CHECKS = {
    "input": "XML parses",
    "structure": "draw.io cell structure",
    "canvas": "A4 landscape canvas",
    "edge": "connector integrity",
    "icon": "icon rendering quality",
    "style": "SAP Fiori Horizon styling",
}


def _classify_diagnostic(message: str) -> tuple[str, dict[str, str], list[str]]:
    cell_match = re.search(r"\b(?:cell|edge) ([^:]+):", message)
    subject = {"cell": cell_match.group(1)} if cell_match else {}
    cases = (
        ("failed to parse XML", "input/xml-parse", ["repair the XML syntax and retry"]),
        ("missing root cell", "structure/root-cell", ["add the required draw.io root cells 0 and 1"]),
        ("duplicate cell id", "structure/duplicate-id", ["assign a unique id to every mxCell"]),
        ("both vertex='1' and edge='1'", "structure/cell-kind", ["make the cell either a vertex or an edge"]),
        ("page size is", "canvas/page-size", ["set pageWidth=1169 and pageHeight=827"]),
        ("non-existent shape=mxgraph.sap", "style/unsupported-stencil", ["use an embedded SAP SVG icon from icon-index.json"]),
        ("no source/target", "edge/endpoints-missing", ["connect the edge to source and target cells"]),
        ("references non-existent cell", "edge/endpoint-invalid", ["use ids of existing source and target cells"]),
        ("missing port pin", "edge/port-pins", ["add exitX, exitY, entryX, and entryY to the edge style"]),
        ("manual waypoint", "edge/manual-waypoints", ["remove waypoints or document the obstacle-forced detour"]),
        ("will render blurry", "icon/intrinsic-size", ["run upscale_svg_icons.py with the level's icon size"]),
        ("off-palette color", "style/off-palette", ["replace the color with a token from the SAP BTP palette"]),
    )
    for needle, code, fixes in cases:
        if needle in message:
            return code, subject, fixes
    return "structure/unknown", subject, ["inspect the reported subject and repair the local violation"]


def _build_receipt(path: Path, errors: list[str], warnings: list[str], quality: str) -> dict[str, object]:
    data = path.read_bytes()
    diagnostics = []
    for severity, messages in (("error", errors), ("warning", warnings)):
        for message in messages:
            code, subject, fixes = _classify_diagnostic(message)
            diagnostics.append({
                "code": code,
                "severity": severity,
                "message": message,
                "subject": subject,
                "supportedFixes": fixes,
            })

    error_groups = {
        entry["code"].split("/", 1)[0]
        for entry in diagnostics
        if entry["severity"] == "error"
    }
    warning_groups = {
        entry["code"].split("/", 1)[0]
        for entry in diagnostics
        if entry["severity"] == "warning"
    }
    checks = [
        {
            "id": check_id,
            "label": label,
            "ok": check_id not in error_groups,
            "status": (
                "fail" if check_id in error_groups
                else "warn" if check_id in warning_groups
                else "pass"
            ),
        }
        for check_id, label in CHECKS.items()
    ]
    return {
        "ok": not errors,
        "type": "btp-drawio",
        "quality": quality,
        "input": str(path.resolve()),
        "artifact": {
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
        },
        "validation": {
            "checksPassed": sum(check["ok"] for check in checks),
            "checkCount": len(checks),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "checks": checks,
        "diagnostics": diagnostics,
    }


def _parse_style(style: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in style.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
        elif part.strip():
            out[part.strip()] = ""
    return out


def _get_root_svg_dims(b64: str) -> tuple[int, int] | None:
    try:
        svg = base64.b64decode(b64).decode("utf-8")
    except Exception:
        return None
    m = ROOT_SVG_RE.search(svg)
    if not m:
        return None
    attrs = dict(WH_ATTR_RE.findall(m.group(0)))
    try:
        return int(float(attrs.get("width", "0"))), int(float(attrs.get("height", "0")))
    except ValueError:
        return None


def _validate_tree(root, strict_palette: bool, strict_waypoints: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    cells = root.findall(".//mxCell")
    ids = [c.get("id") for c in cells]
    id_set = set(ids)

    if "0" not in id_set:
        errors.append('missing root cell <mxCell id="0"/>')
    if "1" not in id_set:
        errors.append('missing root cell <mxCell id="1" parent="0"/>')

    seen: set[str] = set()
    for cid in ids:
        if cid in seen:
            errors.append(f"duplicate cell id: {cid}")
        seen.add(cid)

    model = root.find(".//mxGraphModel")
    if model is not None:
        pw = model.get("pageWidth")
        ph = model.get("pageHeight")
        if (pw, ph) != ("1169", "827"):
            warnings.append(f"page size is {pw}x{ph}, expected 1169x827 (A4 landscape)")

    for cell in cells:
        cid = cell.get("id", "?")
        is_vertex = cell.get("vertex") == "1"
        is_edge = cell.get("edge") == "1"
        style = cell.get("style", "") or ""

        if is_vertex and is_edge:
            errors.append(f"cell {cid}: has both vertex='1' and edge='1'")
        if "shape=mxgraph.sap." in style:
            errors.append(f"cell {cid}: uses non-existent shape=mxgraph.sap.* stencil")

        if is_edge:
            src = cell.get("source")
            tgt = cell.get("target")
            if src is None and tgt is None:
                warnings.append(f"edge {cid}: no source/target — uses raw coordinate points (prefer source+target with port pins)")
            else:
                if src is not None and src not in id_set:
                    errors.append(f"edge {cid}: source='{src}' references non-existent cell")
                if tgt is not None and tgt not in id_set:
                    errors.append(f"edge {cid}: target='{tgt}' references non-existent cell")
                if src and tgt:
                    sd = _parse_style(style)
                    missing = [k for k in ("exitX", "exitY", "entryX", "entryY") if k not in sd]
                    if missing:
                        warnings.append(f"edge {cid}: missing port pin attribute(s) {missing} — may auto-route diagonally")

            arr = cell.find(".//Array[@as='points']")
            if arr is not None and len(arr) > 0:
                msg = f"edge {cid}: has {len(arr)} manual waypoint(s) — prefer empty <Array as='points'/>"
                (errors if strict_waypoints else warnings).append(msg)

        if is_vertex:
            geom = cell.find("mxGeometry")
            if geom is not None:
                try:
                    cw = int(float(geom.get("width", "0")))
                    ch = int(float(geom.get("height", "0")))
                except ValueError:
                    cw = ch = 0
                m = SVG_DATA_RE.search(style)
                if m and cw and ch:
                    dims = _get_root_svg_dims(m.group(1))
                    if dims is not None:
                        sw, sh = dims
                        if sw and sh and (cw > sw * 1.5 or ch > sh * 1.5):
                            warnings.append(f"cell {cid}: SVG intrinsic {sw}x{sh} but cell {cw}x{ch} — will render blurry (run upscale_svg_icons.py)")

        for hexcol in HEX_RE.findall(style):
            if hexcol.lower() not in PALETTE_LC:
                msg = f"cell {cid}: off-palette color {hexcol}"
                (errors if strict_palette else warnings).append(msg)

    return errors, warnings


def validate_xml(xml: str, *, strict_palette: bool = False, strict_waypoints: bool = False) -> tuple[list[str], list[str]]:
    """Validate a draw.io XML string. Returns (errors, warnings)."""
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        return [f"failed to parse XML: {e}"], []
    return _validate_tree(root, strict_palette, strict_waypoints)


def validate_path(path: Path, *, strict_palette: bool = False, strict_waypoints: bool = False) -> tuple[list[str], list[str]]:
    return validate_xml(path.read_text(encoding="utf-8"), strict_palette=strict_palette, strict_waypoints=strict_waypoints)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("file", help="Path to .drawio file")
    parser.add_argument("--strict-palette", action="store_true", help="Treat off-palette colors as errors")
    parser.add_argument("--strict-waypoints", action="store_true", help="Treat manual waypoints as errors")
    parser.add_argument("--quality", choices=("standard", "showcase"), default="standard",
                        help="standard allows warnings; showcase requires zero warnings")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable validation receipt")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        print(f"error: {path} not found", file=sys.stderr)
        return 2

    errors, warnings = validate_path(path, strict_palette=args.strict_palette, strict_waypoints=args.strict_waypoints)

    if args.quality == "showcase" and warnings:
        errors.extend(warnings)
        warnings = []

    if args.json:
        print(json.dumps(_build_receipt(path, errors, warnings, args.quality), indent=2))
        return 0 if not errors else 1

    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"FAIL: {e}", file=sys.stderr)

    if not errors:
        print(f"OK: {path} passed validation ({len(warnings)} warning(s))")
        return 0
    print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
