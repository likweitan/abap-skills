# ATC Cloudification Repository - Quick Reference

## JSON File URLs by Target Product

### SAP Cloud ERP

| File                         | URL                                                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Released APIs (Latest)**   | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfoLatest.json`                  |
| **CSV (offline processing)** | Corresponding CSV files available in the [src directory](https://github.com/SAP/abap-atc-cr-cv-s4hc/tree/main/src) |

**ATC Check**: "Cloud Readiness" → Usage of Released APIs (Cloudification Repository)

---

### SAP Cloud ERP Private

| File                   | URL                                                                                                   |
| ---------------------- | ----------------------------------------------------------------------------------------------------- |
| **Latest version**     | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCELatest.json` |
| **Release 2025 FPS01** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCE2025_1.json` |
| **Release 2025 FPS00** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCE2025_0.json` |
| **Release 2023 FPS03** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCE2023_3.json` |
| **Release 2023 FPS02** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCE2023_2.json` |
| **Release 2023 FPS01** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCE2023_1.json` |
| **Release 2023 FPS00** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCE2023_0.json` |
| **Release 2022 FPS02** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCE2022_2.json` |
| **Release 2022 FPS01** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCE2022_1.json` |
| **Release 2022 FPS00** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCE2022.json`   |

**ATC Check**: "Clean Core" → Usage of Released APIs (Cloudification Repository)

**URL pattern**: `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCE{YEAR}_{FPS}.json`

> **Note**: JSON files are available for Feature Pack Stack (FPS) releases of Cloud ERP Private only. No dedicated support package updates on JSON files.

---

### New Clean Core Check (Classic APIs)

| File                                      | URL                                                                                                        |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Object Classifications (SAP)**          | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectClassifications_SAP.json`        |
| **Object Classifications (3-Tier Model)** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectClassifications_3TierModel.json` |
| **Object Classifications (General)**      | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectClassifications.json`            |

