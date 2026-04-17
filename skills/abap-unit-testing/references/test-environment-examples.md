# Test Environment & Test Double Examples

Detailed code examples for CDS test environments, OSQL test environments, RAP BO test doubles, and test seams.

## CDS Test Environment

For testing CDS view entities with stubbed data sources.

```abap
CLASS ltc_cds_view DEFINITION FINAL FOR TESTING
  DURATION SHORT RISK LEVEL HARMLESS.

  PRIVATE SECTION.
    CLASS-DATA environment TYPE REF TO if_cds_test_environment.

    CLASS-METHODS class_setup.
    CLASS-METHODS class_teardown.
    METHODS setup.
    METHODS test_view_calculation FOR TESTING.
ENDCLASS.

CLASS ltc_cds_view IMPLEMENTATION.

  METHOD class_setup.
    " Create test environment for the CDS view entity
    " Automatically stubs all data sources used by the view
    environment = cl_cds_test_environment=>create( i_for_entity = 'ZI_SALESORDER' ).
  ENDMETHOD.

  METHOD class_teardown.
    environment->destroy( ).
  ENDMETHOD.

  METHOD setup.
    " Clear test data before each test
    environment->clear_doubles( ).
  ENDMETHOD.

  METHOD test_view_calculation.
    " Arrange — insert test data into stubbed data source
    DATA lt_test_data TYPE STANDARD TABLE OF zsalesorder.
    lt_test_data = VALUE #(
      ( client = sy-mandt order_id = '001' customer_id = 'CUST1'
        net_amount = 100 currency_code = 'EUR' status = 'N' )
      ( client = sy-mandt order_id = '002' customer_id = 'CUST1'
        net_amount = 200 currency_code = 'EUR' status = 'A' ) ).

    environment->insert_test_data( i_data = lt_test_data ).

    " Act — select from the CDS view
    SELECT FROM zi_salesorder
      FIELDS OrderId, NetAmount, Status
      WHERE CustomerId = 'CUST1'
      INTO TABLE @DATA(lt_result).

    " Assert
    cl_abap_unit_assert=>assert_equals(
      act = lines( lt_result )
      exp = 2
      msg = 'Expected 2 orders for CUST1' ).
  ENDMETHOD.

ENDCLASS.
```

### Key Points

- `cl_cds_test_environment=>create( )` automatically stubs all underlying data sources
- Use `insert_test_data( )` to provide data for the stubbed tables
- Use `clear_doubles( )` in `setup` to isolate tests
- Always call `destroy( )` in `class_teardown`
- Works with associations, joins, and complex CDS expressions

## OSQL (Open SQL) Test Environment

For testing ABAP classes that use ABAP SQL `SELECT` statements.

```abap
CLASS ltc_sql_dependent DEFINITION FINAL FOR TESTING
  DURATION SHORT RISK LEVEL HARMLESS.

  PRIVATE SECTION.
    CLASS-DATA environment TYPE REF TO if_osql_test_environment.

    CLASS-METHODS class_setup.
    CLASS-METHODS class_teardown.
    METHODS setup.
    METHODS test_read_customers FOR TESTING.
ENDCLASS.

CLASS ltc_sql_dependent IMPLEMENTATION.

  METHOD class_setup.
    " Create test environment for specific tables/views
    environment = cl_osql_test_environment=>create(
      i_dependency_list = VALUE #(
        ( 'ZCUSTOMER' )
        ( 'ZSALESORDER' ) ) ).
  ENDMETHOD.

  METHOD class_teardown.
    environment->destroy( ).
  ENDMETHOD.

  METHOD setup.
    environment->clear_doubles( ).
  ENDMETHOD.

  METHOD test_read_customers.
    " Arrange
    DATA lt_customers TYPE STANDARD TABLE OF zcustomer.
    lt_customers = VALUE #(
      ( client = sy-mandt customer_id = 'C1' customer_name = 'Alice' )
      ( client = sy-mandt customer_id = 'C2' customer_name = 'Bob' ) ).

    environment->insert_test_data( i_data = lt_customers ).

    " Act
    DATA(cut) = NEW zcl_customer_reader( ).
    DATA(lt_result) = cut->get_all_customers( ).

    " Assert
    cl_abap_unit_assert=>assert_equals(
      act = lines( lt_result )
      exp = 2 ).
  ENDMETHOD.

ENDCLASS.
```

