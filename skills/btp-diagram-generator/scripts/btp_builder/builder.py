"""High-level SAP BTP solution-diagram builder.

Authoring API is intentionally tiny:

    BtpDiagram(level, title)            # instantiate
        .btp_container(...)             # the big light-blue box
        .subaccount(parent, label)      # white card inside
        .service(name, in_, ...)        # any BTP service icon
        .user(label, ...)               # End User icon + label
        .app_client(label, ...)         # generic mobile/desktop tile
        .external(label, kind, ...)     # right-side external system tile
        .idp(label, ...)                # 3rd-party IdP tile
        .connect(src, tgt, kind, dir)   # arrow with auto-pinned ports
        .save(path)                     # validates then writes XML

Positional helpers (right_of=, below=, left_of=, above=) auto-place the new node
relative to a previously created NodeRef, with a configurable gap (default 20).
"""
from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from html import escape as _html_escape
from pathlib import Path
from typing import Optional, Union

from .icons import lookup_icon
from .palette import (
    BTP_BORDER,
    BTP_FILL,
    NON_SAP_BORDER,
    NON_SAP_FILL,
    TEXT_TITLE,
    WHITE,
)
from .styles import STYLES, port_pins, sap_logo_style

# ──────────────────────────────────────────────────────────────────────────────


