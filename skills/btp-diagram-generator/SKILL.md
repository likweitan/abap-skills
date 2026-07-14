---
name: btp-diagram-generator
description: "Generate SAP BTP (Business Technology Platform) solution architecture diagrams as native draw.io (.drawio) files following the official SAP BTP Solution Diagram guidelines (Fiori Horizon design system) and open them via a configured draw.io MCP server. USE WHEN: user asks to create/draw/design/sketch a BTP diagram, BTP architecture, BTP landscape, BTP solution diagram, BTP reference architecture, SAP Business Technology Platform diagram, or wants to visualize SAP BTP services (CAP, Build, Integration Suite, SAC, AI Core, HANA Cloud, Cloud Foundry, Kyma, Workzone, etc.) and their interdependencies in draw.io / drawio / diagrams.net. DO NOT USE FOR: non-BTP architecture diagrams, generic flowcharts, sequence/UML diagrams, or diagrams that should remain in Mermaid/PlantUML."
---

# BTP Solution Diagram Generator

Produces a `.drawio` file in the workspace that conforms to the [SAP BTP Solution Diagram guidelines](https://sap.github.io/btp-solution-diagrams/) and opens it through whichever [draw.io MCP server](https://www.drawio.com/doc/faq/ai-drawio-generation) is configured.

## ⚡ Quick Path (use this first)

For the vast majority of diagrams, **do not hand-write XML**. Use the `btp_builder` Python package — it owns icon lookup, SAP palette, port pinning, label HTML, A4 sizing, SVG upscaling, and validation. A typical L1 diagram is ~20 lines.

```python
# scripts/examples/task_center_arch.py — runnable end-to-end
import sys
from pathlib import Path
# Add the skill's scripts/ dir to sys.path so `btp_builder` imports work
# regardless of where the skill is installed (repo, ~/.claude/skills/, etc.)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from btp_builder import BtpDiagram

d = BtpDiagram(level="L1", title="Task Center Reference Architecture")

btp = d.btp_container(x=260, y=80, w=560, h=440)
sub = d.subaccount(parent=btp, label="Subaccount",
                   x=btp.x + 24, y=btp.y + 110, w=520, h=170)

wz = d.service("work zone",   in_=sub, x=sub.x + 60, y=sub.y + 60)
tc = d.service("task center", right_of=wz)
ci = d.service("cloud identity", below=tc)

eu = d.user("End User", x=60, y=btp.y + 100)
ac = d.app_client("Application Clients\n(Mobile or Desktop)", below=eu)

s4    = d.external("SAP S/4HANA\nOn-Premise Solutions",
                   x=btp.right_edge() + 40, y=btp.y + 70, kind="sap")
third = d.external("3rd Party\nApplications", below=s4, kind="non-sap")
cloud = d.external("SAP Cloud\nApplications", below=third, kind="sap")
idp   = d.idp("3rd-party Identity Provider",
              x=ci.center_x() - 140, y=btp.bottom_edge() + 60)

d.connect(eu, ac, direction="down")
d.connect(ac, wz, direction="right")
d.connect(wz, tc, kind="dblhd")
d.connect(tc, ci, kind="dblhd", direction="down")
d.connect(tc, s4); d.connect(tc, third); d.connect(tc, cloud)
d.connect(idp, ci, kind="dashed", direction="up")

d.save("btp-task-center-architecture.drawio")  # validates → raises on errors
```

Run via `uv run python <script>.py` from the repository root. `save()` validates first and raises `ValueError` with the full error list if anything is off; warnings are printed.

### Quick-Path API surface

| Call                                                        | Returns   | Notes                                                                                                                                                       |
| ----------------------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `BtpDiagram(level, title)`                                  | builder   | level ∈ `L0`/`L1`/`L2`. Drives icon size + label weight.                                                                                                    |
| `.btp_container(x,y,w,h, sub_label, env_label, with_logo)`  | `NodeRef` | Light-blue outer frame + SAP corner logo + Subaccount/Multi-Cloud labels.                                                                                   |
| `.subaccount(parent, label, ...)`                           | `NodeRef` | White card inside the BTP container.                                                                                                                        |
| `.inner_card(parent, label, ...)`                           | `NodeRef` | Generic white sub-card (e.g. CIS service group).                                                                                                            |
| `.service(name, in_=, right_of=, left_of=, below=, above=)` | `NodeRef` | `name` is fuzzy-matched via [reference/icon-aliases.json](reference/icon-aliases.json) (e.g. `"task center"`, `"cpi"`, `"hana cloud"`).                     |
| `.user(label, kind="sap")`                                  | `NodeRef` | kind ∈ `sap` / `non-sap` / `highlight`.                                                                                                                     |
| `.app_client(label, ...)`                                   | `NodeRef` | Generic mobile/desktop tile.                                                                                                                                |
| `.external(label, kind="sap"/"non-sap", ...)`               | `NodeRef` | Right-side external system tile.                                                                                                                            |
| `.idp(label, ...)`                                          | `NodeRef` | 3rd-party Identity Provider tile.                                                                                                                           |
| `.connect(src, tgt, kind, direction)`                       | edge id   | `kind` ∈ `std`/`dblhd`/`dashed`/`optional`/`auth`/`scim`/`trust`/`neutral`. `direction` auto-pins ports — override with `"right"`/`"left"`/`"up"`/`"down"`. |
| `.save(path, validate=True)`                                | `Path`    | Writes XML. Validates inline (raises on errors).                                                                                                            |

Positional kwargs (`right_of`, `left_of`, `below`, `above`, `in_`) auto-place nodes — only set explicit `x,y` for the first anchor in each row/column.

### Icon name discovery

```python
from btp_builder import list_aliases, list_icons, lookup_icon
print(list(list_aliases())[:30])     # short names → canonical keys
print(lookup_icon("integration suite", "L1")["key"])
```

If `lookup_icon` raises `IconNotFound`, fall back to a styled tile (`external(label, kind="sap")`) and call it out in the final response.

### Open the diagram

```sh
uv run python skills/btp-diagram-generator/scripts/open_diagram.py btp-task-center-architecture.drawio
```

Falls back to printing a `https://app.diagrams.net/?…#create=...` URL if no system opener is found. If a draw.io MCP tool is available in the runtime, prefer that — only call MCP tools that actually appear in the tool list.

---

## Manual XML path (advanced / niche cases only)

Use this only when the Quick Path doesn't cover what you need (e.g. exotic legend variants, custom flow-protocol pills, novel layouts not yet supported by the builder). Everything below documents the underlying XML primitives the builder generates for you.

## When to use

Trigger on requests like:

- "Draw a BTP architecture for …"
- "Generate a BTP solution diagram showing CAP + HANA Cloud + Build Workzone"
- "Create a draw.io of our SAP BTP integration landscape"
- "L0 / L1 / L2 BTP diagram for <use case>"

If the request is a generic flowchart, sequence diagram, or non-SAP architecture, do not use this skill — generate Mermaid or use a plain draw.io workflow instead.

## Inputs to gather (ask once, concisely)

Before generating, confirm what is missing. Default to L1 if unspecified.

| Input                    | Default              | Notes                                                                                                                                                                  |
| ------------------------ | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Audience level           | L1                   | L0 = business overview (no legend, neutral connectors); L1 = technical (services + main flows); L2 = detailed (data flows, protocols, components)                      |
| BTP services / SaaS apps | (must ask)           | e.g. CAP, Build Code, Integration Suite (CPI/Event Mesh/API Mgmt), HANA Cloud, SAC, AI Core, Joule, Build Workzone, Identity Authentication, Destination, Connectivity |
| Non-BTP systems          | (optional)           | e.g. S/4HANA Cloud, SuccessFactors, Ariba, third-party SaaS, on-prem systems, end users                                                                                |
| Environment / runtime    | Cloud Foundry        | Cloud Foundry, Kyma, ABAP Environment                                                                                                                                  |
| Region / multi-region?   | single               | Affects grouping containers                                                                                                                                            |
| Primary flows            | (must ask)           | What connects to what, direction, purpose                                                                                                                              |
| Output filename          | `btp-diagram.drawio` | Saved to workspace root unless user specifies                                                                                                                          |

If the user gives a one-line prompt with enough services and a clear flow, proceed without asking — surface assumptions in the final response.

## Workflow

### 1. Map requirements to BTP icons

> **There is no `mxgraph.sap.*` stencil family.** SAP BTP icons in draw.io are SVGs embedded as base64 inside `shape=image;image=data:image/svg+xml,<base64>;…` style strings, distributed via the [SAP draw.io shape library XML files](https://github.com/SAP/btp-solution-diagrams/tree/main/assets/shape-libraries-and-editable-presets/draw.io). Generating `shape=mxgraph.sap.foo` produces an empty square in the canvas — you have seen this fail.

For every requested service, obtain its real `style` string by looking it up in [reference/icon-index.json](reference/icon-index.json):

1. **Preferred:** Load [reference/icon-index.json](reference/icon-index.json) (~660 KB, 100 icons). It maps each icon title (e.g. `31068-sap-build-work-zone_sd`) to its `style` string and library cell `width`/`height`. Match by substring against the requested service name.
2. **Source XML libraries** (if you need a non-default size or a metadata field the index doesn't carry) live in [reference/libraries/](reference/libraries/) — one size-M `mxlibrary` per icon set (foundational, integration suite, app-dev, AI, data-analytics, BTP-SaaS, all-in-one).
3. **Style donors:** for compound patterns (subaccount cards, NETWORK boundaries, pill labels, legend cards), consult the curated [reference/examples/](reference/examples/) — 11 official editable diagrams (Task Center L0/L1/L2, Build Work Zone L2, Process Automation L2, Cloud Identity Services L1/L2, Private Link L2, SAP Start L2). Open any of them and copy the exact style string.
4. If a service is genuinely missing from the library, use the styled fallback tile (see §3 below) and **list it in the final response** so the user can replace it.

Default icon geometry by audience level (matches the official examples — see [reference/example-patterns.md §5](reference/example-patterns.md)):

> **SVG intrinsic size warning:** Every icon in the SAP shape library has `width="16" height="16"` on its root `<svg>` element, even in the size-M set. draw.io rasterizes at that intrinsic size then upscales, producing a blurry icon. After extracting a base64 SVG, patch the root `<svg width>` and `<svg height>` to match the target cell size (e.g. 48 for L1) before re-encoding. Keep `viewBox` unchanged. See [reference/example-patterns.md §11](reference/example-patterns.md) for the Python helper.

| Level | Icon size | Label            |
| ----- | --------- | ---------------- |
| L0    | 50×50     | Arial 14 bold    |
| L1    | 48×48     | Arial 14 bold    |
| L2    | 32×32     | Arial 12 regular |

The label goes in the cell's `value=` attribute and renders below the icon (the library style already sets `verticalLabelPosition=bottom`). Always keep the `points=[[0,0,0,0,0],…]` 12-anchor array from the library style so connectors snap cleanly.

### 2. Apply the SAP Fiori Horizon palette

Always use these colors only (never pick arbitrary fills). Source: SAP BTP Solution Diagram guideline — _Foundation (Atoms)_ and _Areas_:

| Token                      | Hex                      | Use                                                           |
| -------------------------- | ------------------------ | ------------------------------------------------------------- |
| SAP/BTP border (Primary)   | `#0070F2`                | BTP container stroke, accent fills, sub-card stroke           |
| SAP/BTP fill               | `#EBF8FF`                | BTP container background                                      |
| Non-SAP border             | `#475E75`                | Non-SAP / external area strokes, generic data-flow connectors |
| Non-SAP fill / Subtle bg   | `#F5F6F7`                | Non-SAP areas, page background, generic pill fill             |
| Title text                 | `#1D2D3E`                | Headings, primary labels                                      |
| Secondary text             | `#556B82`                | Sub-labels, descriptions, footnotes                           |
| Positive (Auth, green)     | `#188918` / bg `#F5FAE5` | Authentication flows (SAML, OIDC) — per guideline             |
| Critical (Warning, orange) | `#C35500` / bg `#FFF8D6` | Warnings                                                      |
| Negative (Error, red)      | `#D20A0A` / bg `#FFEAF4` | Errors                                                        |
| Teal accent                | `#07838F` / bg `#DAFDF5` | Highlight areas                                               |
| Indigo (Authorization)     | `#5D36FF` / bg `#F1ECFF` | Authorization / provisioning (SCIM) flows — per guideline     |
| Pink (Trust)               | `#CC00DC` / bg `#FFF0FA` | Trust flows (mutual trust, federation) — per guideline        |

Font: `Arial` (or `Arial Black` for headings), size 12 for body labels, 14 for service labels, 16 for group titles.

### 3. Apply the atomic structure

Per the SAP atomic design system (Atoms → Molecules → Organisms). The exact style strings, sizes and HTML label patterns to copy live in [reference/example-patterns.md](reference/example-patterns.md) — match those rather than inventing variants.

- **Document title** (every diagram): a floating text cell above the BTP container, blue `#0070F2` bold Arial 16, format `"{Scenario} - SAP BTP Solution Diagram"`.
- **Outer container** (Subaccount / Multi-Cloud): `rounded=1;strokeColor=#0070F2;fillColor=#EBF8FF;arcSize=32;absoluteArcSize=1;strokeWidth=1.5;`. Carries the SAP-logo image tile in the top-left and two stacked labels: bold `Subaccount` (Arial 16) + smaller `Multi-Cloud` (Arial 12).
- **Sub-containers** (white cards inside the BTP boundary — e.g. Cloud Identity Services group): same `#0070F2` stroke, `#FFFFFF` fill, `arcSize=16`. **Always blue stroke, never slate**, when the card sits inside the BTP container. Per the guideline _Areas / Nesting_: alternate fill vs. no-fill between parent and child to keep visual contrast (BTP container has fill `#EBF8FF`, so inner cards use white).
- **Service nodes**: BTP icons (§1) wrapped in a `style="group" connectable="0"` cell whenever they need a separate text label or are co-positioned with another shape. Children use coordinates relative to the group origin.
- **External-system tiles** (e.g. `SAP S/4HANA On-Premise`): a group of (white card `arcSize=14` + ~28×28 icon top-left + bold `font-size:16px` label on the right). Sit outside the BTP container.
- **Users / actors**: a `group` containing the user SVG image and a centered `End User` text label below.
- **Connectors** — copy the right variant from the example patterns reference. Per the guideline _Connectors_ section, line _style_ encodes flow nature and line _color_ encodes flow semantic:
  - **Line style:** solid = direct synchronous request/response · `dashed=1` = indirect / asynchronous · `dashed=1;dashPattern=1 4;` (dotted) = optional · `strokeWidth=3` = **firewalls / network barriers only**.
  - **Semantic color:** Authentication = green `#188918` · Authorization / Provisioning (SCIM) = indigo `#5D36FF` · Mutual trust / federation = pink `#CC00DC` · Generic data = slate `#475E75`.
  - Standard data flow: `endArrow=blockThin;strokeColor=#475E75;endFill=1;endSize=4;startSize=4;strokeWidth=1.5;`
  - Orthogonal: prefix with `edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;`
  - Authentication (SAML/OIDC): same shape, `strokeColor=#188918`
  - Authorization / Provisioning (SCIM): same shape, `strokeColor=#5D36FF`
  - Mutual trust: add `startArrow=blockThin;startFill=1` and `strokeColor=#CC00DC`
  - Async / indirect: add `dashed=1`
  - Optional: add `dashed=1;dashPattern=1 4;` (dotted)
  - Network / firewall boundary line: thick grey vertical separator `strokeColor=#475E75;strokeWidth=3;jumpStyle=gap;` with a small uppercase `NETWORK` label (`#475E75`) beside it. **Reserve `strokeWidth=3` for firewalls/network barriers only** — do not use it for normal data flows.
  - **Always pin exit/entry ports** to avoid diagonal auto-routing: add `exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;` (adjust X/Y for the direction). For vertical connectors use `exitY=1` / `entryY=0`. **Remove manual `<mxPoint>` waypoints** unless a deliberate detour is needed — leave `<Array as="points"/>` empty. See [reference/example-patterns.md §8](reference/example-patterns.md) for the full port-pinning reference.
- **Edge labels** are _separate vertex pills_, not inline edge text — small rounded rectangles `arcSize=50`, ~16 px tall, color-matched to the connector (generic `#475E75`/`#F5F6F7`, auth `#188918`/`#F5FAE5`, authz/SCIM `#5D36FF`/`#F1ECFF`, trust `#CC00DC`/`#FFF0FA`).
- **L0**: no legend, no protocol pills, neutral `endArrow=block` or `endArrow=none` connectors.
- **L1**: directional `endArrow=blockThin` connectors, optionally a few colored auth/provisioning flows and pill labels.
- **L2**: add a description block + `Diagram Level: L2` under the title, pill tags on every meaningful edge, and a **legend card** in the top-right (white card, `strokeColor=#eaecee`, with colored 16×16 ellipse swatches for each flow type and a sample arrow per arrow style).

### 4. Generate the draw.io XML

Follow the [draw.io AI generation rules](https://www.drawio.com/doc/faq/ai-drawio-generation):

- Use **uncompressed** XML, full `<mxfile>` wrapper (so file-level vars are usable).
- Always include `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>`.
- Vertices: `vertex="1"`. Edges: `edge="1"` with `source`/`target`. Mutually exclusive.
- Unique IDs across the diagram.
- Coordinates: top-left `(0,0)`, x→right, y→down. Children inside a group use coordinates _relative_ to the group.
- Match perimeter to shape (e.g. `perimeter=ellipsePerimeter` for ellipses).
- XML-escape labels (`&amp;`, `&lt;`, `&gt;`, `&quot;`). HTML markup inside `value=` is allowed and is the standard way to bold/size text — see the official examples.
- Keep grid spacing on multiples of 10 px (`gridSize="10"`); leave ≥20 px gaps between siblings; sub-containers padded by ~18–24 px.
- It is normal and expected for diagrams to be authored in **negative** coordinate space (e.g. `x="-2200"`); draw.io centers on content.

Page size: **always A4 landscape** — `pageWidth="1169" pageHeight="827"`, even for dense L2. Larger virtual canvas comes from spreading groups across negative coordinates, not from changing the page size. L2 additionally sets `background="none"` on `<mxGraphModel>`.

### 5. Write the file

Save to the path the user requested (default: workspace root, `btp-diagram.drawio`). Do not overwrite an existing file without confirming.

### 6. Open via the MCP server

Detect which draw.io MCP integration is available, in this order — use the first that is configured:

1. **MCP Tool Server** (`@drawio/mcp` / `npx @drawio/mcp`): call its "open diagram" tool with the generated XML to launch the editor in the browser.
2. **MCP App Server** (`mcp.draw.io/mcp` remote): call its render tool to embed the interactive viewer inline in chat.
3. **Neither configured**: skip silently and instead print a `https://app.diagrams.net/?pv=0&grid=0#create=...` URL built per the FAQ (URI-encode JSON `{"type":"xml","compressed":true,"data":"<base64-deflate-raw>"}`). If you cannot compress in-context, print the file path and instruct the user to open it in their installed draw.io.

Never invent an MCP tool name — only call tools that actually appear in the available tool list.

### 7. Validate before delivering

Run the bundled validator script first — it codifies most of the checklist:

```sh
python3 skills/btp-diagram-generator/scripts/validate_diagram.py <file.drawio>
```

If it warns about blurry icons (SVG intrinsic size smaller than cell), fix in place:

```sh
python3 skills/btp-diagram-generator/scripts/upscale_svg_icons.py <file.drawio> --size 48 --in-place
```

Then verify these remaining items by eye:

- [ ] All labels XML-escaped.
- [ ] No overlapping shapes (≥20px gap).
- [ ] BTP container visually encloses all BTP services; external systems sit outside it.
- [ ] L0 diagrams have no legend and neutral connectors; L2 includes a legend card top-right and a description block under the title.
- [ ] Edge labels are pill _vertex_ cells, not inline `value=` text on the `edge="1"` cell.

The validator covers everything else: root cells, unique IDs, vertex/edge exclusivity, no `mxgraph.sap.*`, edge source/target validity, port pinning, manual waypoints, SVG intrinsic size vs cell geometry, palette colors, and A4 landscape page size.

For deeper validation, reference [`mxfile.xsd`](https://github.com/jgraph/drawio-mcp/blob/main/shared/mxfile.xsd) and the [style reference checklist](https://github.com/jgraph/drawio-mcp/blob/main/shared/style-reference.md#15-validation-checklist-for-ai-generated-files).

## Final response template

When done, respond with:

1. The saved file path as a workspace-relative markdown link.
2. Whether the diagram was opened in the MCP editor (and how), or the fallback URL/instructions.
3. A short bullet list of **assumptions made** and any **icons that fell back** to generic tiles, so the user can correct them.
4. If the diagram opened in a draw.io workspace using **dark theme**, mention that SAP labels (`#1D2D3E`) are intentionally dark per the Fiori Horizon spec and will appear faint on dark canvas — switch draw.io to light theme or export to PNG/SVG to verify.
5. One sentence on how to iterate (e.g. "ask me to add X service or change the audience level to L2").

## Bundled assets

- [reference/icon-index.json](reference/icon-index.json) — flat `{title → {style, width, height}}` map of all 100 BTP service icons + 3 generic user icons (`generic:user-sap` / `-non-sap` / `-highlight`). **Primary lookup source for icon styles.** The Quick-Path builder reads this for you.
- [reference/icon-aliases.json](reference/icon-aliases.json) — short-name → canonical-key map (132 aliases like `"task center"`, `"cpi"`, `"hana cloud"`, `"end user"`). Drives the fuzzy lookup in `BtpDiagram.service()`.
- [reference/styles.json](reference/styles.json) — named SAP style strings (`container_btp`, `card_subaccount`, `tile_external_sap`, `arrow_dblhd`, `pill_auth`, …) + port-pin fragments + per-level icon sizes. Loaded by the builder; useful as a copy-paste reference when hand-authoring XML.
- [reference/templates/](reference/templates/) — empty L0/L1/L2 mxfile skeletons, ready to fill in.
- [reference/sap-logo.b64.txt](reference/sap-logo.b64.txt) — base64 of the SAP corner logo SVG, embedded by `btp_container(with_logo=True)`.
- [reference/libraries/](reference/libraries/) — the 7 official SAP draw.io `mxlibrary` XML files (foundational, integration-suite, app-dev-automation, data-analytics, AI, BTP-SaaS, and the all-in-one size-M set). Use when you need raw library data the index doesn't expose.
- [reference/svg/](reference/svg/) — 129 raw `.svg` source files for every BTP service icon. Use when you need to edit/recolor an icon, export to non-draw.io targets, or embed an icon outside a draw.io style string.
- [reference/examples/](reference/examples/) — the 11 official editable example diagrams (Task Center L0/L1/L2, Build Work Zone L2, Process Automation L2, Cloud Identity Services L1/L2, Private Link L2, SAP Start L2). **Primary source for compound style patterns** (subaccount card, network boundary, pill labels, legend card).
- [reference/sap-btp-palette.json](reference/sap-btp-palette.json) — the exact color tokens above, ready to paste into draw.io `Extras → Configuration` `customColorSchemes`.
- [reference/example-patterns.md](reference/example-patterns.md) — ready-to-copy style strings, sizes, label HTML and connector/pill recipes extracted from the example diagrams. **Consult this whenever you need the exact style of a container, icon, edge or pill — do not improvise.**

## Bundled scripts

In `scripts/`, runnable with `uv run python` (no third-party dependencies):

- [scripts/btp_builder/](scripts/btp_builder/) — **the Quick-Path package**. `BtpDiagram` DSL, icon lookup with alias resolution, palette constants, port-pin helpers, SVG upscaling, named styles. Import as `from btp_builder import BtpDiagram`.
- [scripts/examples/task_center_arch.py](scripts/examples/task_center_arch.py) — runnable canonical example reproducing the Task Center reference architecture end-to-end.
- [scripts/open_diagram.py](scripts/open_diagram.py) — opens a `.drawio` file via the OS opener (macOS `open`, Linux `xdg-open`, Windows `start`); falls back to printing an `app.diagrams.net` URL.
- [scripts/validate_diagram.py](scripts/validate_diagram.py) — enforces the §7 checklist. Catches `mxgraph.sap.*` typos, duplicate IDs, edges with broken source/target, missing port pins, manual waypoints, off-palette colors, and SVG intrinsic-size blur. Use `--strict-palette` and `--strict-waypoints` to fail on warnings. Also exposes `validate_xml(xml)` / `validate_path(path)` for reuse from Python.
- [scripts/upscale_svg_icons.py](scripts/upscale_svg_icons.py) — fixes blurry icons by patching the root `<svg>` `width`/`height` to match the cell geometry (keeps `viewBox` unchanged). Default target 48 px; pass `--size 32` for L2, `--size 50` for L0. Use `--in-place` to overwrite. (The Quick-Path builder applies this automatically; only run manually on hand-authored XML.)
