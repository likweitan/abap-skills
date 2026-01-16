# Clean ABAP Quick Reference

This document provides quick reference patterns for Clean ABAP compliance checks.

## Naming Patterns

### ✓ Good
```abap
DATA max_wait_time_in_seconds TYPE i.
DATA customizing_entries TYPE STANDARD TABLE.
METHODS read_user_preferences.
CLASS /clean/user_preference_reader.
```

### ✗ Bad
```abap
DATA lv_max_time TYPE i.           " Hungarian notation
DATA gt_entries TYPE STANDARD TABLE. " Prefix
METHODS read_t005.                  " Technical name
CLASS /dirty/t005_reader.           " Technical name
```

## Language Constructs

### ✓ Good - Functional Style
```abap
DATA(variable) = 'A'.
DATA(uppercase) = to_upper( lowercase ).
index += 1.
DATA(object) = NEW /clean/my_class( ).
result = VALUE #( FOR row IN input ( row-text ) ).
DATA(line) = value_pairs[ name = 'A' ].
DATA(exists) = xsdbool( line_exists( value_pairs[ name = 'A' ] ) ).
```

### ✗ Bad - Procedural Style
```abap
MOVE 'A' TO variable.
TRANSLATE lowercase TO UPPER CASE.
ADD 1 TO index.
CREATE OBJECT object TYPE /dirty/my_class.
LOOP AT input INTO DATA(row).
  INSERT row-text INTO TABLE result.
ENDLOOP.
READ TABLE value_pairs WITH KEY name = 'A' TRANSPORTING NO FIELDS.
DATA(exists) = xsdbool( sy-subrc = 0 ).
```

## Constants

### ✓ Good
```abap
CLASS /clean/message_severity DEFINITION.
  PUBLIC SECTION.
    TYPES: BEGIN OF ENUM type,
             warning,
             error,
           END OF ENUM type.
ENDCLASS.

" Or grouped constants
CONSTANTS:
  BEGIN OF message_severity,
    warning TYPE symsgty VALUE 'W',
    error   TYPE symsgty VALUE 'E',
  END OF message_severity.
```

### ✗ Bad
```abap
CONSTANTS:
  c_warning TYPE symsgty VALUE 'W',
  c_01 TYPE spart VALUE '01',      " Non-descriptive
  warning TYPE symsgty VALUE 'W',
  transitional TYPE i VALUE 1,      " Ungrouped, unrelated
  error TYPE symsgty VALUE 'E'.
```

## Variables

### ✓ Good - Inline
```abap
METHOD do_something.
  DATA(name) = 'something'.
  DATA(reader) = /clean/reader=>get_instance_for( name ).
  result = reader->read_it( ).
ENDMETHOD.
```

### ✗ Bad - Up-front
```abap
METHOD do_something.
  DATA:
    name   TYPE seoclsname,
    reader TYPE REF TO /dirty/reader.
  name = 'something'.
  reader = /dirty/reader=>get_instance_for( name ).
  result = reader->read_it( ).
ENDMETHOD.
```

## Tables

### ✓ Good
```abap
" Explicit key
DATA itab TYPE STANDARD TABLE OF row_type WITH NON-UNIQUE KEY comp1 comp2.
DATA itab TYPE STANDARD TABLE OF row_type WITH EMPTY KEY.

" Modern operations
INSERT VALUE #( ... ) INTO TABLE itab.
IF line_exists( my_table[ key = 'A' ] ).
DATA(line) = my_table[ key = 'A' ].
LOOP AT my_table REFERENCE INTO DATA(line) WHERE key = 'A'.
```

### ✗ Bad
```abap
" Default key
DATA itab TYPE STANDARD TABLE OF row_type WITH DEFAULT KEY.

" Old-style operations
APPEND VALUE #( ... ) TO itab.
READ TABLE my_table WITH KEY key = 'A' TRANSPORTING NO FIELDS.
IF sy-subrc = 0.
READ TABLE my_table INTO DATA(line) WITH KEY key = 'A'.
LOOP AT my_table INTO DATA(line).
  IF line-key = 'A'.
```

