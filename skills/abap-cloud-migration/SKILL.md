---
name: abap-cloud-migration
description: Help with migrating classic ABAP custom code to ABAP Cloud including custom code adaptation, identifying unreleased API replacements, generating wrapper classes for unreleased objects, ATC Cloud Readiness checks, handling incompatible language constructs, and step-by-step migration workflows. Use when users ask about migrating to ABAP Cloud, custom code migration, cloud readiness, unreleased API replacement, wrapper pattern, ATC cloud checks, code adaptation, classic to cloud migration, S/4HANA cloud migration, or clean core compliance. Triggers include "migrate to ABAP Cloud", "cloud readiness check", "unreleased API", "replace with released API", "custom code adaptation", "wrapper for unreleased", "ATC cloud", "clean core migration", "move to tier 1", or "ABAP Cloud compatibility".
---

# ABAP Cloud Migration Patterns

Guide for systematically migrating classic ABAP custom code to ABAP Cloud (Tier 1) compliance.

## Workflow

1. **Assess current state**: Run ATC Cloud Readiness checks on existing code
2. **Categorize findings**: Group by finding type (unreleased API, language construct, etc.)
3. **Plan migration**: Prioritize by impact and determine replacement strategy
4. **Implement replacements**: Apply released API replacements or create wrappers
5. **Validate**: Re-run ATC checks and test functionality

## Migration Assessment

### Running ATC Cloud Readiness Checks

1. In ADT: Right-click package → **Run As** → **ABAP Test Cockpit**
2. Use check variant `ABAP_CLOUD_READINESS` or a custom variant with cloud-relevant checks
3. Review findings in the ATC Results view

### Key ATC Check Messages

| Message ID | Description                           | Action                            |
| ---------- | ------------------------------------- | --------------------------------- |
| `NROB`     | Use of unreleased number range API    | Use `CL_NUMBERRANGE_RUNTIME`      |
| `BAPI`     | Direct BAPI call                      | Use released RAP API or wrapper   |
| `DYNP`     | Dynpro/screen usage                   | Replace with Fiori/UI5            |
| `FUGR`     | Unreleased function module call       | Find released replacement or wrap |
| `CLAS`     | Unreleased class usage                | Find released replacement or wrap |
| `TABL`     | Direct DB table access (not released) | Use released CDS view entity      |
| `LANG`     | Incompatible language construct       | Refactor to use modern ABAP       |

## Common API Replacements

### Database Access

| Classic Pattern           | ABAP Cloud Replacement        |
| ------------------------- | ----------------------------- |
| `SELECT FROM mara`        | `SELECT FROM i_product`       |
| `SELECT FROM bkpf / bseg` | `SELECT FROM i_journalentry`  |
| `SELECT FROM vbak / vbap` | `SELECT FROM i_salesorder`    |
| `SELECT FROM ekko / ekpo` | `SELECT FROM i_purchaseorder` |
| `SELECT FROM kna1`        | `SELECT FROM i_customer`      |
| `SELECT FROM lfa1`        | `SELECT FROM i_supplier`      |
| `SELECT FROM t001`        | `SELECT FROM i_companycode`   |
| Direct table access       | Use `I_*` released CDS views  |

### Function Modules → Released Classes

| Classic FM                              | Released Replacement                                 |
| --------------------------------------- | ---------------------------------------------------- |
| `GUID_CREATE`                           | `cl_system_uuid=>create_uuid_x16_static( )`          |
| `CONVERSION_EXIT_ALPHA_INPUT`           | `cl_abap_format=>alpha_input( )`                     |
| `CONVERSION_EXIT_ALPHA_OUTPUT`          | `cl_abap_format=>alpha_output( )`                    |
| `POPUP_TO_CONFIRM`                      | Not available — use Fiori UI                         |
| `NUMBER_GET_NEXT`                       | `cl_numberrange_runtime=>number_get( )`              |
| `BAPI_TRANSACTION_COMMIT`               | Handled by RAP framework (no explicit commit)        |
| `SO_NEW_DOCUMENT_ATT_SEND_API1`         | `cl_bcs_mail_message` (send emails)                  |
| `READ_TEXT` / `SAVE_TEXT`               | Not released — wrap or use custom persistence        |
| `JOB_OPEN` / `JOB_CLOSE` / `JOB_SUBMIT` | `cl_apj_rt_api` (Application Jobs)                   |
| `ENQUEUE_*` / `DEQUEUE_*`               | RAP draft / managed locking or `CL_ABAP_LOCK_OBJECT` |

