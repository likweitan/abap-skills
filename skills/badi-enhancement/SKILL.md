---
name: badi-enhancement
description: Help with BAdI (Business Add-In) development and the ABAP enhancement framework including new BAdIs, fallback classes, filter-based BAdIs, enhancement spots, enhancement implementations, key user extensibility, classic BAdIs, and the new enhancement framework. Use when users ask about BAdI, BAdIs, Business Add-In, enhancement spot, enhancement implementation, enhancement framework, BAdI filter, BAdI fallback, BAdI definition, BAdI implementation, key user extensibility, custom logic injection, enhancement point, implicit enhancement, explicit enhancement, or extending SAP standard code. Triggers include "create a BAdI", "implement a BAdI", "enhancement spot", "find a BAdI", "BAdI filter", "fallback class", "key user extensibility", "extend standard", or "enhancement framework".
---

# BAdI & Enhancement Framework

Guide for using BAdIs (Business Add-Ins) and the ABAP enhancement framework to extend SAP standard functionality.

## Workflow

1. **Determine the user's goal**:
   - Finding an existing BAdI to implement
   - Creating a custom BAdI definition
   - Implementing a BAdI
   - Understanding classic vs. new enhancement framework
   - Using key user extensibility
   - Extending standard code via enhancement spots

2. **Identify the framework**:
   - New BAdI framework (preferred, ABAP Cloud compatible)
   - Classic BAdI framework (legacy, `SE18`/`SE19`)
   - Enhancement spots and implementations
   - Key user extensibility (no-code)

3. **Guide implementation** following best practices

## BAdI Framework Overview

### New vs. Classic BAdIs

| Aspect               | New BAdI Framework              | Classic BAdI Framework |
| -------------------- | ------------------------------- | ---------------------- |
| **Transactions**     | ADT or `SE18`/`SE19`            | `SE18`/`SE19`          |
| **Enhancement Spot** | Required container              | Not applicable         |
| **Multiple Use**     | Always multiple-use             | Configurable           |
| **Filter**           | Filter types supported          | Filter values          |
| **Fallback Class**   | Supported                       | Not available          |
| **ABAP Cloud**       | Supported (released BAdIs only) | Not available          |
| **Recommendation**   | Use for all new development     | Maintain existing only |

## Creating a Custom BAdI

### Step 1: Create Enhancement Spot

```
ADT: New → Other ABAP Repository Object → Enhancements → Enhancement Spot
Name: Z_ENH_SPOT_TRAVEL
```

### Step 2: Define the BAdI Interface

```abap
INTERFACE zif_badi_travel_validate
  PUBLIC.
  METHODS validate
    IMPORTING
      is_travel       TYPE zstravel
    CHANGING
      ct_messages     TYPE bapiret2_t
    RAISING
      cx_badi_not_implemented.
ENDINTERFACE.
```

### Step 3: Define the BAdI in Enhancement Spot

In the enhancement spot, add a BAdI definition:

| Property           | Value                                 |
| ------------------ | ------------------------------------- |
| **BAdI Name**      | `ZBADI_TRAVEL_VALIDATE`               |
| **Interface**      | `ZIF_BADI_TRAVEL_VALIDATE`            |
| **Multiple Use**   | Yes (allows multiple implementations) |
| **Fallback Class** | `ZCL_BADI_TRAVEL_FALLBACK` (optional) |

### Step 4: Create Fallback Class (Optional)

```abap
CLASS zcl_badi_travel_fallback DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_badi_travel_validate.
ENDCLASS.

CLASS zcl_badi_travel_fallback IMPLEMENTATION.
  METHOD zif_badi_travel_validate~validate.
    "Default behavior when no implementation is active
  ENDMETHOD.
ENDCLASS.
```

### Step 5: Call the BAdI in Your Code

```abap
"Get BAdI handle
DATA lo_badi TYPE REF TO zif_badi_travel_validate.

GET BADI lo_badi.

"Call BAdI — loops through all active implementations
CALL BADI lo_badi->validate
  EXPORTING is_travel   = ls_travel
  CHANGING  ct_messages = lt_messages.
```

### With Filters

```abap
"Define BAdI with filter
"In Enhancement Spot: add filter type COUNTRY (type LAND1)

"Get BAdI with filter
GET BADI lo_badi
  FILTERS country = ls_travel-country.

CALL BADI lo_badi->validate
  EXPORTING is_travel   = ls_travel
  CHANGING  ct_messages = lt_messages.
```

## Implementing an Existing BAdI

### Step 1: Find the BAdI

Methods to find a BAdI:

- **ADT search**: Search for BAdI name or enhancement spot
- **Transaction `SE18`**: Browse BAdI definitions
- **Breakpoint on `GET BADI`**: Set breakpoint at `CL_BADI_INTERNAL_FACTORY=>GET_BADI` to find BAdIs called during a process
- **Documentation**: Check SAP documentation or community for BAdI names

