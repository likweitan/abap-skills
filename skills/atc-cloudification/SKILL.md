---
name: atc-cloudification
description: Configure ATC Cloud Readiness and Clean Core checks using the SAP Cloudification Repository for Released APIs. Use when users ask about ATC check variants for cloud readiness, clean core compliance, released API checks, cloudification repository setup, objectReleaseInfo JSON files, SAP Cloud ERP or SAP Cloud ERP Private API validation, or migrating custom code to ABAP Cloud. Triggers include "configure ATC cloud readiness", "set up clean core check", "cloudification repository URL", "released APIs check", or "which JSON file for my S/4HANA version".
---

# ATC Cloudification Repository Check

Configure the ABAP Test Cockpit (ATC) check **"Usage of Released APIs (Cloudification Repository)"** to validate custom code against SAP's released API list for SAP Cloud ERP and SAP Cloud ERP Private.

## Overview

The [SAP Cloudification Repository](https://github.com/SAP/abap-atc-cr-cv-s4hc) contains the list of released and unreleased APIs for SAP Cloud ERP. The JSON files from this repository are used as content for the ATC check, enabling customers and partners to analyse existing custom code for released API usage across all ECC and S/4HANA releases.

## Quick Reference

Read `references/quick-reference.md` for:

- JSON file URLs for each target product and version
- ATC check variant configuration steps
- Available JSON files and their purpose
- SAP Notes required for setup

## Configuration by Target Product

### SAP Cloud ERP

1. Activate in your ATC check variant: **"Cloud Readiness"** → **Usage of Released APIs (Cloudification Repository)**
2. In the check attributes, enter the URL:
   ```
   https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfoLatest.json
   ```

### SAP Cloud ERP Private

1. Activate in your ATC check variant: **"Clean Core"** → **Usage of Released APIs (Cloudification Repository)**
2. In the check attributes, enter the URL for your version:
   - **Latest version**: `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCELatest.json`
   - **Specific release**: Replace `PCELatest` with the version, e.g. `PCE2025_0` for Release 2025 FPS00

### New Clean Core Check (Note 3565942)

For the newer ATC checks **"Usage of APIs"** and **"Allowed Enhancement Technologies"**, use:

```
https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectClassifications_SAP.json
```

## Clean Core Levels and API State Mapping

Custom objects are assigned Clean Core **levels**, while SAP objects are categorized into **states**. The mapping is:

| Clean Core Level | API State          | Meaning                                                                                               |
| ---------------- | ------------------ | ----------------------------------------------------------------------------------------------------- |
| **Level A**      | Released           | Allowed in ABAP Cloud developments (language version "ABAP for Cloud Development")                    |
| **Level A**      | Deprecated         | Still usable in ABAP Cloud, but a newer recommended API exists and should be preferred                |
| **Level B**      | Classic API        | Usable only in standard ABAP developments (language version "Standard ABAP"), not in ABAP Cloud       |
| **Level C**      | Not to be released | Not permitted in ABAP Cloud developments, but a successor API is available and should be used instead |
| **Level D**      | No API             | Not usable in ABAP Cloud, and also not recommended for standard ABAP developments                     |

### Key rules

- **Level A** (Released): Use these APIs for all new ABAP Cloud development. These are the target.
- **Level B** (Classic API): Permitted for clean core extensions in standard ABAP only. Use the wrapper pattern (Tier 2 RFC proxy) to bridge to ABAP Cloud when no Level A successor exists.
- **Level C** (Not to be released): A successor API exists — migrate to the successor.
- **Level D** (No API): Avoid entirely. No successor is planned.
- **Deprecated**: Technically still Level A, but plan migration to the newer replacement API.

### JSON files and states

- `objectReleaseInfo*.json` files contain states: `released`, `deprecated`, `notToBeReleased`, `notReleased`
- `objectClassifications*.json` files contain states: `classicAPI`, `noAPI`, `internalAPI`
- Labels: `remote-enabled` (RFC-enabled), `transactional-consistent` (suitable for RAP-based applications)

## Workflow

1. **Determine the target product**: SAP Cloud ERP or SAP Cloud ERP Private
2. **Identify the correct JSON file** using the quick reference
3. **Verify prerequisites**: Ensure required SAP Notes are implemented
4. **Configure ATC check variant** with the appropriate check and JSON URL
5. **Run ATC checks** on custom code to identify usage of unreleased APIs
6. **Review findings** and plan remediation using successor API information and the level mapping above

## Cloudification API Viewer

Use the online viewers to browse released APIs interactively:

- **SAP Cloud ERP**: https://sap.github.io/abap-atc-cr-cv-s4hc/
- **SAP Cloud ERP Private**: https://sap.github.io/abap-atc-cr-cv-s4hc/?version=objectReleaseInfo_PCELatest.json
- **Classic API Clean Core Model**: https://sap.github.io/abap-atc-cr-cv-s4hc/?version=objectClassifications_SAP.json