### Language Constructs

| Incompatible Construct                   | Cloud-Compatible Alternative                   |
| ---------------------------------------- | ---------------------------------------------- |
| `CALL TRANSACTION`                       | Not available — use API or RAP                 |
| `SUBMIT ... AND RETURN`                  | Not available — use Application Jobs           |
| `WRITE` / `SKIP` / `ULINE` (list output) | Not available — use Fiori UI for output        |
| `CALL SCREEN` / `CALL SELECTION-SCREEN`  | Not available — use Fiori/UI5                  |
| `MESSAGE ... RAISING`                    | `RAISE EXCEPTION TYPE ...`                     |
| `CALL FUNCTION ... IN UPDATE TASK`       | RAP saver class / managed save                 |
| `EXEC SQL` (Native SQL)                  | ABAP SQL or AMDP                               |
| `GENERATE SUBROUTINE POOL`               | Not available — use strategy/factory pattern   |
| `DESCRIBE FIELD ... TYPE`                | RTTI: `cl_abap_typedescr=>describe_by_data( )` |
| `GET/SET PARAMETER ID`                   | Not available — use method parameters          |

## Wrapper Pattern

When no released API exists, create a wrapper class in Tier 2 (classic ABAP) and release it for Tier 1 consumption.

### Step 1: Create Wrapper Interface (Tier 2, released for Cloud)

```abap
"Released for use in ABAP Cloud (C1 contract)
INTERFACE zif_text_handler
  PUBLIC.
  METHODS read_text
    IMPORTING iv_id          TYPE thead-tdid
              iv_name        TYPE thead-tdname
              iv_object      TYPE thead-tdobject
              iv_language    TYPE sy-langu DEFAULT sy-langu
    RETURNING VALUE(rt_text) TYPE tline_tab
    RAISING   zcx_text_error.

  METHODS save_text
    IMPORTING iv_id       TYPE thead-tdid
              iv_name     TYPE thead-tdname
              iv_object   TYPE thead-tdobject
              iv_language TYPE sy-langu DEFAULT sy-langu
              it_text     TYPE tline_tab
    RAISING   zcx_text_error.
ENDINTERFACE.
```

### Step 2: Create Wrapper Class (Tier 2, released for Cloud)

```abap
"Implementation uses unreleased FMs internally
"Released for use in ABAP Cloud (C1 contract)
CLASS zcl_text_handler DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_text_handler.
ENDCLASS.

CLASS zcl_text_handler IMPLEMENTATION.
  METHOD zif_text_handler~read_text.
    "Uses unreleased FM internally — OK in Tier 2
    CALL FUNCTION 'READ_TEXT'
      EXPORTING
        id       = iv_id
        name     = iv_name
        object   = iv_object
        language = iv_language
      TABLES
        lines    = rt_text
      EXCEPTIONS
        OTHERS   = 1.
    IF sy-subrc <> 0.
      RAISE EXCEPTION TYPE zcx_text_error.
    ENDIF.
  ENDMETHOD.

  METHOD zif_text_handler~save_text.
    DATA ls_header TYPE thead.
    ls_header-tdid     = iv_id.
    ls_header-tdname   = iv_name.
    ls_header-tdobject = iv_object.
    ls_header-tdspras  = iv_language.

    CALL FUNCTION 'SAVE_TEXT'
      EXPORTING header = ls_header
      TABLES    lines  = it_text
      EXCEPTIONS OTHERS = 1.
    IF sy-subrc <> 0.
      RAISE EXCEPTION TYPE zcx_text_error.
    ENDIF.
  ENDMETHOD.
ENDCLASS.
```

### Step 3: Release the Wrapper

