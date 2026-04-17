---
name: abap-cloud
description: Help with ABAP Cloud development including the 3-tier extensibility model, ABAP Cloud language version restrictions, wrapper patterns for unreleased APIs, clean core principles, and key user vs developer extensibility. Use when users ask about ABAP Cloud, ABAP for Cloud Development, clean core, 3-tier model, tier 1 tier 2 tier 3, wrapper pattern, released APIs, language version, restricted ABAP, embedded Steampunk, developer extensibility, key user extensibility, or ABAP Cloud readiness. Triggers include "ABAP Cloud restrictions", "clean core", "wrapper class", "tier model", "released API alternative", "ABAP language version", "Steampunk", or "extensibility model".
---

# ABAP Cloud / Clean Core

Guide for developing with the ABAP Cloud programming model, understanding the 3-tier extensibility model, and applying clean core principles.

## Workflow

1. **Determine the user's context**:
   - Understanding ABAP Cloud concepts and restrictions
   - Choosing the right extensibility tier
   - Wrapping unreleased APIs for use in ABAP Cloud
   - Identifying released API alternatives
   - Setting up clean core-compliant development

2. **Identify the extensibility tier**:
   - Tier 1: Key user extensibility (no code)
   - Tier 2: Developer extensibility (ABAP Cloud / ABAP for Cloud Development)
   - Tier 3: Classic extensibility (standard ABAP, only on-premise/private cloud)

3. **Guide implementation** using clean core principles

## ABAP Language Versions

| Language Version               | Scope                                                         | Available In                                       |
| ------------------------------ | ------------------------------------------------------------- | -------------------------------------------------- |
| **ABAP for Cloud Development** | Only released APIs and objects; restricted syntax; no SAP GUI | BTP ABAP Environment, S/4HANA (embedded Steampunk) |
| **Standard ABAP**              | Full ABAP syntax; all repository objects accessible           | On-premise, private cloud                          |

### Key Restrictions in ABAP for Cloud Development

- Only released SAP APIs (C1 contract) can be used
- No direct database table access for SAP tables (use released CDS views instead)
- No classic dynpro, selection screens, or SAP GUI-dependent statements
- No `CALL TRANSACTION`, `SUBMIT`, `AUTHORITY-CHECK` (use `CL_ABAP_AUTHORIZATION` instead)
- No classic BAdIs or user exits
- No `EXEC SQL` or native SQL (use ABAP SQL or AMDP)
- No function modules (except released RFC-enabled ones)
- No `INCLUDE` programs
- No `WRITE` or classic list output
- Must use `if_oo_adt_classrun` for console output

## 3-Tier Extensibility Model

### Tier 1 — Key User Extensibility (No Code)

- Custom fields and logic via SAP Fiori UIs
- Custom CDS views (basic)
- Custom business objects (simple)
- Custom analytical queries
- No ABAP development required

### Tier 2 — Developer Extensibility (ABAP Cloud)

- ABAP for Cloud Development language version
- Only released APIs with stability contracts
- RAP-based business objects
- Side-by-side or embedded development
- Full lifecycle management via ADT

```abap
"Example: Tier 2 class using only released APIs
CLASS zcl_my_extension DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_oo_adt_classrun.
ENDCLASS.

CLASS zcl_my_extension IMPLEMENTATION.
  METHOD if_oo_adt_classrun~main.
    "Only released CDS views — no direct table access
    SELECT FROM I_BusinessPartner
      FIELDS BusinessPartner, BusinessPartnerName
      INTO TABLE @DATA(partners)
      UP TO 10 ROWS.
    out->write( partners ).
  ENDMETHOD.
ENDCLASS.
```

### Tier 3 — Classic Extensibility (Standard ABAP)

- Full ABAP language scope
- Access to all repository objects
- Classic enhancement points, BAdIs, user exits
- Only available on-premise or private cloud
- Not recommended for new cloud-ready development

## Wrapper Pattern