## Strings

### ✓ Good
```abap
CONSTANTS some_constant TYPE string VALUE `ABC`.
DATA(some_string) = `ABC`.
DATA(message) = |Received HTTP code { status_code } with message { text }|.
```

### ✗ Bad
```abap
DATA some_string TYPE string VALUE 'ABC'.  " Single quotes
DATA(message) = `Received ` && status_code && ` with ` && text.  " Concatenation
```

## Booleans

### ✓ Good
```abap
DATA has_entries TYPE abap_bool.
has_entries = abap_true.
IF has_entries = abap_false.
DATA(has_entries) = xsdbool( line IS NOT INITIAL ).
IF is_empty( table ).  " Predicative call
```

### ✗ Bad
```abap
DATA has_entries TYPE char1.
has_entries = 'X'.
IF has_entries = space.
IF line IS INITIAL.
  has_entries = abap_false.
ELSE.
  has_entries = abap_true.
ENDIF.
IF is_empty( table ) = abap_true.  " Unnecessary comparison
```

## Conditions

### ✓ Good
```abap
IF has_entries = abap_true.       " Positive
IF variable IS NOT INITIAL.        " IS NOT
IF condition_is_fulfilled( ).      " Predicative

" Decomposed
DATA(example_provided) = xsdbool( example_a IS NOT INITIAL OR
                                  example_b IS NOT INITIAL ).
IF example_provided = abap_true.
```

### ✗ Bad
```abap
IF has_no_entries = abap_false.    " Negative
IF NOT variable IS INITIAL.        " NOT IS
IF condition_is_fulfilled( ) = abap_true.  " Unnecessary comparison

" Complex inline
IF ( example_a IS NOT INITIAL OR example_b IS NOT INITIAL ) AND
   ( applies( example_a ) = abap_true OR applies( example_b ) = abap_true ).
```

## Ifs

### ✓ Good
```abap
IF has_entries = abap_false.
  " do something
ENDIF.

CASE type.
  WHEN type-some_type.
    " ...
  WHEN type-some_other_type.
    " ...
  WHEN OTHERS.
    RAISE EXCEPTION NEW /clean/unknown_type_failure( ).
ENDCASE.
```

### ✗ Bad
```abap
IF has_entries = abap_true.
ELSE.
  " do something
ENDIF.

IF type = type-some_type.
  " ...
ELSEIF type = type-some_other_type.
  " ...
ELSE.
  RAISE EXCEPTION NEW /dirty/unknown_type_failure( ).
ENDIF.

" Deep nesting
IF <this>.
  IF <that>.
    IF <other>.
      IF <something>.
```

## Classes

### ✓ Good
```abap
CLASS /clean/account DEFINITION PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES /clean/account_intf.
    METHODS constructor.
  PRIVATE SECTION.
    DATA balance TYPE i.
    METHODS calculate_interest RETURNING VALUE(result) TYPE i.
ENDCLASS.
```

### ✗ Bad
```abap
CLASS /dirty/account DEFINITION PUBLIC CREATE PUBLIC.  " Not FINAL
  PUBLIC SECTION.
    METHODS read_balance RETURNING VALUE(result) TYPE i.  " Not in interface
    METHODS write_balance IMPORTING value TYPE i.
    DATA balance TYPE i.  " Public data
  PROTECTED SECTION.
    METHODS calculate_interest.  " Should be PRIVATE
ENDCLASS.
```

## Methods - Calls

### ✓ Good
```abap
DATA(sum) = aggregate_values( values ).
modify->update( node = /clean/my_bo_c=>node-item
                key  = item->key
                data = item ).
DATA(unique_list) = remove_duplicates( list ).
DATA(sum) = aggregate_values( values ).  " No me->
```

### ✗ Bad
```abap
aggregate_values(
  EXPORTING values = values
  RECEIVING result = DATA(sum) ).
  
CALL METHOD modify->update
  EXPORTING
    node = /dirty/my_bo_c=>node-item
    key  = item->key
    data = item.

DATA(unique_list) = remove_duplicates( list = list ).  " Unnecessary param name
DATA(sum) = me->aggregate_values( values ).  " Unnecessary me->
```

