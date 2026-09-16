# Clean Core Levels — Detailed Reference

Detailed reference for SAP's clean core **level concept** (Levels A, B, C, D), which supersedes the former 3-tier extensibility model.

## Why SAP evolved the model

The 3-tier extensibility model directed customers to build upgrade-safe extensions primarily via publicly released APIs, restricting technologies to those also available in the public cloud (Tier 1). This was effective but stringent:

- Many customer landscapes contain large portfolios of legacy classic ABAP code
- Even new extensions frequently use classic ABAP technologies
- A uniform, restrictive evaluation did not reflect the real spectrum of upgrade risk
- Some classic patterns (e.g., ABAP List Viewer) pose minimal upgrade risk and should not be labelled "unclean"

The level concept replaces binary "clean vs. unclean" with a graded, risk-based assessment.

### What changed

- **Classic APIs**: selected classic APIs are now recognized as upgrade-stable and acceptable (Level B), avoiding unnecessary rewrites
- **Not-recommended objects**: SAP explicitly flags objects known to cause upgrade problems, so teams avoid them early
- **Internal SAP objects**: a **changelog for SAP objects** lets customers assess upgrade risk in advance

### What did not change

- Decoupling extensions from SAP standard code remains the fundamental principle
- Level A (SAP Business AI Platform + ABAP Cloud, both SAP Build) remains the gold standard
- The "SAP Business AI Platform first" strategy still applies

## Level Overview Matrix

| Aspect                  | Level A                                              | Level B                                       | Level C                                     | Level D                                        |
| ----------------------- | ---------------------------------------------------- | --------------------------------------------- | ------------------------------------------- | ---------------------------------------------- |
| **Name**                | Extend with SAP Build and Joule Studio               | Leverage classic APIs                         | Access internal objects                     | Not recommended                                |
| **Clean core status**   | Clean core                                           | Conditional clean core                        | Conditional clean core                      | Not clean core                                 |
| **SAP object qualifier**| `[Released]` remote API, local API, extension point  | `[Classic]` SAP API, SAP extension point      | `[Internal]` SAP object                     | `[Not recommended]` object / extension point   |
| **Stability guarantee** | Formal **stability contract**                        | Expert nomination, no formal contract         | None — may change at any time               | None — actively discouraged                    |
| **Documentation**       | SAP Business Accelerator Hub, fully documented       | Documented by SAP                             | May be incomplete or absent                 | N/A                                            |
| **SAP support**         | Fully supported                                      | Supported as recommended usage                | Not in formal support scope                 | Not supported                                  |
| **ATC finding**         | None                                                 | Priority 3 (information)                      | Priority 2 (warning)                        | Priority 1 (error)                             |
| **Language version**    | ABAP for Cloud Development                           | Standard ABAP                                 | Standard ABAP                               | Standard ABAP                                  |
| **Upgrade risk**        | Minimal                                              | Low                                           | Moderate (mitigable via changelog)          | High                                           |
| **Action**              | Target state                                         | Acceptable; monitor for released successors   | Minimize; monitor changelog                 | **Remediate immediately**                      |

## The lowest-level rule

An extension is classified by the **lowest** clean core level used within it.

> Example: an extension that uses Level A released APIs plus one Level C internal object is classified as **Level C** overall.

This means a single internal object call can demote an otherwise clean application. Wrapping is the standard mitigation — it localizes the violation and reduces ATC findings to a single exemption.

## Level A — Extend with SAP Build and Joule Studio

### What to expect

Highest standard: future-ready, maximum upgrade stability, fully aligned with SAP's clean core vision. Released objects are officially supported, documented in the SAP Business Accelerator Hub, and governed by a transparent lifecycle.

**Caveat**: Level A coverage does not span the complete functional scope of SAP Cloud ERP Private, and full coverage is not planned.

### Which customer extensions qualify

- **Side-by-side** on SAP Business AI Platform (SAP Build for CAP and ABAP Cloud) using **only** released remote APIs
- **On-stack** built with key user extensibility or developer extensibility using the relevant ABAP language versions

### What it includes on the SAP side

SAP objects and extension points officially released under clearly defined stability contracts:

- Released remote APIs (OData, SOAP, events) — SAP Business Accelerator Hub
- Released local APIs (CDS views, classes, interfaces, BO interfaces) — Cloudification Repository and ADT
- Released extension points (released BAdIs, released extension includes, released RAP BOs)

### Portability note

On-stack Level A extensions for SAP Cloud ERP Private are generally **not** portable to SAP Cloud ERP (public) without adaptation, due to scope and codebase differences.

Side-by-side extensions on SAP Business AI Platform are more likely to be compatible in a private-to-public transformation because they decouple business logic from the core. Parity is not guaranteed — API availability and application scope differ, and industry solutions may have no public-cloud equivalent.

## Level B — Leverage classic APIs

### What to expect

Addresses requirements that released APIs cannot fulfil. Uses APIs and extension points nominated as **classic APIs**: well-established, broadly recommended, thoroughly documented. No formal stability contract, but a longstanding history of reliable use and SAP internal quality assurance. Significantly broader scope than Level A while still following SAP best practices.

### Which customer extensions qualify

Extensions using **only** objects classified as classic APIs or released APIs:

- Wrappers around classic APIs to enable use in Level A applications — e.g., `BAPI_PO_CREATE1`
- Classic ABAP extensions such as ALV implementations in Dynpro (SAP GUI) or Web Dynpro using `CL_GUI_ALV_GRID`
- Custom objects in ABAP language version Standard, provided they do not reference restricted or unsupported SAP objects

### What it includes on the SAP side

Objects explicitly nominated by SAP experts as classic APIs:

- Legacy APIs (BAPIs and similar)
- User exits and BAdIs deliberately exposed for customer use
- Established frameworks — SAP GUI, ABAP List Viewer grid
- Reuse services and application-specific frameworks

### Discovery

- `objectClassifications_SAP.json` in the Cloudification Repository
- Viewer: https://sap.github.io/abap-atc-cr-cv-s4hc/?version=objectClassifications_SAP.json
- **SAP Note 3578329** — classification of classic technologies, reuse services and application frameworks

Classified object types: `FUNC` (function modules), `CLAS` (classes), `INTF` (interfaces), `STOB` (CDS views), `BDEF` (BO interfaces).

DDIC objects (data elements, structures, table types) are **not** classified and are not checked by ATC when used as data types. Only SQL access to SAP tables is checked.

### The `transactional-consistent` label

Classic APIs may carry a `transactional-consistent` label indicating the API can be used inside RAP-based applications (respecting the RAP transactional model).

## Level C — Access internal objects

### What to expect

SAP internal objects that are technically accessible but not classified or intended for customer use. Not released, not recommended, not cloud-ready, not in SAP's formal support scope. Documentation may be incomplete or absent. No long-term stability or usage guarantees.

Provides access to capabilities beyond Levels A and B, at notable upgrade risk.

### Which customer extensions qualify

Objects or patterns neither formally released (A) nor nominated as mature (B):

- Direct use of internal function modules, classes, or interfaces
- **Read** access to SAP tables not endorsed for external consumption
- Custom field on a DB table via classic append
- Wrappers around internal objects

### What it includes on the SAP side

By **default**, all SAP objects are considered internal and subject to change without notice. Level C is everything not designated released (A), classic API (B), or not recommended (D).

SAP may reclassify internal objects to Level B (classic API) or Level D (not recommended), driven by customer feedback, product strategy, or observed upgrade challenges. Level C is therefore fluid.

Objects with a released successor are flagged `internalAPI` in the Cloudification Repository.

### Changelog for SAP objects

A mitigation mechanism that proactively identifies SAP internal objects targeted for **incompatible changes** in upcoming releases of SAP Cloud ERP Private.

Incompatible changes include:
- Deletion of objects (e.g., function modules)
- Renaming or deletion of function module parameters
- Incompatible changes to parameter types
- Renaming or deletion of methods in SAP classes
- Removal of fields from CDS views

Covered object types: `FUNC`, `CLAS`, `INTF`, `STOB`, `BDEF`.

**Key features:**
- Automated ATC checks analyze custom code and detect incompatible changes and deletions of referenced SAP objects
- Early access to information about future incompatible changes
- Increased planning reliability — allocate resources before the upgrade, not during it

**Delivery mechanism:** changelog information is transferred via the Simplification Database infrastructure. Download the Simplification Database file from the SAP Software Download Center and import it via transaction `SYCM`.