def _xml_escape(s: str) -> str:
    """Escape for XML attribute values; preserves draw.io HTML labels."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _label_html(text: str, *, bold: bool = True, pt: int = 14, color: str = TEXT_TITLE, font: str = "arial") -> str:
    """Wrap a plain string into the bold/sized HTML draw.io expects in value=."""
    text = _html_escape(text).replace("\n", "<br/>")
    weight = "<b>" if bold else ""
    weight_close = "</b>" if bold else ""
    inner = f'<font face="{font}" style="font-size: {pt}px; color: {color};">{weight}{text}{weight_close}</font>'
    return _xml_escape(inner)  # escape so it can sit in value="..."


@dataclass
class NodeRef:
    """Handle returned by every node-creation method. Carries geometry for placement."""
    id: str
    x: float
    y: float
    w: float
    h: float

    def right_edge(self) -> float:    return self.x + self.w
    def bottom_edge(self) -> float:   return self.y + self.h
    def center_x(self) -> float:      return self.x + self.w / 2
    def center_y(self) -> float:      return self.y + self.h / 2


@dataclass
class _Cell:
    id: str
    value: str
    style: str
    x: float
    y: float
    w: float
    h: float
    parent: str = "1"
    is_edge: bool = False
    source: str = ""
    target: str = ""

    def to_xml(self) -> str:
        attrs = f'id="{self.id}" value="{self.value}" style="{self.style}" parent="{self.parent}"'
        if self.is_edge:
            attrs += ' edge="1"'
            if self.source:
                attrs += f' source="{self.source}"'
            if self.target:
                attrs += f' target="{self.target}"'
            geo = (
                '<mxGeometry relative="1" as="geometry">'
                '<Array as="points"/></mxGeometry>'
            )
        else:
            attrs += ' vertex="1"'
            geo = f'<mxGeometry x="{self.x}" y="{self.y}" width="{self.w}" height="{self.h}" as="geometry"/>'
        return f"        <mxCell {attrs}>\n          {geo}\n        </mxCell>\n"


# ──────────────────────────────────────────────────────────────────────────────


class BtpDiagram:
    """Builder for one .drawio diagram. Instances are stateful; call save() at end."""

    DEFAULT_GAP = 24
    LABEL_BELOW_GAP = 18  # extra padding for the icon's auto-bottom label

    def __init__(self, level: str = "L1", title: str = "SAP BTP Solution Diagram") -> None:
        if level not in {"L0", "L1", "L2"}:
            raise ValueError("level must be one of L0, L1, L2")
        self.level = level
        self.title = title
        self._cells: list[_Cell] = []
        self._next_id = 0
        self._title_emitted = False

    # ── id helpers ────────────────────────────────────────────────────────────

    def _id(self, prefix: str = "n") -> str:
        self._next_id += 1
        return f"{prefix}-{self._next_id}"

    # ── placement helpers ─────────────────────────────────────────────────────

    def _resolve_position(
        self,
        x: Optional[float],
        y: Optional[float],
        right_of: Optional[NodeRef],
        left_of: Optional[NodeRef],
        below: Optional[NodeRef],
        above: Optional[NodeRef],
        in_: Optional[NodeRef],
        w: float,
        h: float,
        gap: float,
    ) -> tuple[float, float]:
        if right_of is not None:
            return right_of.right_edge() + gap, right_of.center_y() - h / 2
        if left_of is not None:
            return left_of.x - gap - w, left_of.center_y() - h / 2
        if below is not None:
            return below.center_x() - w / 2, below.bottom_edge() + gap + self.LABEL_BELOW_GAP
        if above is not None:
            return above.center_x() - w / 2, above.y - gap - self.LABEL_BELOW_GAP - h
        if in_ is not None and (x is None or y is None):
            # default: top-left padding inside the parent
            return in_.x + 24, in_.y + 24
        if x is None or y is None:
            raise ValueError("must specify x/y or one of right_of/left_of/below/above/in_")
        return float(x), float(y)

    def _emit_title(self) -> None:
        if self._title_emitted:
            return
        self._title_emitted = True
        val = (
            f'&lt;b style=&quot;color: {BTP_BORDER}; font-family: arial; '
            f'font-size: 16px;&quot;&gt;'
            f'{_html_escape(self.title)} - SAP BTP Solution Diagram&lt;/b&gt;'
        )
        self._cells.append(_Cell(
            id="title", value=val, style=STYLES["text_title"],
            x=0, y=-60, w=600, h=30,
        ))

    # ── containers ────────────────────────────────────────────────────────────

    def btp_container(
        self,
        *,
        x: float = 0, y: float = 0,
        w: float = 920, h: float = 510,
        sub_label: str = "Subaccount",
        env_label: str = "Multi-Cloud",
        with_logo: bool = True,
    ) -> NodeRef:
        """Outer light-blue BTP box with the SAP corner-logo + Subaccount/Env labels."""
        self._emit_title()
        cid = self._id("btp")
        self._cells.append(_Cell(
            id=cid, value="", style=STYLES["container_btp"],
            x=x, y=y, w=w, h=h,
        ))
        if with_logo:
            self._cells.append(_Cell(
                id=self._id("logo"), value="", style=sap_logo_style(),
                x=x + 20, y=y + 18, w=67, h=18,
            ))
        # Subaccount / env stacked labels
        if sub_label:
            self._cells.append(_Cell(
                id=self._id("sublbl"),
                value=_label_html(sub_label, bold=True, pt=16),
                style=STYLES["text_label"],
                x=x + 20, y=y + 40, w=140, h=28,
            ))
        if env_label:
            self._cells.append(_Cell(
                id=self._id("envlbl"),
                value=_label_html(env_label, bold=False, pt=12),
                style=STYLES["text_label"],
                x=x + 20, y=y + 64, w=120, h=24,
            ))
        return NodeRef(id=cid, x=x, y=y, w=w, h=h)

    def subaccount(
        self,
        *,
        parent: NodeRef,
        label: str = "Subaccount",
        x: Optional[float] = None,
        y: Optional[float] = None,
        w: float = 620,
        h: float = 195,
        pad: float = 24,
    ) -> NodeRef:
        """White inner card inside the BTP container."""
        if x is None: x = parent.x + pad
        if y is None: y = parent.y + 60
        cid = self._id("sub")
        self._cells.append(_Cell(
            id=cid, value="", style=STYLES["card_subaccount"],
            x=x, y=y, w=w, h=h,
        ))
        if label:
            self._cells.append(_Cell(
                id=self._id("subhdr"),
                value=_label_html(label, bold=True, pt=16),
                style=STYLES["text_label"],
                x=x + 16, y=y + 10, w=140, h=28,
            ))
        return NodeRef(id=cid, x=x, y=y, w=w, h=h)

    def inner_card(
        self,
        *,
        parent: NodeRef,
        label: str = "",
        x: Optional[float] = None,
        y: Optional[float] = None,
        w: float = 240,
        h: float = 140,
    ) -> NodeRef:
        """Generic white sub-card inside the BTP container (e.g. for grouping CIS services)."""
        if x is None: x = parent.x + 24
        if y is None: y = parent.y + 240
        cid = self._id("card")
        self._cells.append(_Cell(
            id=cid, value="", style=STYLES["card_inner"],
            x=x, y=y, w=w, h=h,
        ))
        if label:
            self._cells.append(_Cell(
                id=self._id("cardhdr"),
                value=_label_html(label, bold=True, pt=14),
                style=STYLES["text_label"],
                x=x + 12, y=y + 8, w=w - 24, h=24,
            ))
        return NodeRef(id=cid, x=x, y=y, w=w, h=h)

    # ── service / user nodes ──────────────────────────────────────────────────

    def service(
        self,
        name: str,
        *,
        in_: Optional[NodeRef] = None,
        right_of: Optional[NodeRef] = None,
        left_of: Optional[NodeRef] = None,
        below: Optional[NodeRef] = None,
        above: Optional[NodeRef] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        label: Optional[str] = None,
        gap: Optional[float] = None,
    ) -> NodeRef:
        """Add a BTP service icon. `name` is resolved via the alias system."""
        icon = lookup_icon(name, level=self.level)
        w, h = icon["width"], icon["height"]
        gap = gap if gap is not None else self.DEFAULT_GAP
        # Wider gap for service rows so labels don't collide
        if right_of is not None or left_of is not None:
            gap = max(gap, 100)
        x, y = self._resolve_position(x, y, right_of, left_of, below, above, in_, w, h, gap)
        cid = self._id("svc")
        self._cells.append(_Cell(
            id=cid,
            value=_xml_escape(label or _icon_pretty_name(icon["key"])),
            style=icon["style"],
            x=x, y=y, w=w, h=h,
        ))
        return NodeRef(id=cid, x=x, y=y, w=w, h=h)

    def user(
        self,
        label: str = "End User",
        *,
        right_of: Optional[NodeRef] = None,
        left_of: Optional[NodeRef] = None,
        below: Optional[NodeRef] = None,
        above: Optional[NodeRef] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        kind: str = "sap",
        gap: Optional[float] = None,
    ) -> NodeRef:
        key = {"sap": "end user", "non-sap": "non-sap user", "highlight": "highlight user"}[kind]
        icon = lookup_icon(key, level=self.level)
        w, h = icon["width"], icon["height"]
        gap = gap if gap is not None else self.DEFAULT_GAP
        if left_of is not None: gap = max(gap, 80)
        x, y = self._resolve_position(x, y, right_of, left_of, below, above, None, w, h, gap)
        cid = self._id("user")
        self._cells.append(_Cell(
            id=cid, value=_xml_escape(label),
            style=icon["style"], x=x, y=y, w=w, h=h,
        ))
        return NodeRef(id=cid, x=x, y=y, w=w, h=h)

    # ── tiles (app client / external / idp) ───────────────────────────────────

    def _tile(
        self,
        label: str,
        style_key: str,
        *,
        right_of: Optional[NodeRef] = None,
        left_of: Optional[NodeRef] = None,
        below: Optional[NodeRef] = None,
        above: Optional[NodeRef] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        w: float = 200,
        h: float = 70,
        gap: Optional[float] = None,
        label_pt: int = 14,
    ) -> NodeRef:
        gap = gap if gap is not None else self.DEFAULT_GAP
        x, y = self._resolve_position(x, y, right_of, left_of, below, above, None, w, h, gap)
        cid = self._id("tile")
        self._cells.append(_Cell(
            id=cid,
            value=_label_html(label, bold=True, pt=label_pt),
            style=STYLES[style_key],
            x=x, y=y, w=w, h=h,
        ))
        return NodeRef(id=cid, x=x, y=y, w=w, h=h)

    def app_client(self, label: str = "Application Clients\n(Mobile or Desktop)", **kwargs) -> NodeRef:
        kwargs.setdefault("w", 200)
        kwargs.setdefault("h", 70)
        kwargs.setdefault("label_pt", 13)
        return self._tile(label, "tile_app_client", **kwargs)

    def external(
        self,
        label: str,
        *,
        kind: str = "sap",
        **kwargs,
    ) -> NodeRef:
        """External system tile to the right of BTP. kind ∈ {'sap', 'non-sap'}."""
        style_key = "tile_external_sap" if kind == "sap" else "tile_external_non_sap"
        return self._tile(label, style_key, **kwargs)

    def idp(self, label: str = "3rd-party Identity Provider", **kwargs) -> NodeRef:
        kwargs.setdefault("w", 280)
        kwargs.setdefault("h", 60)
        kwargs.setdefault("label_pt", 13)
        return self._tile(label, "tile_idp", **kwargs)

    # ── connectors ────────────────────────────────────────────────────────────

    _ARROW_KIND = {
        "std":      "arrow_std",
        "dblhd":    "arrow_dblhd",
        "dashed":   "arrow_dashed",
        "optional": "arrow_optional",
        "auth":     "arrow_auth",
        "scim":     "arrow_scim",
        "trust":    "arrow_trust",
        "neutral":  "arrow_l0_neutral",
    }

    def connect(
        self,
        src: NodeRef,
        tgt: NodeRef,
        *,
        kind: str = "std",
        direction: Optional[str] = None,
    ) -> str:
        """Add an arrow. `direction` overrides auto-detection (right/left/up/down)."""
        if kind not in self._ARROW_KIND:
            raise ValueError(f"unknown arrow kind {kind!r}; choose from {list(self._ARROW_KIND)}")
        style = STYLES[self._ARROW_KIND[kind]]
        if direction is None:
            direction = self._auto_direction(src, tgt)
        style += port_pins(direction)
        cid = self._id("e")
        self._cells.append(_Cell(
            id=cid, value="", style=style,
            x=0, y=0, w=0, h=0,
            is_edge=True, source=src.id, target=tgt.id,
        ))
        return cid

    @staticmethod
    def _auto_direction(src: NodeRef, tgt: NodeRef) -> str:
        dx = tgt.center_x() - src.center_x()
        dy = tgt.center_y() - src.center_y()
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        return "down" if dy > 0 else "up"

    # ── output ────────────────────────────────────────────────────────────────

    def to_xml(self) -> str:
        cells_xml = "".join(c.to_xml() for c in self._cells)
        bg = ' background="none"' if self.level == "L2" else ""
        return f"""<mxfile host="btp-builder" version="1.0">
  <diagram name="BTP_Diagram" id="btp-{uuid.uuid4().hex[:12]}">
    <mxGraphModel dx="2103" dy="1425" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0"{bg}>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{cells_xml}      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""

    def save(self, path: Union[str, Path], *, validate: bool = True) -> Path:
        """Validate, then write to disk. Raises ValueError on validation errors."""
        xml = self.to_xml()
        if validate:
            # Local import to avoid circular dep at module load
            import sys as _sys
            from pathlib import Path as _P
            _scripts = _P(__file__).resolve().parents[1]
            if str(_scripts) not in _sys.path:
                _sys.path.insert(0, str(_scripts))
            from validate_diagram import validate_xml  # type: ignore

            errors, warnings = validate_xml(xml)
            if errors:
                raise ValueError(
                    "validation failed:\n  " + "\n  ".join(errors)
                )
            for w in warnings:
                print(f"WARN: {w}")
        out = Path(path)
        out.write_text(xml, encoding="utf-8")
        return out


# ──────────────────────────────────────────────────────────────────────────────


def _icon_pretty_name(key: str) -> str:
    """Convert canonical key (e.g. '31068-sap-build-work-zone_sd') to a human label."""
    s = key
    if s.startswith("generic:"):
        s = s.split(":", 1)[1]
    s = re.sub(r"^\d+-", "", s)
    s = re.sub(r"_sd$|_sd_$", "", s)
    s = s.replace("_", " ").replace("-", " ")
    # Title-case but uppercase well-known acronyms
    parts = s.split()
    fixed = []
    upper = {"sap", "btp", "hana", "fhir", "api", "ui5", "abap", "saas", "cap", "cf", "ai", "scim"}
    for p in parts:
        fixed.append(p.upper() if p.lower() in upper else p.capitalize())
    return " ".join(fixed)
