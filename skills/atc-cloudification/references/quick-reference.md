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
| **Object Classifications (General)**      | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectClassifications.json`            |
| **Object Classifications (legacy 3-tier)** | `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectClassifications_3TierModel.json` — superseded by the level concept |

**ATC Check**: "Usage of APIs" and "Allowed Enhancement Technologies" (Note [3565942](https://me.sap.com/notes/3565942))

> Use `objectClassifications_SAP.json` for the clean core level concept. The `_3TierModel` file reflects the superseded 3-tier model and is retained for backward compatibility only.

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

## Clean Core Levels and Object Classification

An extension is classified by the **lowest** clean core level of any SAP object it consumes.

| Clean Core Level | SAP object qualifier                     | JSON state / default                | ATC finding              | Meaning                                                                                  |
| ---------------- | ---------------------------------------- | ----------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------- |
| **Level A**      | `[Released]` remote/local API, ext. point | `released` (also `deprecated`)      | No finding               | Governed by a formal **stability contract**. Target state for all new development.       |
| **Level B**      | `[Classic]` SAP API / extension point     | `classicAPI`                        | Priority 3 (information) | SAP-nominated classic APIs and frameworks. No stability contract, but proven stable.     |
| **Level C**      | `[Internal]` SAP object                   | **default** for unclassified; `internalAPI` when a successor exists | Priority 2 (warning) | Not released, not documented, not supported. Conditionally clean with the changelog. |
| **Level D**      | `[Not recommended]` object / technology   | `noAPI`                             | Priority 1 (error)       | Explicitly unfit for customer use. Highest risk and technical debt — remediate now.      |

**Clean core status**: Level A = clean core · Levels B and C = conditional clean core · Level D = not clean core.

> **Important**: any SAP object that is not released and not listed in the classification JSON defaults to **internal** (Level C). There is no "unclassified = safe" state.

### JSON file state fields

- **`objectReleaseInfo*.json`** (release state): `released`, `deprecated`, `notToBeReleased`, `notReleased`
- **`objectClassifications_SAP.json`** (clean core classification): `classicAPI` (Level B), `noAPI` (Level D), `internalAPI` (Level C with a released successor available)

### Classified object types

Classic API classifications are provided for:

| Type   | Description       |
| ------ | ----------------- |
| `FUNC` | Function modules  |
| `CLAS` | Classes           |
| `INTF` | Interfaces        |
| `STOB` | CDS views         |
| `BDEF` | BO interfaces     |

DDIC objects (data elements, structures, table types) are **not** classified and are **not** checked by ATC when used as data types. Only SQL access to SAP tables is checked.

### Labels

| Label                      | Meaning                                                                            |
| -------------------------- | ---------------------------------------------------------------------------------- |
| `remote-enabled`           | The API is RFC-enabled for remote calls                                            |
| `transactional-consistent` | The API can be used inside RAP-based applications (respecting the RAP transactional model) |

### ATC findings mapped to levels

| ATC priority             | Level | Finding                                                                          | Recommended action                                |
| ------------------------ | ----- | -------------------------------------------------------------------------------- | ------------------------------------------------- |
| **Priority 1 (Error)**   | **D** | Object is modified                                                               | Remove modification; use a BAdI instead           |
|                          |       | Enhancement technology is not allowed                                            | Delete enhancement implementation; use a BAdI     |
|                          |       | Implicit or explicit enhancement (source code plug-in)                           | Delete enhancement implementation; use a BAdI     |
|                          |       | Direct **write** access to SAP database tables                                   | Use released or classic APIs                      |
|                          |       | Call of form routines in SAP program                                             | Use released or classic APIs                      |
|                          |       | Usage of SAP object classified as `noAPI` (e.g., `RFC_READ_TABLE`)                | Use released or classic APIs; use successor info  |
|                          |       | Usage of critical ABAP statements                                                | Use released or classic APIs                      |
| **Priority 2 (Warning)** | **C** | Direct **read** access to SAP database table/view                                | Use released CDS view or classic API              |
|                          |       | Usage of SAP object not classified as classic API (internal) and not released    | Use released or classic APIs                      |
| **Priority 3 (Info)**    | **B** | Usage of deprecated APIs                                                         | Use the successor instead                         |
|                          |       | Usage of classic APIs (e.g., `CL_GUI_ALV_GRID`)                                   | — acceptable, no action required                  |

### Development guidance by level

- **New development**: always target **Level A** (released APIs) with the ABAP for Cloud Development language version
- **Level B**: acceptable in classic ABAP development where no released API exists. Wrappers around classic APIs are Level B and can be released for ABAP Cloud consumption. Reference: the [classic API wrapper samples](https://github.com/SAP-samples/tier2-rfc-proxy)
- **Level C**: minimize. Replace with released or classic APIs; if unavoidable, wrap the object and create a single fine-grained ATC exemption. Import the changelog for SAP objects via `SYCM` to detect upcoming incompatible changes
- **Level D**: eliminate entirely. Use successor information from the JSON where available

### Remediation priority

1. **Level D** — eliminate: no modifications, no implicit/explicit enhancements, no table writes, no `noAPI` objects, no critical statements, no SAP form routine calls
2. **Level C** — minimize: no direct table reads, replace internal APIs, check the changelog for remaining usages
3. **Level B** — monitor: adopt successors for deprecated APIs, watch for released equivalents
4. **Level A** — sustain: enforce with `S_ABPLNGVS` authorization and separate software components

---

## Configuration Steps

### Step 1: Implement Required SAP Notes

Install the relevant SAP Notes for your target product (see tables above). Note **3565942** is required for the clean core checks.

### Step 2: Set Up a Central ATC System

Set up a central ATC system for the whole landscape:
- Public cloud solution on **SAP BTP** — SAP's recommended option
- Or installed in the private cloud / on-premise landscape

### Step 3: Configure the Global ATC Check Variant

1. Open transaction **ATC** (or **SCI** for Code Inspector)
2. Start from `ABAP_CLEAN_CORE_DEVELOPMENT` (SAP-delivered) or `ABAP_CLOUD_DEVELOPMENT_DEFAULT`
3. Include the clean core checks:

| Check                                | Technical name                  | Category                 |
| ------------------------------------ | ------------------------------- | ------------------------ |
| Usage of APIs                        | `SYCM_USAGE_OF_APIS`            | Clean core               |
| Allowed enhancement technologies     | `SYCM_ALLOWED_ENH_TECHNOLOGY`   | Clean core               |
| Search customer modifications        | `CI_SEARCH_CUST_MODIFICATIONS`  | Clean core               |
| Critical statements                  | `CI_CRITICAL_STATEMENTS`        | Clean core               |
| Code Vulnerability Analyzer          | `SLIN_SEC`                      | Additionally recommended |

4. For the Cloudification Repository check specifically:
   - **SAP Cloud ERP**: activate "Cloud Readiness" → "Usage of Released APIs (Cloudification Repository)"
   - **SAP Cloud ERP Private**: activate "Clean Core" → "Usage of Released APIs (Cloudification Repository)"

### Step 4: Set the JSON URL

In the attributes of the check, enter the appropriate JSON URL from the tables above.

### Step 5: Configure Transport Settings

Configure ATC transport settings so **priority 1 and 2 findings block the release** of transport tasks and requests.

### Step 6: Import the Changelog for SAP Objects

1. Download the Simplification Database file from the SAP Software Download Center (SAP Support Portal)
2. Import it via transaction `SYCM`
3. Run the changelog ATC check to detect incompatibly changed internal (Level C) objects

### Step 7: Run ATC Checks

Execute the global check variant against custom code, then map findings to clean core levels (P1→D, P2→C, P3→B).

### Step 8: Govern Exemptions

- Exempt only **priority 1 and 2** findings; never exempt priority 3 (classic API usage)
- Use **fine-granular, finding-level** exemptions
- Prefer wrapping the SAP object so one exemption covers all usages
- Use an **ATC baseline** only for legacy code that will not be changed
- Monitor via the **ATC exemption browser**

### Critical statements covered

`CI_CRITICAL_STATEMENTS` reports: kernel function calls · system-calls · editor calls · `EXEC SQL` · database hints · generation of reports and Dynpros · read/insert report · read/insert Dynpro · import/export nametab.

---

## Changelog for SAP Objects

Mitigates Level C upgrade risk by listing internal SAP objects with **incompatible changes** in upcoming releases.

Incompatible changes include:
- Deletion of objects (e.g., function modules)
- Renaming or deletion of function module parameters
- Incompatible changes to parameter types
- Renaming or deletion of methods in SAP classes
- Removal of fields from CDS views

Covered object types: `FUNC`, `CLAS`, `INTF`, `STOB`, `BDEF`.

Delivered via the Simplification Database infrastructure; imported with transaction `SYCM`.

> Objects in the changelog are **not** automatically demoted to Level D. Continued usage may be allowed depending on the change's scope and criticality — but findings should drive refactoring toward released or classic APIs.

---

## Cloudification API Viewer

Browse released APIs online:

| Product / content              | Viewer URL                                                                          |
| ------------------------------ | ----------------------------------------------------------------------------------- |
| SAP Cloud ERP (release info)   | https://sap.github.io/abap-atc-cr-cv-s4hc/                                          |
| SAP Cloud ERP Private (release info) | https://sap.github.io/abap-atc-cr-cv-s4hc/?version=objectReleaseInfo_PCELatest.json |
| Clean core classification      | https://sap.github.io/abap-atc-cr-cv-s4hc/?version=objectClassifications_SAP.json   |

Filter the classification viewer by `state`:

| Filter          | Clean core level | Action                                     |
| --------------- | ---------------- | ------------------------------------------ |
| `classicAPI`    | Level B          | Acceptable in classic ABAP development     |
| `internalAPI`   | Level C          | A released successor exists — migrate      |
| `noAPI`         | Level D          | Must be replaced                           |

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
- **SAP Note 3578329**: Classification of classic technologies, reuse services and application frameworks
- **Clean Core Extensibility Whitepaper**: the authoritative source for the clean core level concept
- **Extend SAP S/4HANA in the cloud and on premise with ABAP based extensions** (Version 2.3, August 2025): ATC setup and governance guidance