When a needed API is not released (Level B/C), create a wrapper in Tier 3 that exposes the functionality via a released interface consumable from Tier 2.

### Wrapper Class Pattern

```abap
"Tier 3: Wrapper class (Standard ABAP language version)
"Released with C1 contract for use from Tier 2
CLASS zcl_wrapper_material DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_material_reader.
    "Set as released API with C1 contract in ADT
ENDCLASS.

CLASS zcl_wrapper_material IMPLEMENTATION.
  METHOD zif_material_reader~get_material.
    "Access unreleased API internally
    SELECT SINGLE * FROM mara
      WHERE matnr = @iv_matnr
      INTO @DATA(ls_mara).
    "Map to released structure
    rs_material = VALUE #(
      matnr = ls_mara-matnr
      mtart = ls_mara-mtart
      matkl = ls_mara-matkl ).
  ENDMETHOD.
ENDCLASS.
```

### Wrapper via RFC Proxy (Remote Tier 2 to Tier 3)

```abap
"Tier 2 consumer calls released RFC wrapper
DATA(lo_dest) = cl_rfc_destination_provider=>create_by_comm_arrangement(
  comm_scenario  = 'Z_MY_COMM_SCENARIO'
  service_id     = 'Z_MY_OUTBOUND_SRV' ).

CALL FUNCTION 'Z_WRAPPER_FM'
  DESTINATION lo_dest->get_destination_name( )
  EXPORTING iv_param = lv_value
  IMPORTING ev_result = lv_result.
```

## Released API Discovery

| Method                          | Description                                                   |
| ------------------------------- | ------------------------------------------------------------- |
| **ADT: Released Object Search** | In ADT, search with `api:` prefix (e.g., `api:cl_*`)          |
| **Cloudification API Viewer**   | Browse at https://sap.github.io/abap-atc-cr-cv-s4hc/          |
| **ATC Cloud Readiness Check**   | Run ATC checks to identify unreleased API usage               |
| **Released ABAP Classes skill** | Use `released-abap-classes` skill for common released classes |
| **XCO Library**                 | `XCO_CP_*` classes provide cloud-ready alternatives           |

## Common Unreleased → Released Replacements

| Unreleased (Classic)        | Released Alternative (ABAP Cloud)                 |
| --------------------------- | ------------------------------------------------- |
| `AUTHORITY-CHECK`           | `CL_ABAP_AUTHORIZATION=>check_authorization()`    |
| `sy-uname`                  | `cl_abap_context_info=>get_user_technical_name()` |
| `sy-datum` / `sy-uzeit`     | `cl_abap_context_info=>get_system_date/time()`    |
| `cl_gui_frontend_services`  | Not available — use Fiori UI instead              |
| `CALL TRANSACTION`          | RAP action or Fiori navigation                    |
| `SUBMIT ... AND RETURN`     | Background job via `CL_APJ_RT_API`                |
| Direct SAP table `SELECT`   | Use released CDS view (I\_\* views)               |
| `CONVERSION_EXIT_*`         | `CL_ABAP_CONV_CODEPAGE`, domain fixed values      |
| `BAPI_*` function modules   | Released APIs or RAP BO consumption               |
| Classic `MESSAGE` statement | RAP messages via `REPORTED`                       |

## Output Format

When helping with ABAP Cloud / clean core topics, structure responses as:

```markdown
## ABAP Cloud Guidance

### Context

- Extensibility tier: [Tier 1/2/3]
- Language version: [ABAP for Cloud Development / Standard ABAP]
- Target platform: [BTP / S/4HANA embedded / on-premise]

### Recommendation

[Guidance on the approach]

### Code Example

[ABAP code following clean core principles]

### Released API References

- [List of relevant released APIs used]
```

## References

- SAP Cloudification Repository: https://github.com/SAP/abap-atc-cr-cv-s4hc
- ABAP Cloud Cheat Sheet: https://github.com/SAP-samples/abap-cheat-sheets
- Clean Core Guidelines: https://help.sap.com/docs/abap-cloud
