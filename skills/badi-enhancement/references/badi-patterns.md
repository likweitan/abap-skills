# BAdI Enhancement Patterns Reference

Common BAdI implementation patterns and best practices for ABAP Cloud and SAP Cloud ERP Private systems.

## Clean core level quick reference

| Technique                          | Level | Notes                                                        |
| ---------------------------------- | ----- | ------------------------------------------------------------ |
| Released BAdI                      | **A** | Preferred code-based extension point                         |
| Key user extensibility             | **A** | Start here for tightly coupled extensions                    |
| Non-released BAdI                  | **B** | Acceptable in classic ABAP; monitor for release              |
| User exits (VOFM, `SAPMV45A`)       | **B** | Stable across upgrades; technically a modification           |
| Customer exits (SMOD/CMOD)         | **B** | Only where no BAdI exists                                    |
| Explicit enhancement spot          | **B/D** | Exceptional cases only, to host a custom BAdI              |
| Implicit enhancement               | **D** | **Do not use** — ATC priority 1                              |
| Source code plug-in                | **D** | **Do not use** — ATC priority 1                              |
| SAP-internal-flagged BAdI          | **D** | Exceptional cases only                                       |
| Modification                       | **D** | Avoid completely                                             |

BAdIs are the **only** enhancement technology recommended under the clean core level concept. `SYCM_ALLOWED_ENH_TECHNOLOGY` flags any other `ENHO` technology as a priority 1 (Level D) finding.

## Basic BAdI Implementation Pattern

### Standard BAdI Structure
```abap
"1. Define BAdI Interface
INTERFACE zif_badi_process
  PUBLIC.
  METHODS process
    IMPORTING
      iv_input       TYPE string
    CHANGING
      cv_output      TYPE string
    RAISING
      cx_badi_not_implemented.
ENDINTERFACE.

"2. Define BAdI in Enhancement Spot
"Properties:
"- BAdI Name: ZBADI_PROCESS
"- Interface: ZIF_BADI_PROCESS
"- Multiple Use: Yes
"- Fallback Class: ZCL_BADI_PROCESS_FALLBACK (optional)

"3. Call BAdI in production code
DATA lo_badi TYPE REF TO zif_badi_process.
GET BADI lo_badi.
CALL BADI lo_badi->process
  EXPORTING iv_input = lv_input
  CHANGING  cv_output = lv_output.

"4. Implement BAdI
CLASS zcl_badi_impl_process DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_badi_process.
ENDCLASS.

CLASS zcl_badi_impl_process IMPLEMENTATION.
  METHOD zif_badi_process~process.
    "Custom implementation
    cv_output = |Processed: { iv_input }|.
  ENDMETHOD.
ENDCLASS.
```

## Filter-Based BAdI Patterns

### Pattern 1: Country-Specific Processing
```abap
"BAdI Definition with Filter
"Filter Type: COUNTRY (LAND1)

"Implementation
DATA lo_badi TYPE REF TO zif_badi_country_process.
GET BADI lo_badi
  FILTERS country = lv_country_code.

CALL BADI lo_badi->process
  EXPORTING iv_data = ls_data
  IMPORTING ev_result = lv_result.
```

### Pattern 2: Company Code Filtering
```abap
"BAdI Definition with Filter
"Filter Type: BUKRS (BUKRS)

"Implementation
GET BADI lo_badi
  FILTERS company_code = lv_bukrs.
```

### Pattern 3: Document Type Filtering
```abap
"BAdI Definition with Filter
"Filter Type: CHAR4 (custom)

"Implementation
GET BADI lo_badi
  FILTERS doc_type = ls_document-doc_type.
```

## Fallback Class Patterns

### Pattern 1: Default Behavior
```abap
CLASS zcl_badi_fallback DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_badi_process.
ENDCLASS.

CLASS zcl_badi_fallback IMPLEMENTATION.
  METHOD zif_badi_process~process.
    "Default implementation when no active BAdI implementation exists
    cv_output = |Default processing: { iv_input }|.
  ENDMETHOD.
ENDCLASS.
```

### Pattern 2: Null Object Pattern
```abap
CLASS zcl_badi_null_fallback DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_badi_process.
ENDCLASS.

CLASS zcl_badi_null_fallback IMPLEMENTATION.
  METHOD zif_badi_process~process.
    "Do nothing - null object pattern
    RETURN.
  ENDMETHOD.
ENDCLASS.
```