**Important**: objects in the changelog are **not** automatically demoted to "not recommended". Continued usage may still be allowed depending on the scope and criticality of the change. Changelog findings should nevertheless drive refactoring toward released or classic APIs where feasible.

## Level D — Not recommended

### What to expect

Most critical risk category, highest technical debt. Exposes customers to multiple risks and significant maintenance effort during upgrades and daily operations. May compromise system stability, data integrity, and business agility. **Prioritize for removal or rework without delay.**

### Which customer extensions qualify

Extensions relying on SAP objects or patterns explicitly marked as not recommended:

- Objects labelled `noAPI` in the Cloudification Repository (e.g., `RFC_READ_TABLE`)
- Modifications to SAP objects
- SAP Notes applied with manual corrections (e.g., DDIC object from SAP BASIS)
- Implicit enhancements
- Explicit enhancements / source code plug-ins
- Unsupported **write** operations on SAP tables
- Calls to form routines within SAP programs
- Critical ABAP statements
- Implementation of BAdIs flagged as SAP-internal
- Any attempt to use objects designated out-of-scope for customer consumption

### Critical ABAP statements (Level D)

The `CI_CRITICAL_STATEMENTS` ATC check considers:
- Calling a kernel function
- Using a system-call
- Using an editor call
- `EXEC SQL` calls
- Using a database hint
- Generation of reports and Dynpros
- Read/insert report
- Read/insert Dynpro
- Import/export nametab

### Discovery

Filter the Cloudification Repository Viewer for `state` = `noAPI`:
https://sap.github.io/abap-atc-cr-cv-s4hc/?version=objectClassifications_SAP.json

## ATC Governance Setup

### Recommended architecture

Set up a **central ATC system** for the whole landscape. Options:
- Public cloud solution on SAP BTP — **SAP's recommended option**
- Installed in the private cloud or on-premise landscape

Configure **one global check variant** used during development and when releasing transport tasks. Configure ATC transport settings so **priority 1 and 2 findings block the release** of transport tasks and requests.

### Clean core ATC checks

| Check                             | Category                    | Technical name                    | Purpose                                                                                                        |
| --------------------------------- | --------------------------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Allowed enhancement technologies** | Clean core               | `SYCM_ALLOWED_ENH_TECHNOLOGY`     | Reports `ENHO` enhancements using non-allowed technology. Only BAdI enhancement technology is recommended.      |
| **Usage of APIs**                 | Clean core                  | `SYCM_USAGE_OF_APIS`              | Reports usage of classic objects based on released/classic API classification; SQL on SAP tables/views; SAP form routines |
| **Search customer modifications** | Clean core                  | `CI_SEARCH_CUST_MODIFICATIONS`    | Finds modified objects, one finding per object. Checks ABAP Cloud object type support.                          |
| **Critical statements**           | Clean core                  | `CI_CRITICAL_STATEMENTS`          | Statements critical for security or program stability (kernel calls etc.)                                       |
| **Code Vulnerability Analyzer**   | Additionally recommended    | `SLIN_SEC`                        | Security vulnerabilities                                                                                        |

> If **Usage of APIs** and **Allowed Enhancement Technologies** are missing, implement **SAP Note 3565942**.

### Check variants

- Start from `ABAP_CLOUD_DEVELOPMENT_DEFAULT` as a template and enrich with the checks above
- SAP delivers a predefined `ABAP_CLEAN_CORE_DEVELOPMENT` variant for initial setup
- `ABAP_CLOUD_READINESS` checks whether ABAP Cloud rules are respected when transforming classic code

### ATC findings mapped to levels

