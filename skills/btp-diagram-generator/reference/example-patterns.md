# BTP Diagram Patterns (extracted from official examples)

Patterns and ready-to-copy style strings derived from
[btp-solution-diagrams/assets/editable-diagram-examples](https://github.com/SAP/btp-solution-diagrams/tree/main/assets/editable-diagram-examples)
(SAP Task Center L0/L1/L2, SAP Build Work Zone L2, SAP Build Process Automation L2,
Cloud Identity Services Authentication / Authorization / Identity Lifecycle L1/L2,
Private Link Service L2, SAP Start L2).

These are the conventions the official `.drawio` files actually use — follow
them rather than inventing your own layout.

---

## 1. Page setup

All examples use **A4 landscape**:

```xml
<mxGraphModel dx="2103" dy="1425" grid="0" gridSize="10" guides="1" tooltips="1"
  connect="1" arrows="1" fold="1" page="1" pageScale="1"
  pageWidth="1169" pageHeight="827" math="0" shadow="0">
```

- `pageWidth="1169" pageHeight="827"` for **all** levels (L0/L1/L2 — even dense L2).
  Multi-page or larger virtual canvas is achieved by placing groups across negative
  coordinates, not by changing the page size.
- L2 sets `background="none"`.
- `grid="0"` is common; gridSize=10 throughout.

## 2. Document title (top of every diagram)

A single text cell, floated above the BTP container:

```xml
<mxCell value="&lt;b style=&quot;color: rgb(0, 112, 242); font-family: arial; font-size: 16px;&quot;&gt;SAP Task Center - SAP BTP Solution Diagram&lt;/b&gt;"
  style="text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=12;fontColor=#1d2d3e;fontFamily=Helvetica;"
  vertex="1" parent="1">
  <mxGeometry x="-960" y="-733" width="365" height="31" as="geometry"/>
</mxCell>
```

Pattern: **`{Scenario name} - SAP BTP Solution Diagram`**, blue (`#0070F2`) bold Arial 16.

L2 additionally adds a description group right below containing one paragraph in
slate (`#475e75`) and a `Diagram Level: L2` label.

## 3. Outer BTP container (Subaccount / Multi-Cloud)

```text
rounded=1;whiteSpace=wrap;html=1;
strokeColor=#0070F2;fillColor=#EBF8FF;
arcSize=32;absoluteArcSize=1;
imageWidth=64;imageHeight=64;strokeWidth=1.5;
```

- Holds the SAP-logo tile in its top-left corner (a separate `shape=image` cell
  ~67×18 px positioned at the container's top-left, +18 px below the top edge).
- Two text labels stacked at top-left: bold **`Subaccount`** (Arial 16) and
  smaller **`Multi-Cloud`** (Arial 12).
- The fill `#EBF8FF` is the only place the light blue background appears.

## 4. Sub-containers (white cards inside the BTP container)

Used for Cloud Identity Services group, on-prem solutions, cloud solutions,
3rd party apps, etc.

```text
rounded=1;whiteSpace=wrap;html=1;
strokeColor=#0070F2;strokeWidth=1.5;
arcSize=16;absoluteArcSize=1;
fillColor=#FFFFFF;perimeterSpacing=0;
```

- `arcSize=16` for inner cards, `arcSize=14` for the external-system tiles.
- Always `strokeColor=#0070F2` (same blue as the outer container — never slate
  for cards inside the BTP boundary).

## 5. Service icons

Always rendered as base64-embedded SVGs. Standard style:

```text
shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;
verticalAlign=top;aspect=fixed;imageAspect=0;
image=data:image/svg+xml,<BASE64>;
strokeWidth=1.5;fontStyle=1;fontSize=14;fontColor=#1D2D3E;
points=[[0,0,0,0,0],[0,0.25,0,0,0],[0,0.5,0,0,0],[0,0.75,0,0,0],[0.25,0,0,0,0],[0.5,0,0,0,0],[0.75,0,0,0,0],[1,0,0,0,0],[1,0.25,0,0,0],[1,0.5,0,0,0],[1,0.75,0,0,0]];
```

Conventional sizes:

| Level | Icon size                                            | Label font                       |
| ----- | ---------------------------------------------------- | -------------------------------- |
| L0    | 50×50 or 52×52                                       | Arial 14 bold                    |
| L1    | 48×48 or 50×50                                       | Arial 14 bold                    |
| L2    | 32×32 (often) – icons get small to fit dense layouts | Arial 12 regular (`fontStyle=0`) |

The label is the cell's `value` (line break = `&#xa;`); it renders **below**
the icon thanks to `verticalLabelPosition=bottom`.

The 12-point `points=[…]` array gives connection anchors around the icon's
perimeter — keep it on every icon so connectors snap cleanly.

## 6. Grouping icons with their text label

Whenever an icon needs additional text (role, modality) below or beside it,
wrap both in a group:

```xml
<mxCell id="g1" value="" style="group" parent="1" vertex="1" connectable="0">
  <mxGeometry x="-960" y="-640" width="80" height="80" as="geometry"/>
</mxCell>
<mxCell id="g1-icon" value="" style="shape=image;...;image=data:image/svg+xml,..."
  parent="g1" vertex="1">
  <mxGeometry x="16.5" width="50" height="50" as="geometry"/>
</mxCell>
<mxCell id="g1-label" value="&lt;b style=&quot;font-size:14px;&quot;&gt;End User&lt;/b&gt;"
  style="text;html=1;align=center;verticalAlign=middle;..."
  parent="g1" vertex="1">
  <mxGeometry y="50" width="80" height="30" as="geometry"/>
</mxCell>
```

- Group cells must have `connectable="0"`; their children use coordinates
  _relative_ to the group's origin.
- This is also how external-system tiles (white card + small icon + bold label)
  are constructed.

## 7. External-system tile (e.g. "SAP S/4HANA On-Premise")

```xml
<mxCell style="group" connectable="0" .../>            <!-- 153×70 group -->
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#0070F2;
    strokeWidth=1.5;arcSize=14;fillColor=#FFFFFF;perimeterSpacing=0;"/>
  <mxCell style="shape=image;...;image=data:image/svg+xml,..."/>           <!-- ~28×28, top-left -->
  <mxCell value="&lt;b style=&quot;font-size:16px;&quot;&gt;SAP S/4HANA&lt;br&gt;On-Premise Solutions&lt;/b&gt;"
          style="text;html=1;align=left;..."/>                              <!-- right side -->
```

## 8. Connectors

| Purpose                                 | Style fragment                                                                                             |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Standard data flow** (L1/L2)          | `endArrow=blockThin;html=1;strokeColor=#475E75;rounded=0;endFill=1;endSize=4;startSize=4;strokeWidth=1.5;` |
| **Orthogonal flow**                     | prepend `edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;`                         |
| **Mutual trust** (bidirectional)        | `endArrow=blockThin;startArrow=blockThin;startFill=1;endFill=1;`                                           |
| **Optional / dashed**                   | `endArrow=none;dashed=1;strokeColor=#475E75;`                                                              |
| **Authentication (SAML/OIDC)**          | as standard, but `strokeColor=#188918`                                                                     |
| **Authorization / Provisioning (SCIM)** | as standard, but `strokeColor=#5D36FF` (indigo per Fiori Horizon)                                          |
| **Mutual trust** (pink)                 | as standard, but `strokeColor=#CC00DC` and `startArrow=blockThin;startFill=1`                              |
| **Async / indirect**                    | as standard, but `dashed=1` (per guideline: dashed = indirect/async)                                       |
| **Optional flow**                       | `endArrow=blockThin;dashed=1;dashPattern=1 4;strokeColor=#475E75;` (dotted per guideline)                  |
| **L0 connector** (neutral)              | `endArrow=none` or `endArrow=block;endFill=1` with no edge label                                           |
| **Firewall / Network boundary**         | `endArrow=none;strokeColor=#475E75;rounded=1;strokeWidth=3;jumpStyle=gap;` (thick grey, firewalls only)    |

A small `NETWORK` label (`#475E75`, Arial 12 bold uppercase) sits just to the left
of the network boundary line.

### Connector port pinning — avoid diagonal/angled lines

When an edge has `source`/`target` set but no explicit exit/entry ports, draw.io
auto-picks the closest anchor, which often produces diagonal lines. **Always pin
ports** on directional connectors:

```text
exitX=1;exitY=0.5;exitDx=0;exitDy=0;   ← leaves the right-center of the source
entryX=0;entryY=0.5;entryDx=0;entryDy=0;  ← enters the left-center of the target
```

Common values: `0` = left/top, `0.5` = center, `1` = right/bottom.

For vertical connectors (e.g. service → IdP below):

```text
exitX=0.5;exitY=1;exitDx=0;exitDy=0;
entryX=0.5;entryY=0;entryDx=0;entryDy=0;
```

**Remove manual waypoints** (`<Array as="points">` children with `<mxPoint>`) unless
a specific detour is intentional. Waypoints combined with auto-routing produce
extra bends. The default should be:

```xml
<mxGeometry relative="1" as="geometry">
  <Array as="points"/>
</mxGeometry>
```

## 10. Edge labels = "pill" tags, not inline text

Protocol/data labels are _separate vertex cells_ placed on top of (or near) the
edge — a small rounded rectangle, ~16 px tall:

```text
rounded=1;whiteSpace=wrap;html=1;arcSize=50;
strokeColor=#475E75;fillColor=#F5F6F7;     // generic data
fontColor=#475E75;
```

Variants matched to the connector color:

| Tag kind                   | strokeColor | fillColor | fontColor |
| -------------------------- | ----------- | --------- | --------- |
| Generic data (`Task Data`) | `#475E75`   | `#F5F6F7` | `#475E75` |
| REST/Token/SPI             | `#475E75`   | `default` | `#475E75` |
| SAML2/OIDC (auth, green)   | `#188918`   | `#F5FAE5` | `#266F3A` |
| SCIM (authz, indigo)       | `#5D36FF`   | `#F1ECFF` | `#5D36FF` |
| Trust (pink)               | `#CC00DC`   | `#FFF0FA` | `#CC00DC` |

Label HTML pattern: `<font color="..." size="1"><b>SAML2/OIDC</b></font>`.

## 11. Service icon SVG intrinsic size — fix blurry rendering

All icons in the SAP shape library have `width="16" height="16"` as their
intrinsic SVG dimensions, even in the size-M set. When draw.io renders a
`shape=image` cell at 48×48, it rasterizes the SVG at 16×16 first and then
upscales — producing a blurry icon.

**Fix:** After extracting the base64 SVG from the library, decode it, replace
`width="16" height="16"` on the root `<svg>` element with the target cell size
(e.g. `width="48" height="48"` for L1), then re-encode. The `viewBox` must
remain unchanged so the artwork scales correctly:

```python
import base64, re

def upscale_svg(b64: str, w: int, h: int) -> str:
    svg = base64.b64decode(b64).decode()
    svg = re.sub(r'(<svg\b[^>]*)\bwidth="[^"]*"', fr'\1width="{w}"', svg, count=1)
    svg = re.sub(r'(<svg\b[^>]*)\bheight="[^"]*"', fr'\1height="{h}"', svg, count=1)
    return base64.b64encode(svg.encode()).decode()
```

Apply this to every icon SVG when embedding it in the diagram. This is
unrelated to the cell geometry `width`/`height` — both must be set correctly.

## 12. Legend (L2 only)

A small card in the top-right area:

```text
rounded=0;whiteSpace=wrap;html=1;strokeColor=#eaecee;
strokeWidth=1.5;arcSize=16;fillColor=#FFFFFF;absoluteArcSize=1;
```

Contents:

- A bold **`Legend`** title (Arial 12).
- One row per flow type: a 16×16 colored `ellipse` swatch + 10 px Arial label
  (`Authentication`, `Provisioning`, `Access`).
- One row per arrow style: a short sample arrow + label
  (`Mutual Trust`, `Optional`).
- Inline service-icon swatch + `Service` label.

## 13. Negative coordinates are normal

Every example file places the diagram in negative coordinate space (e.g.
`x="-2200"`, `y="-1500"`). draw.io centers on the content, so this is fine
and matches the conventions used in the official files.

## 14. Per-level recipes

### L0 — business overview

- One outer BTP container.
- 3–6 service icons (50×50) directly inside, no sub-containers other than the
  Subaccount card.
- A few external systems on the right.
- Connectors: thin, neutral (`#475E75`), `endArrow=block` or `endArrow=none`,
  no protocol pills.
- No legend.

### L1 — technical

- Subaccount card + (optionally) one Cloud Identity Services sub-card.
- 4–10 services (48×48), labels Arial 14 bold.
- Directional connectors with `endArrow=blockThin`; a few colored
  authentication/provisioning flows.
- Optional `NETWORK` boundary line if on-prem systems are shown.
- Optional small pill labels for key protocols.

### L2 — detailed

- Title + description paragraph + `Diagram Level: L2`.
- Subaccount card with multiple inner sub-cards (Cloud Identity Services
  group, etc.).
- Icons shrunk to 32×32 to fit; labels Arial 12 regular.
- Pill tags on every meaningful edge (REST/Token, SAML2/OIDC, SCIM, Task Data).
- Network boundary line with `jumpStyle=gap`.
- Legend card in the top-right.

## 15. Validation against the examples

Before delivering an L1 or L2 diagram, sanity-check:

- [ ] The outer container is `#0070F2` stroke / `#EBF8FF` fill, `arcSize=32`.
- [ ] All inner cards use the same blue stroke (never slate).
- [ ] All icons are `shape=image;...;image=data:image/svg+xml,...` — no `mxgraph.sap.*` shapes.
- [ ] Icon `points=[…]` array is present (12 anchor points) on every service icon.
- [ ] All service icon SVGs have been upscaled to the target cell size (§11) — no 16×16 intrinsic dimensions.
- [ ] All directional connectors have `exitX`/`exitY`/`entryX`/`entryY` port pins and empty `<Array as="points"/>` (§8) — no diagonal lines.
- [ ] Edge labels are pill _vertices_, not inline `value=` text on the edge.
- [ ] Connector colors come from {`#475E75`, `#188918`, `#5D36FF`, `#CC00DC`} only (firewall reuses `#475E75` thick).
- [ ] L2 only: legend card present, network line present if on-prem is shown,
      description block present.

When in doubt, open one of the editable examples and copy the exact style
string for the element you need.