## Methods - Signatures

### ✓ Good
```abap
METHODS calculate
  IMPORTING value1 TYPE i
            value2 TYPE i
  RETURNING VALUE(result) TYPE i.

METHODS check
  IMPORTING business_partners TYPE business_partners
  RETURNING VALUE(result) TYPE result_type.
```

### ✗ Bad
```abap
METHODS calculate
  IMPORTING iv_value1 TYPE i
            iv_value2 TYPE i
            iv_value3 TYPE i OPTIONAL
            iv_value4 TYPE i OPTIONAL
  EXPORTING ev_result TYPE i
            ev_status TYPE status.

METHODS check
  IMPORTING business_partners TYPE business_partners
  EXPORTING result TYPE result_type
            failed_keys TYPE /bobf/t_frw_key
            messages TYPE /bobf/t_frw_message.
```

## Error Handling

### ✓ Good
```abap
IF input IS INITIAL.
  RAISE EXCEPTION NEW /clean/invalid_input( ).
ENDIF.

TRY.
    result = call_something( ).
  CATCH cx_static_check INTO DATA(error).
    RAISE EXCEPTION NEW /clean/wrapped_error( previous = error ).
ENDTRY.
```

### ✗ Bad
```abap
IF input IS INITIAL.
  ev_error = abap_true.
  RETURN.
ENDIF.

TRY.
    result = call_something( ).
  CATCH cx_root.  " Too generic
    " Silent catch
ENDTRY.
```

## Comments

### ✓ Good
```abap
"Workaround for bug in SAP Note 12345
DATA(result) = calculate_with_workaround( ).

" TODO (USERID): Refactor after migration to S/4HANA
```

### ✗ Bad
```abap
" Add 1 to index
index = index + 1.

" * This is an old style comment

" MOVE 'OLD' TO code.  " Commented code

" Version 1.0 - Initial version
" Version 1.1 - Fixed bug
```

## Testing

### ✓ Good
```abap
METHOD should_return_sum_when_adding_two_numbers.
  " Given
  DATA(value1) = 5.
  DATA(value2) = 3.
  
  " When
  DATA(result) = calculator->add( value1 = value1
                                  value2 = value2 ).
  
  " Then
  cl_abap_unit_assert=>assert_equals(
    act = result
    exp = 8 ).
ENDMETHOD.
```

### ✗ Bad
```abap
METHOD test_1.
  DATA(result) = calculator->add( value1 = 5 value2 = 3 ).
  cl_abap_unit_assert=>assert_equals( act = result exp = 8 ).
  
  result = calculator->subtract( value1 = 5 value2 = 3 ).
  cl_abap_unit_assert=>assert_equals( act = result exp = 2 ).
  
  result = calculator->multiply( value1 = 5 value2 = 3 ).
  cl_abap_unit_assert=>assert_equals( act = result exp = 15 ).
ENDMETHOD.
```

## Common Anti-Patterns Summary

1. **Hungarian Notation**: lv_, gt_, lt_, ls_, iv_, ev_, rv_
2. **Magic Numbers**: Hard-coded values without constants
3. **Up-front Declarations**: DATA section instead of inline
4. **Old SELECT**: Without @ host variables
5. **DEFAULT KEY**: Should specify explicit key or EMPTY KEY
6. **APPEND TO**: Should use INSERT INTO TABLE
7. **Empty IF**: Logic only in ELSE branch
8. **Deep Nesting**: More than 3 levels
9. **Long Methods**: More than 20 lines
10. **Multiple Parameters**: More than 3 IMPORTING parameters
11. **EXPORTING**: Should use RETURNING for single output
12. **Static Classes**: Should use instance classes with interfaces
13. **Return Codes**: Should use exceptions
14. **Commented Code**: Should be deleted
15. **Obvious Comments**: Comments explaining what instead of why