In ADT, open the wrapper class properties:

1. Go to **API State** tab
2. Add **Use System-Internally (C1)** contract
3. Set visibility to **Use in ABAP Cloud**

### Step 4: Use in Tier 1 Code

```abap
"Tier 1 (ABAP Cloud) code — uses released wrapper
DATA(lo_text) = NEW zcl_text_handler( ).
DATA(lt_text) = lo_text->zif_text_handler~read_text(
  iv_id     = 'ST'
  iv_name   = lv_doc_name
  iv_object = 'VBBK' ).
```

## Migration Strategy by Object Type

### Reports / Programs

```
Classic Report → Application Job class + CDS view + Fiori app
1. Extract data logic → CDS view entities
2. Extract business logic → ABAP Cloud class
3. Create Application Job catalog entry (CL_APJ_DT_CREATE_CONTENT)
4. Schedule via Fiori app "Application Jobs"
```

### Dynpro Transactions

```
Dynpro Transaction → RAP BO + Fiori Elements app
1. Identify CRUD operations → RAP behavior definition
2. Map screen fields → CDS view entity
3. Create service definition/binding
4. Generate Fiori Elements app
```

### BAPIs

```
BAPI → RAP BO with custom actions
1. Map BAPI parameters → CDS abstract entities
2. Implement as RAP actions or factory actions
3. Expose via OData service binding
```

### RFC Function Modules

```
RFC FM → Released API class or RAP service
1. If simple logic → Released ABAP class
2. If CRUD → RAP BO with service binding
3. If complex → Wrapper class (Tier 2)
```

## Finding Released Replacements

### In ADT

1. **Released Object Search**: `Ctrl+Shift+A` → Filter by "Released" APIs
2. **API State Filter**: In Project Explorer, filter by C1 release state
3. **ABAP Element Info**: Hover over unreleased object → see suggestion if available

### Using the Released Objects App

Fiori app **Released Objects** (`F5865`):

- Search by classic object name
- Filter by release state (C1, C2)
- View successor information

### Programmatic Check

```abap
"Check if an object is released for ABAP Cloud
SELECT SINGLE *
  FROM i_apistateofrepositoryobject
  WHERE ObjectType     = 'CLAS'
    AND ObjectName     = 'CL_NUMBERRANGE_RUNTIME'
    AND ReleaseState   = 'RELEASED'
  INTO @DATA(ls_state).
```

## Step-by-Step Migration Checklist

1. [ ] Run ATC Cloud Readiness check on the package/objects
2. [ ] Export findings and categorize by type
3. [ ] For each unreleased API usage:
   - [ ] Search for released replacement (CDS view `I_ApiStateOfRepositoryObject`)
   - [ ] If found: replace directly
   - [ ] If not found: create Tier 2 wrapper
4. [ ] For each incompatible language construct:
   - [ ] Refactor to cloud-compatible alternative
5. [ ] For Dynpro/ALV/list-based UIs:
   - [ ] Plan Fiori replacement (separate project)
6. [ ] Move migrated objects to ABAP Cloud language version package
7. [ ] Re-run ATC checks — all findings must be resolved
8. [ ] Execute regression tests

## Output Format

When helping with migration topics, structure responses as:

```markdown
## Migration Guidance

### Current Code Analysis

- Unreleased APIs found: [list]
- Incompatible constructs: [list]
- Estimated effort: [low / medium / high]

### Replacement Strategy

[For each finding: original → replacement with code]

### Wrapper Requirements

[Objects needing Tier 2 wrappers]
```

## References

- Custom Code Migration Guide: https://help.sap.com/docs/abap-cloud/abap-development-tools-user-guide/custom-code-migration
- ABAP Cloud API Release Info: https://help.sap.com/docs/abap-cloud/abap-rap/released-abap-objects
- Wrapper Pattern: https://github.com/SAP-samples/abap-cheat-sheets/blob/main/19_ABAP_Cloud.md
- ATC Cloud Readiness: https://help.sap.com/docs/abap-cloud/abap-development-tools-user-guide/checking-abap-cloud-readiness