**ATC Check**: "Usage of APIs" and "Allowed Enhancement Technologies" (Note [3565942](https://me.sap.com/notes/3565942))

---

### SAP BTP, ABAP Environment

| File           | URL                                                                                                   |
| -------------- | ----------------------------------------------------------------------------------------------------- |
| **BTP Latest** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_BTPLatest.json` |

---

## Required SAP Notes

### Cloud Readiness approach

| Note                                                         | Description                  |
| ------------------------------------------------------------ | ---------------------------- |
| [3284711](https://launchpad.support.sap.com/#/notes/3284711) | ATC Check for GitHub Repo    |
| [3377462](https://launchpad.support.sap.com/#/notes/3377462) | Fix error in ATC Check       |
| [3507814](https://launchpad.support.sap.com/#/notes/3507814) | Own released objects support |

### Clean Core approach (SAP Cloud ERP Private)

| Note                                                         | Description                                                       |
| ------------------------------------------------------------ | ----------------------------------------------------------------- |
| [3449860](https://launchpad.support.sap.com/#/notes/3449860) | Classic APIs support in ATC Checks                                |
| [3489660](https://me.sap.com/notes/3489660)                  | Enable deployment into UI5 ABAP Repository with ABAP Cloud        |
| [3565942](https://me.sap.com/notes/3565942)                  | ATC Checks "Usage of APIs" and "Allowed Enhancement Technologies" |
| [3710789](https://launchpad.support.sap.com/#/notes/3710789) | Function group fix for Classic APIs                               |
| [3470426](https://me.sap.com/notes/3470426)                  | Collection note for >20000 Level A released data elements         |

### SSL Setup

Ensure [SSL setup](https://docs.abapgit.org/user-guide/setup/ssl-setup.html) to access GitHub from S/4HANA system via ATC. See note [3582797](https://me.sap.com/notes/3582797/E) for SSL Handshake troubleshooting.

---

## Clean Core Levels and API State Mapping

SAP objects have **states** that map to Clean Core **levels** for custom code classification:

| Clean Core Level | API State in JSON | Viewer State       | Description                                                                                |
| ---------------- | ----------------- | ------------------ | ------------------------------------------------------------------------------------------ |
| **Level A**      | `released`        | Released           | Allowed in ABAP Cloud developments (ABAP for Cloud Development language version)           |
| **Level A**      | `deprecated`      | Deprecated         | Still usable in ABAP Cloud, but a newer recommended API exists — prefer the successor      |
| **Level B**      | `classicAPI`      | Classic API        | Usable only in standard ABAP (not ABAP Cloud). Use wrapper pattern to bridge to ABAP Cloud |
| **Level C**      | `notToBeReleased` | Not to be released | Not permitted in ABAP Cloud. A successor API is available — migrate to it                  |
| **Level D**      | `noAPI`           | No API             | Not usable in ABAP Cloud, not recommended for standard ABAP either                         |
| —                | `internalAPI`     | Internal API       | SAP-internal use only, not available for customer/partner development                      |

### JSON file state fields

- **`objectReleaseInfo*.json`** (Cloud Readiness check): States are `released`, `deprecated`, `notToBeReleased`, `notReleased`
- **`objectClassifications*.json`** (Clean Core check): States are `classicAPI`, `noAPI`, `internalAPI`

### Labels

| Label                      | Meaning                                                                 |
| -------------------------- | ----------------------------------------------------------------------- |
| `remote-enabled`           | The API is RFC-enabled for remote calls                                 |
| `transactional-consistent` | Supports commit/rollback semantics, suitable for RAP-based applications |

### Development guidance by level

- **New development**: Always target **Level A** (released APIs) with ABAP Cloud language version
- **Level B extensions**: Use standard ABAP language version; wrap classic APIs with the [Tier 2 RFC proxy](https://github.com/SAP-samples/tier2-rfc-proxy) when bridging to ABAP Cloud
- **Level C objects**: Identify and migrate to the successor API listed in the JSON
- **Level D objects**: Avoid entirely — no successor planned

---

## Configuration Steps

### Step 1: Implement Required SAP Notes

Install the relevant SAP Notes for your target product (see tables above).

### Step 2: Configure ATC Check Variant

1. Open transaction **ATC** (or **SCI** for Code Inspector)
2. Create or edit your check variant
3. For **SAP Cloud ERP**: Activate "Cloud Readiness" → "Usage of Released APIs (Cloudification Repository)"
4. For **SAP Cloud ERP Private**: Activate "Clean Core" → "Usage of Released APIs (Cloudification Repository)"

### Step 3: Set the JSON URL

In the attributes of the check, enter the appropriate JSON URL from the tables above.

### Step 4: Run ATC Checks

Execute the ATC check variant against your custom code objects to identify usage of unreleased APIs.

---

## Cloudification API Viewer

Browse released APIs online:

| Product                      | Viewer URL                                                                          |
| ---------------------------- | ----------------------------------------------------------------------------------- |
| SAP Cloud ERP                | https://sap.github.io/abap-atc-cr-cv-s4hc/                                          |
| SAP Cloud ERP Private        | https://sap.github.io/abap-atc-cr-cv-s4hc/?version=objectReleaseInfo_PCELatest.json |
| Classic API Clean Core Model | https://sap.github.io/abap-atc-cr-cv-s4hc/?version=objectClassifications_SAP.json   |

---

## Partner Extensions

Partners can offer released APIs as part of extension shipments. Use Report `SYCM_API_CLASSIFICATION_MANAGR` to generate partner JSON files. Each namespace needs its own JSON filename: `objectClassifications_NAMESPACE.json`. Partner files are hosted in the [src/partner](https://github.com/SAP/abap-atc-cr-cv-s4hc/tree/main/src/partner) folder.

Required note: [3630552](https://me.sap.com/notes/3630552) - Classic API Support in ATC Check "Usage of APIs" for Partners.

---

## Customer Influence Channels

- [SAP Cloud ERP](https://influence.sap.com/sap/ino/#campaign/2759)
- [SAP Cloud ERP Private](https://influence.sap.com/sap/ino/#/campaign/3516)
- Details in note [3126893](https://launchpad.support.sap.com/#/notes/3126893)

---

## Related Resources

- **Repository**: https://github.com/SAP/abap-atc-cr-cv-s4hc
- **Classic API Wrappers**: https://github.com/SAP-samples/tier2-rfc-proxy
- **LLM-optimized TOON format**: Available in `objectClassifications_SAP.toon` and `objectReleaseInfo_PCELatest.toon`