## RAP BO Test Doubles

### Transactional Buffer Test Double

For testing code that uses EML to interact with a RAP BO.

```abap
CLASS ltc_rap_consumer DEFINITION FINAL FOR TESTING
  DURATION SHORT RISK LEVEL HARMLESS.

  PRIVATE SECTION.
    CLASS-DATA environment TYPE REF TO if_botd_txbufdbl_bo_test_env.

    CLASS-METHODS class_setup.
    CLASS-METHODS class_teardown.
    METHODS setup.
    METHODS test_create_order FOR TESTING.
ENDCLASS.

CLASS ltc_rap_consumer IMPLEMENTATION.

  METHOD class_setup.
    " Create a transactional buffer test double for the RAP BO
    environment = cl_botd_txbufdbl_bo_test_env=>create(
      environment_config = cl_botd_txbufdbl_bo_test_env=>prepare_environment_config(
      )->set_bdef_dependencies( VALUE #( ( 'ZR_SALESORDER' ) ) ) ).
  ENDMETHOD.

  METHOD class_teardown.
    environment->destroy( ).
  ENDMETHOD.

  METHOD setup.
    environment->clear_doubles( ).
  ENDMETHOD.

  METHOD test_create_order.
    " Act — code under test uses EML to create an order
    MODIFY ENTITIES OF zr_salesorder
      ENTITY Root
      CREATE FIELDS ( Description Status )
      WITH VALUE #(
        ( %cid = 'test1'
          Description = 'Test Order'
          Status = 'NEW' ) )
      MAPPED DATA(mapped)
      FAILED DATA(failed)
      REPORTED DATA(reported).

    " Assert
    cl_abap_unit_assert=>assert_initial( act = failed ).
    cl_abap_unit_assert=>assert_not_initial( act = mapped-root ).
  ENDMETHOD.

ENDCLASS.
```

### Mocking EML APIs

For testing RAP handler method implementations.

```abap
CLASS ltc_rap_handler DEFINITION FINAL FOR TESTING
  DURATION SHORT RISK LEVEL HARMLESS.

  PRIVATE SECTION.
    CLASS-DATA environment TYPE REF TO if_botd_mockemlapi_bo_test_env.

    CLASS-METHODS class_setup.
    CLASS-METHODS class_teardown.
    METHODS setup.
    METHODS test_action_handler FOR TESTING.
ENDCLASS.

CLASS ltc_rap_handler IMPLEMENTATION.

  METHOD class_setup.
    environment = cl_botd_mockemlapi_bo_test_env=>create(
      environment_config = cl_botd_mockemlapi_bo_test_env=>prepare_environment_config(
      )->set_bdef_dependencies( VALUE #( ( 'ZR_SALESORDER' ) ) ) ).
  ENDMETHOD.

  METHOD class_teardown.
    environment->destroy( ).
  ENDMETHOD.

  METHOD setup.
    environment->clear_doubles( ).
  ENDMETHOD.

  METHOD test_action_handler.
    " Configure mock EML API responses
    DATA lt_read_result TYPE TABLE FOR READ RESULT zr_salesorder.
    lt_read_result = VALUE #(
      ( OrderUUID = '12345' Description = 'Test' Status = 'NEW' ) ).

    environment->get_test_double( 'ZR_SALESORDER'
      )->configure_read_response( lt_read_result ).

    " Create handler instance for testing
    DATA lo_handler TYPE REF TO lhc_root.
    CREATE OBJECT lo_handler FOR TESTING.

    " Execute handler method...
  ENDMETHOD.

ENDCLASS.
```

## Test Seams (Legacy Code)

For injecting test behavior into legacy code without refactoring.

```abap
" Production code
METHOD get_current_date.
  TEST-SEAM get_date.
    rv_date = sy-datum.
  END-TEST-SEAM.
ENDMETHOD.

" Test code
METHOD test_future_date.
  TEST-INJECTION get_date.
    rv_date = '20301231'.
  END-TEST-INJECTION.

  DATA(lv_result) = cut->get_current_date( ).
  cl_abap_unit_assert=>assert_equals(
    act = lv_result
    exp = '20301231' ).
ENDMETHOD.
```

> **Note**: Prefer constructor injection over test seams for new code. Test seams are useful for making legacy code testable without major refactoring.