| ATC priority          | Level | Finding                                                                          | Recommended action                                    |
| --------------------- | ----- | -------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Priority 1 (Error)**   | D  | Object is modified                                                               | Remove modification; use a BAdI instead if needed     |
|                       |       | Enhancement technology is not allowed                                            | Delete enhancement implementation; use a BAdI         |
|                       |       | Implementation of implicit or explicit enhancement (source code plug-in)         | Delete enhancement implementation; use a BAdI         |
|                       |       | Direct **write** access to SAP database tables                                   | Use released or classic APIs instead                  |
|                       |       | Call of form routines in SAP program                                             | Use released or classic APIs instead                  |
|                       |       | Usage of SAP object classified as `noAPI`                                         | Use released or classic APIs; use successor info       |
|                       |       | Usage of critical ABAP statements                                                | Use released or classic APIs instead                  |
| **Priority 2 (Warning)** | C  | Direct **read** access to SAP database table/view                                | Use released CDS view or classic API instead          |
|                       |       | Usage of SAP object not classified as classic API (SAP internal) and not released | Use released or classic APIs instead                  |
| **Priority 3 (Info)**    | B  | Usage of deprecated APIs                                                         | Use the successor instead                             |
|                       |       | Usage of classic APIs                                                            | — (acceptable, no action required)                    |

### ATC exemption strategy

- Focus exemptions on **priority 1 (Error)** and **priority 2 (Warning)** findings
- **Do not** create exemptions for priority 3 (Info) findings such as classic API usage
- Use **fine-granular, finding-level** exemptions for clean core findings — best governance
- Use an **ATC baseline** only for old legacy code you will not change, to hide a large set of clean core findings
- **Preferred practice**: wrap the SAP object and use the wrapper in custom code. One usage → one exemption instead of many
- Use the **ATC exemption browser** to monitor exemptions and track clean core adoption

## Development Model Setup

| Model                        | Purpose                                            | Tools / rules                                                                                                                                                       | Custom ABAP code structuring                            |
| ---------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| **ABAP Cloud development**   | Cloud-ready development of new apps and extensions | Objects in language version ABAP for Cloud Development · rules enforced by syntax and runtime checks · ADT mandatory · developer role `SAP_BC_ABAP_DEVELOPER_5`      | Software component with language version ABAP for Cloud Development |
| **Classic ABAP development** | Usage of legacy technologies                       | Objects in language version Standard ABAP · rules controlled via ATC (e.g., classic API usage)                                                                        | Packages in `HOME` or existing classic software component |

### Access rules

**ABAP Cloud objects** may access only:
1. Custom objects inside the same software component
2. Released SAP objects (released APIs)
3. Custom objects released for ABAP Cloud development (released custom APIs) from a classic component

**Classic ABAP objects** should access only:
1. Custom objects inside their own software component
2. Released SAP APIs and classic SAP APIs
3. Custom objects in classic and ABAP Cloud software components

### Authorization-based enforcement

Authorization object `S_ABPLNGVS` controls whether a developer may create Standard ABAP objects or only ABAP for Cloud Development objects. Use role template `SAP_BC_ABAP_DEVELOPER_5` as a starting point for an ABAP Cloud–only developer role.

### Stepwise transformation

The ABAP language version of individual objects in a classic software component can be switched to ABAP for Cloud Development:
- ABAP code objects (classes, interfaces): as of SAP S/4HANA release 2019
- DDIC, CDS and other objects: as of SAP S/4HANA release 2022

Run `ABAP_CLOUD_READINESS` beforehand to verify ABAP Cloud rules are respected.

## Decision Guide

### Choose Level A when
- ✅ A released API or extension point covers the requirement
- ✅ Building a new application or extension
- ✅ Cloud portability matters
- ✅ Key user extensibility or RAP-based developer extensibility suffices

### Choose Level B when
- ✅ No released API exists for the required functionality
- ✅ The UI must remain classic (SAP GUI, Web Dynpro)
- ✅ Extending an SEGW/BOPF/UI5 app or a GUI transaction
- ✅ Correcting or extending existing classic custom code
- ✅ A classic API (BAPI, ALV grid, non-released BAdI) is available and nominated

### Accept Level C only when
- ⚠️ No released or classic API covers the requirement
- ⚠️ You have wrapped the internal object and created a single ATC exemption
- ⚠️ You monitor the changelog for SAP objects for incompatible changes
- ⚠️ You have a plan to migrate once a higher-level API appears

### Never use Level D
- ❌ Modifications — use BAdIs instead
- ❌ Implicit/explicit enhancements — use BAdIs instead
- ❌ Direct write access to SAP tables — use released or classic APIs
- ❌ `noAPI` objects — use released or classic APIs, check successor info
- ❌ Critical ABAP statements
- ❌ Calls to SAP form routines
- ❌ SAP-internal-flagged BAdIs (exceptional cases only)