### Step 2: Create Enhancement Implementation

```
ADT: New → Other ABAP Repository Object → Enhancements → Enhancement Implementation
Name: Z_ENH_IMPL_TRAVEL_CHECK
Enhancement Spot: Z_ENH_SPOT_TRAVEL (or SAP's spot)
```

### Step 3: Create BAdI Implementation Class

```abap
CLASS zcl_badi_impl_travel_check DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_badi_travel_validate.
ENDCLASS.

CLASS zcl_badi_impl_travel_check IMPLEMENTATION.
  METHOD zif_badi_travel_validate~validate.
    "Custom validation logic
    IF is_travel-begin_date < cl_abap_context_info=>get_system_date( ).
      APPEND VALUE #(
        type       = 'E'
        id         = 'Z_TRAVEL'
        number     = '001'
        message_v1 = 'Travel begin date must be in the future'
      ) TO ct_messages.
    ENDIF.
  ENDMETHOD.
ENDCLASS.
```

## BAdIs in ABAP Cloud / RAP

In ABAP for Cloud Development, BAdIs follow a specific pattern:

### Released BAdIs

- Only SAP-released BAdIs can be implemented
- Search for released BAdIs in ADT: `api:badi`
- Common in RAP scenarios for extending standard RAP BOs

### RAP BAdI Pattern

```abap
"BAdI for extending SAP Fiori apps / RAP BOs
"Implement the released BAdI interface
CLASS zcl_my_rap_badi DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_some_released_badi.
ENDCLASS.

CLASS zcl_my_rap_badi IMPLEMENTATION.
  METHOD if_some_released_badi~some_method.
    "Custom logic
  ENDMETHOD.
ENDCLASS.
```

### Dynamic BAdI Calls

```abap
"Dynamic GET BADI with BAdI name in variable
DATA lo_badi TYPE REF TO cl_badi_base.
DATA(lv_badi_name) = 'ZBADI_MY_BADI'.

GET BADI lo_badi TYPE (lv_badi_name).

"Dynamic CALL BADI with method name in variable
CALL BADI lo_badi->('VALIDATE')
  EXPORTING is_data = ls_data.
```

## Enhancement Spots and Implementations

Beyond BAdIs, the enhancement framework supports:

### Explicit Enhancement Points

SAP defines explicit points in standard code where custom logic can be inserted:

```abap
"In SAP standard code:
ENHANCEMENT-POINT z_enh_point SPOTS z_enh_spot.

"In your enhancement implementation:
ENHANCEMENT z_my_enhancement.
  "Your custom code here
  IF lv_condition = abap_true.
    "Custom logic
  ENDIF.
ENDENHANCEMENT.
```

### Explicit Enhancement Sections

```abap
"SAP code with replaceable section:
ENHANCEMENT-SECTION z_section SPOTS z_enh_spot.
  "Default code (can be replaced)
  lv_result = lv_a + lv_b.
END-ENHANCEMENT-SECTION.

"Your replacement:
ENHANCEMENT z_my_section_impl.
  "Custom replacement code
  lv_result = lv_a * lv_b.
ENDENHANCEMENT.
```

## Key User Extensibility

No-code/low-code extension capabilities available via SAP Fiori:

| Capability                    | Description                                 |
| ----------------------------- | ------------------------------------------- |
| **Custom Fields**             | Add fields to standard business objects     |
| **Custom Logic**              | Add validation/determination logic via BRF+ |
| **Custom CDS Views**          | Create simple analytical views              |
| **Custom Business Objects**   | Create simple transactional objects         |
| **Custom Analytical Queries** | Build queries on existing CDS views         |

## Best Practices

1. **Prefer new BAdI framework** over classic BAdIs
2. **Use filters** to scope implementations to specific contexts
3. **Implement fallback classes** for default behavior
4. **Keep implementations focused** — one concern per implementation
5. **Document the BAdI** with clear interface documentation
6. **Test implementations** independently using ABAP Unit
7. **In ABAP Cloud**, only implement released BAdIs

## Output Format

When helping with BAdI/enhancement topics, structure responses as:

```markdown
## BAdI / Enhancement Guidance

### Framework

- Type: [New BAdI / Classic BAdI / Enhancement Spot / Key User]
- Context: [ABAP Cloud / Standard ABAP]

### Implementation

[Step-by-step with code examples]

### Testing

[How to verify the enhancement works]
```

## References

- BAdI Cheat Sheet: https://github.com/SAP-samples/abap-cheat-sheets/blob/main/35_BAdIs.md
- Enhancement Framework: https://help.sap.com/docs/abap-cloud/abap-development-tools-user-guide/enhancement
- Key User Extensibility: https://help.sap.com/docs/sap-s4hana-cloud/extensibility