## Common BAdI Use Cases

### Use Case 1: Data Validation
```abap
INTERFACE zif_badi_validate.
  METHODS validate
    IMPORTING
      is_data        TYPE any
    CHANGING
      ct_messages    TYPE bapiret2_t
    RETURNING
      VALUE(rv_valid) TYPE abap_bool.
ENDINTERFACE.

"Implementation
METHOD zif_badi_validate~validate.
  "Custom validation logic
  IF is_data-field1 IS INITIAL.
    APPEND VALUE #(
      type       = 'E'
      id         = 'Z_MSG'
      number     = '001'
      message_v1 = 'Field 1 is required'
    ) TO ct_messages.
    rv_valid = abap_false.
  ELSE.
    rv_valid = abap_true.
  ENDIF.
ENDMETHOD.
```

### Use Case 2: Data Enrichment
```abap
INTERFACE zif_badi_enrich.
  METHODS enrich
    CHANGING
      cs_data TYPE any.
ENDINTERFACE.

"Implementation
METHOD zif_badi_enrich~enrich.
  "Add calculated fields
  cs_data-calculated_field = cs_data-field1 + cs_data-field2.
  cs_data-enrichment_timestamp = cl_abap_context_info=>get_system_time( ).
ENDMETHOD.
```

### Use Case 3: Integration Hooks
```abap
INTERFACE zif_badi_integration.
  METHODS before_save
    IMPORTING
      is_data        TYPE any.
  METHODS after_save
    IMPORTING
      is_data        TYPE any.
ENDINTERFACE.

"Implementation
METHOD zif_badi_integration~before_save.
  "Call external system before save
  DATA(lo_http_client) = cl_web_http_client_manager=>create_by_http_destination(
    cl_http_destination_provider=>create_by_url( 'https://api.example.com' ) ).
  "Make API call...
ENDMETHOD.
```

## RAP BAdI Patterns

### Pattern 1: RAP BAdI for Extension
```abap
"Released RAP BAdI interface
CLASS zcl_rap_badi_extension DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_some_released_rap_badi.
ENDCLASS.

CLASS zcl_rap_badi_extension IMPLEMENTATION.
  METHOD if_some_released_rap_badi~some_method.
    "Custom RAP extension logic
  ENDMETHOD.
ENDCLASS.
```

### Pattern 2: Dynamic BAdI Calls
```abap
"Dynamic BAdI call with variable BAdI name
DATA lo_badi TYPE REF TO cl_badi_base.
DATA(lv_badi_name) = 'ZBADI_MY_BADI'.

GET BADI lo_badi TYPE (lv_badi_name).

"Dynamic method call
CALL BADI lo_badi->('VALIDATE')
  EXPORTING is_data = ls_data.
```

## Testing BAdI Implementations

### Unit Test Pattern
```abap
CLASS ltc_badi_test DEFINITION FINAL FOR TESTING
  DURATION SHORT RISK LEVEL HARMLESS.
  PRIVATE SECTION.
    DATA mo_badi TYPE REF TO zif_badi_process.
    METHODS setup.
    METHODS test_process FOR TESTING.
ENDCLASS.

CLASS ltc_badi_test IMPLEMENTATION.
  METHOD setup.
    "Create test double
    mo_badi = NEW zcl_badi_test_double( ).
  ENDMETHOD.

  METHOD test_process.
    "Arrange
    DATA(lv_input) = 'test input'.

    "Act
    mo_badi->process(
      EXPORTING iv_input  = lv_input
      CHANGING  cv_output = DATA(lv_output) ).

    "Assert
    cl_abap_unit_assert=>assert_equals(
      act = lv_output
      exp = 'Processed: test input' ).
  ENDMETHOD.
ENDCLASS.
```

## ABAP Cloud Considerations

### Released BAdIs Only
```abap
"In ABAP Cloud, only implement released BAdIs
"Search for released BAdIs in ADT: api:badi

"Example of released RAP BAdI
CLASS zcl_released_badi_impl DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_sap_released_badi_interface.
ENDCLASS.
```

### Finding Released BAdIs
```abap
"Programmatic check for released BAdIs
SELECT SINGLE *
  FROM i_apistateofrepositoryobject
  WHERE ObjectType     = 'BADI'
    AND ObjectName     = 'Z_MY_BADI'
    AND ReleaseState   = 'RELEASED'
  INTO @DATA(ls_state).
```

## Migration Patterns