## Remediation Priority

Address findings in this order:

1. **Level D — eliminate entirely**
   - No modifications → use BAdIs
   - No implicit or explicit enhancements → use BAdIs
   - No direct write access to SAP DB tables → released or classic APIs
   - No not-recommended (`noAPI`) APIs → released or classic APIs
   - Remove critical ABAP statements → released or classic APIs
   - Do not call form routines in SAP programs → released or classic APIs

2. **Level C — minimize**
   - No direct read access to SAP tables → released or classic CDS views
   - Replace SAP internal APIs with released or classic APIs
   - If internal APIs are still needed, explore the changelog for SAP objects for incompatible changes
   - Wrap remaining internal objects and exempt once

3. **Level B — monitor**
   - Track deprecated API findings (priority 3) and adopt successors
   - Monitor when SAP releases an equivalent API, then migrate to Level A
   - Do not rewrite stable classic code without a reason

4. **Level A — sustain**
   - Enforce via `S_ABPLNGVS` authorization and separate software components
   - Keep the global ATC variant active in development and transport release

## Legacy code transformation options

| Option                          | When to apply                                                                    | Typical tasks                                                                                                     |
| ------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Retire unused code**          | ~60% of custom code in a typical ERP is not used productively                    | Collect usage data with `SUSG`/`SCMON` · analyze in Custom Code Migration app · remove/backup unused code · clone finder |
| **Renovate & innovate side-by-side** | Loosely coupled extensions better served by SAP Business AI Platform       | Analyze dependencies in Custom Code Migration app · transfer code to BTP · adapt via ATC quick fixes             |
| **Renovate & innovate on-stack**| Tightly coupled extensions/modifications worth reimplementing in ABAP Cloud      | Analyze complexity for TCO drivers · make code ABAP Cloud compliant · replace non-released objects with released APIs · use only released extension points |
| **Adapt**                       | None of the above is feasible — minimum viable action                            | Adapt via readiness ATC checks, Simplification Database and ADT quick fixes (up to ~60% automation) · SQL Monitor for performance · CDS/AMDP/ABAP SQL pushdown |

### Transition guidance by use case

| Category            | Existing use case                                    | Guidance                                                                             |
| ------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Extensions          | Custom field (append) on DB table or CDS view        | Migrate to released extension includes if available                                  |
| Extensions          | Implementation of an SAP BAdI                        | Check for a released BAdI and adapt the implementation to ABAP Cloud                 |
| Extensions          | Extension of an SAP Fiori app (SEGW, BOPF, UI5)      | Migrate the extension (or parts) to the newly delivered RAP application if available |
| Extensions          | Implementation of user exit (e.g., `SAPMV45A`)       | Analyze with ATC clean core checks; adopt released and classic APIs where possible   |
| Extensions          | Existing modifications                               | Check whether a released or classic BAdI can replace the modification                |
| Extensions          | Existing enhancement implementation (implicit/explicit) | Check whether a released or classic BAdI can replace it                           |
| Custom applications | Existing custom SAP Fiori app (SEGW, BOPF, UI5)      | Analyze with ATC clean core checks; adopt released and classic APIs                  |
| Custom applications | Classic ABAP reports (with or without ALV)           | Analyze with ATC clean core checks; adopt released and classic APIs                  |
| Custom applications | Dynpro, BSP or Web Dynpro applications               | Analyze with ATC clean core checks; adopt released and classic APIs                  |
| Data access         | Database access to SAP tables                        | Replace with released or classic APIs                                                |
| Data access         | Usage of not-recommended or SAP internal APIs        | Replace with released or classic APIs                                                |

## Classic extension techniques — level guidance

