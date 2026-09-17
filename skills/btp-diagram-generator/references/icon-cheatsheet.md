# BTP Service → real draw.io style cheatsheet

> **CRITICAL:** There is no `mxgraph.sap.*` stencil family. SAP BTP icons in draw.io are NOT loaded as a built-in stencil — they are vector SVGs embedded as base64 inside a `shape=image;image=data:image/svg+xml,<base64>` style string, distributed via the [SAP shape library XML files](https://github.com/SAP/btp-solution-diagrams/tree/main/assets/shape-libraries-and-editable-presets/draw.io). Inventing a stencil id (e.g. `shape=mxgraph.sap.foo`) renders an empty square.

## How to get a working icon

For every BTP service you place in a diagram, you must obtain its real `style=` string from one of these sources, in priority order:

### Source 1 — pull from a cached library file in the workspace (preferred)

If the workspace contains a copy of the SAP draw.io libraries (typically under `libs/sap-btp/*.xml` or `assets/shape-libraries-*/draw.io/**/*.xml`), open the library XML, find the `<mxCell>` whose `value=` matches the service name, and copy its `style=` string verbatim into your generated diagram. Resize via the cell's `<mxGeometry width=… height=…>` rather than mutating the style.

### Source 2 — fetch the live library from the SAP repo

Use the raw URLs below. Each library file is an `<mxlibrary>` JSON wrapper containing one `<mxCell>` per icon. Parse the library, locate the icon by `value=` (the service display name), and copy its `style`.

| Set | Raw URL (size M = 64×64; replace `02-` with `01-` for S, `03-` for L) |
|---|---|
| Foundational | `https://raw.githubusercontent.com/SAP/btp-solution-diagrams/main/assets/shape-libraries-and-editable-presets/draw.io/20-02-00-sap-btp-service-icons-foundational-set/20-02-00-02-sap-btp-service-icons-foundational-size-M.xml` |
| Integration Suite | `…/20-02-01-sap-btp-service-icons-integration-suite-set/20-02-01-02-sap-btp-service-icons-integration-suite-size-M.xml` |
| App Dev & Automation | `…/20-02-02-sap-btp-service-icons-app-dev-automation-set/20-02-02-02-sap-btp-service-icons-app-dev-automation-size-M.xml` |
| Data & Analytics | `…/20-02-04-sap-btp-service-icons-data-analytics-set/20-02-04-02-sap-btp-service-icons-data-analytics-size-M.xml` |
| AI | `…/20-02-05-sap-btp-service-icons-ai-set/20-02-05-02-sap-btp-service-icons-ai-size-M.xml` |
| BTP SaaS | `…/20-02-06-sap-btp-service-icons-btp-saas-set/20-02-06-02-sap-btp-service-icons-btp-saas-size-M.xml` |
| All-in-one (every service) | `…/20-02-99-sap-btp-service-icons-all/…-size-M.xml` |
| Generic icons | `…/20-03-generic-icons/…` |

The actual style string for a placed BTP service icon looks like (truncated):

```
shape=image;verticalLabelPosition=bottom;verticalAlign=top;imageAspect=0;aspect=fixed;
image=data:image/svg+xml,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9...
points=[[0,0,0,0,0],…];
fontStyle=0;fontSize=12;fontColor=#1D2D3E
```

Default geometry: `width="64" height="64"` for size M. The label goes in the cell's `value` attribute and renders below the icon.

### Source 3 — fallback tile (use ONLY if the icon is genuinely unavailable)

If you cannot retrieve the real style for a service in this turn, use this styled tile and clearly flag it:

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#EBF8FF;strokeColor=#0070F2;strokeWidth=1.5;
fontSize=12;fontColor=#1D2D3E;align=center;verticalAlign=middle;
```

Geometry: `120×60`. Label = service name. Then list every fallback tile in your final response so the user can swap them later.

> **Never** invent `shape=mxgraph.sap.<anything>` — those stencils do not exist and render as empty squares.

## Service-name lookup hints

Library files use the official product names as the `value=`. When searching:

| User says… | Search the library for `value=` containing… |
|---|---|
| CAP / CAP backend | usually a generic Build Code or runtime tile, not a dedicated service |
| Build Code | `SAP Build Code` |
| Build Apps | `SAP Build Apps` |
| Build Process Automation | `SAP Build Process Automation` |
| Build Workzone | `SAP Build Work Zone` |
| Integration Suite / CPI | `Cloud Integration` |
| API Management | `API Management` |
| Event Mesh / AEM | `Event Mesh` or `Advanced Event Mesh` |
| HANA Cloud | `SAP HANA Cloud` |
| Datasphere | `SAP Datasphere` |
| SAC | `SAP Analytics Cloud` |
| AI Core | `SAP AI Core` |
| Joule | `Joule` |
| Cloud Foundry runtime | `Cloud Foundry Runtime` |
| Kyma runtime | `Kyma Runtime` |
| ABAP environment | `ABAP Environment` |
| IAS | `Identity Authentication` |
| IPS | `Identity Provisioning` |
| XSUAA | `Authorization and Trust Management` |
| Destination | `Destination` |
| Connectivity / Cloud Connector | `Connectivity` / `Cloud Connector` |

If the substring isn't found, fall back per Source 3.

## External / non-BTP shapes

Use neutral rectangles so they're visually distinct from BTP services:

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F6F7;strokeColor=#475E75;strokeWidth=1;
fontSize=12;fontColor=#1D2D3E;align=center;verticalAlign=middle;
```

For SAP non-BTP products (S/4HANA Cloud, SuccessFactors, Ariba, …) the SAP repo also ships a "Cloud Solutions" / SaaS library — apply the same Source 1/2 lookup against the BTP SaaS library.

For end users / personas, fall back to the built-in actor: `shape=actor;html=1;`.

## Connector styles (these are real)

| Purpose | Style |
|---|---|
| L0 neutral link | `endArrow=none;html=1;strokeColor=#475E75;strokeWidth=1.5;` |
| L1/L2 directional | `endArrow=classicThin;html=1;rounded=0;strokeColor=#475E75;fontSize=10;fontColor=#1D2D3E;` |
| Async / event | `endArrow=classicThin;dashed=1;dashPattern=4 4;strokeColor=#5D36FF;` |
| Error / failure path | `endArrow=classicThin;strokeColor=#D20A0A;` |
| Bidirectional sync | `startArrow=classicThin;endArrow=classicThin;` |

## Why labels can look invisible

SAP guideline labels use `fontColor=#1D2D3E` (near-black). In a draw.io **dark theme** editor those labels appear faint against the dark canvas, but they render correctly in any PNG/SVG export, the lightbox, or a light-theme editor. Do not change the font color — instruct the user to switch draw.io to light theme to verify.

## Quick fetch helper (one-shot)

When generating a fresh diagram, fetch the all-in-one library once, parse it, and build an in-memory map of `name → style`. Pseudocode:

```python
import urllib.request, re, html
url = "https://raw.githubusercontent.com/SAP/btp-solution-diagrams/main/assets/shape-libraries-and-editable-presets/draw.io/20-02-99-sap-btp-service-icons-all/20-02-99-02-sap-btp-service-icons-all-size-M.xml"
# library is wrapped as <mxlibrary>[{...},{...}]</mxlibrary> where each item has "xml" containing an <mxCell ... value="…" style="…">
```

Each library entry is a JSON object with an `xml` field containing a compressed/uncompressed mxCell snippet — decode it (deflate-raw + base64 if compressed) to read `value` and `style`. Cache the result to `.cache/sap-btp-icons.json` in the workspace so subsequent diagrams don't re-download.