### Classic BAdI to New BAdI Migration
```abap
"Classic BAdI (SE18/SE19)
CALL FUNCTION 'Z_BADI_CLASSIC'
  EXPORTING
    iv_param = lv_value.

"New BAdI Framework
DATA lo_badi TYPE REF TO zif_badi_new.
GET BADI lo_badi.
CALL BADI lo_badi->process
  EXPORTING iv_param = lv_value.
```

### Level D → Level A/B Remediation

| Existing Level D technique                | Replacement                                              |
| ----------------------------------------- | -------------------------------------------------------- |
| Modification                              | Released BAdI → classic BAdI → key user extensibility    |
| Implicit enhancement                      | Released BAdI → classic BAdI                             |
| Explicit enhancement with inline code     | Move logic into a custom BAdI called from the spot       |
| Source code plug-in                       | Released or classic BAdI                                 |
| SAP-internal-flagged BAdI implementation  | Find an alternative released or classic extension point  |
| SAP Note manual correction                | Reset once the correction ships in the core              |

**Workflow:**
1. Run `SYCM_ALLOWED_ENH_TECHNOLOGY` and `CI_SEARCH_CUST_MODIFICATIONS`
2. For each priority 1 finding, search for a released BAdI (`api:badi` in ADT)
3. If none, search for a classic BAdI in the Cloudification Repository (Level B)
4. If neither exists, consider key user extensibility or a custom BAdI hosted in an explicit enhancement spot
5. Delete the Level D implementation and migrate the logic
6. Re-run ATC to confirm the finding is resolved

### Hosting a custom BAdI in an explicit enhancement spot

When no released or classic BAdI exists, this keeps the enhancement out of Level D inline code:

```abap
"In the explicit enhancement spot — delegate, do not inline
ENHANCEMENT z_my_enhancement.
  DATA lo_badi TYPE REF TO zif_badi_my_logic.
  GET BADI lo_badi FILTERS country = ls_data-country.
  CALL BADI lo_badi->process CHANGING cs_data = ls_data.
ENDENHANCEMENT.
```

The custom BAdI definition and its implementations live in your own package, so the logic is testable, filterable and upgrade-visible.

## Performance Considerations

### Optimization Tips
- Use filter-based BAdIs to reduce execution scope
- Implement fallback classes to avoid overhead
- Cache BAdI instances where appropriate
- Avoid expensive operations in BAdI implementations
- Use BAdI calls sparingly in performance-critical code

### Common Performance Issues
- Too many BAdI calls in loops
- Complex BAdI implementations
- Unnecessary BAdI calls
- Missing filter optimizations

## Error Handling Patterns

### Pattern 1: Exception Handling
```abap
TRY.
    GET BADI lo_badi.
    CALL BADI lo_badi->process
      EXPORTING iv_input = lv_input
      CHANGING  cv_output = lv_output.
  CATCH cx_badi_not_implemented INTO DATA(lx_error).
    "Handle case where no implementation exists
    cv_output = |Default: { lv_input }|.
ENDTRY.
```

### Pattern 2: Graceful Degradation
```abap
"Use fallback class when no implementation exists
DATA lo_badi TYPE REF TO zif_badi_process.
GET BADI lo_badi.

IF lo_badi IS BOUND.
  CALL BADI lo_badi->process
    EXPORTING iv_input = lv_input
    CHANGING  cv_output = lv_output.
ELSE.
  "Use default behavior
  cv_output = |Fallback: { lv_input }|.
ENDIF.
```

## Best Practices

### Design Principles
- Keep BAdI interfaces focused and single-purpose
- Use descriptive method names
- Provide clear documentation
- Implement proper error handling
- Use filters to scope implementations

### Implementation Guidelines
- Implement one concern per BAdI implementation
- Follow Clean ABAP principles
- Add comprehensive unit tests
- Document integration points
- Handle edge cases appropriately

### Maintenance Considerations
- Version BAdI interfaces carefully
- Provide migration guides for changes
- Monitor BAdI performance
- Regular review of BAdI implementations
- Document deprecation timelines

## Common Pitfalls

### Pitfalls to Avoid
- Implementing too much logic in BAdIs
- Creating circular dependencies
- Ignoring error handling
- Missing fallback implementations
- Overusing BAdIs for simple logic

### Troubleshooting Tips
- Check BAdI is active in system
- Verify filter conditions match
- Test with known good data
- Review enhancement spot configuration
- Check authorization for BAdI execution