| Technique                       | Level | Guidance                                                                                          |
| ------------------------------- | ----- | ------------------------------------------------------------------------------------------------- |
| **Released BAdI**               | A     | Preferred extension point                                                                         |
| **Non-released BAdI**           | B     | Good choice for classic extensions even when not released for cloud development                   |
| **SAP-internal-flagged BAdI**   | D     | Exceptional cases only                                                                            |
| **User exits** (VOFM, SAPMV45A) | B     | Predefined SAP coding parts are stable and typically survive upgrades; technically a modification |
| **Customer exits** (SMOD/CMOD)  | B     | Predecessor of BAdIs; use only where no BAdI exists — likely to be replaced in future releases    |
| **Explicit enhancement spots**  | B/D   | Exceptional cases only, to include custom BAdIs. Do not place extension code directly in the spot |
| **Implicit enhancement spots**  | D     | Similar to modifications — do not use                                                             |
| **Modifications**               | D     | Avoid completely. If unavoidable, use the modification assistant and govern via ATC               |
| **DDIC appends**                | B/C   | Append fields via CI includes or extension includes (EEW). Released include → A, else B/C         |
| **CDS extends / metadata extensions** | A/B | Use CDS extends and CDS metadata extensions instead of modifying SAP CDS views                 |
| **OData redefinition**          | B     | Redefine OData services rather than modifying them                                                |
| **Domain value appends, search help appends/exits** | B | Acceptable classic extension techniques                                          |

A general rule for all related objects: **no modifications to the corresponding SAP objects**.

## SAP Cloud ERP Private vs. SAP Cloud ERP (public)

| Aspect                          | SAP Cloud ERP (public)                  | SAP Cloud ERP Private                                                     |
| ------------------------------- | --------------------------------------- | ------------------------------------------------------------------------- |
| **Allowed levels**              | Level A only                            | Levels A–D technically possible; A preferred, D to be remediated          |
| **Language versions**           | ABAP for Cloud Development              | ABAP for Cloud Development and Standard ABAP                              |
| **Non-released API usage**      | Not possible                            | Possible (Level B/C)                                                      |
| **Dynpro extension**            | Not possible                            | Possible (Level B)                                                        |
| **IAM / Communication Mgmt**    | Fiori apps, strict SAP/customer content separation | Classic transactions (`PFCG`, `SM59`, `SOAMANAGER`); no strict separation; IAM/COM Fiori apps unavailable |
| **Functional scope**            | Narrower, fully released                | Broader, largely not covered by released APIs                             |

## Partner add-ons and clean core

- Partner extensions can be certified via the SAP Integration and Certification Center (SAP ICC) open certification program for clean core extensibility criteria, earning the designation **SAP-certified for clean core with SAP S/4HANA Cloud**
- Existing SAP Solution Extensions with add-ons on SAP Cloud ERP Private have been validated by SAP with the respective partners for clean core compliance
- Partners can offer clean core APIs: Level A APIs ship with the corresponding extension; classic APIs (Level B) can be offered under partner responsibility as part of the Cloudification Repository
- Partners generate partner JSON files with report `SYCM_API_CLASSIFICATION_MANAGR`; each namespace needs its own file `objectClassifications_NAMESPACE.json`

## Migration from 3-tier terminology

| Former 3-tier term                            | Clean core level equivalent                                                            |
| --------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Tier 1** — Key user extensibility           | **Level A** (key user extensibility using released extension points)                   |
| **Tier 2** — Developer extensibility (ABAP Cloud) | **Level A** (on-stack ABAP Cloud development with released APIs)                   |
| **Tier 3** — Classic extensibility            | **Level B** where classic APIs are used · **Level C** for internal objects · **Level D** for not-recommended patterns |
| "Tier 2 wrapper for Tier 1 consumption"       | Wrapper in a classic ABAP component released for ABAP Cloud — **Level B** if wrapping a classic API, **Level C** if wrapping an internal object |

The key improvement: former "Tier 3" is no longer a single undifferentiated bucket. Classic API usage (Level B) is now recognized as upgrade-stable, while genuinely risky patterns are isolated as Level D.

## References

- Clean Core Extensibility Whitepaper — the authoritative source for the level concept
- Extend SAP S/4HANA in the cloud and on premise with ABAP based extensions (Version 2.3, August 2025)
- SAP Cloudification Repository: https://github.com/SAP/abap-atc-cr-cv-s4hc
- Cloudification Repository Viewer: https://sap.github.io/abap-atc-cr-cv-s4hc/
- SAP Business Accelerator Hub: https://api.sap.com/
- SAP Note 3578329 — classification of classic technologies and frameworks
- SAP Note 3565942 — clean core ATC checks (`SYCM_USAGE_OF_APIS`, `SYCM_ALLOWED_ENH_TECHNOLOGY`)
- Certification of Partner Solutions following Clean Core (SAP ICC)
