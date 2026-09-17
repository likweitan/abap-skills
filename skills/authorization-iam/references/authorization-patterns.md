# Authorization Patterns Reference

Common authorization patterns and implementations for ABAP Cloud and on-premise systems.

## Authorization Check Patterns

### Pattern 1: Simple Authorization Check (ABAP Cloud)
```abap
"Check single authorization object
DATA(lo_auth) = cl_abap_authorization=>check_authorization(
  EXPORTING
    authorization_object = 'Z_MY_AUTH'
    authorizations       = VALUE #(
      ( field = 'ACTVT' value = '03' )    "Display
      ( field = 'ZCARR' value = lv_carrier ) ) ).

IF lo_auth->is_authorized( ) = abap_false.
  RAISE EXCEPTION TYPE zcx_not_authorized.
ENDIF.
```

### Pattern 2: Multiple Authorization Checks
```abap
"Check multiple activities
DATA(lo_auth_display) = cl_abap_authorization=>check_authorization(
  authorization_object = 'Z_MY_AUTH'
  authorizations       = VALUE #(
    ( field = 'ACTVT' value = '03' )
    ( field = 'ZCARR' value = lv_carrier ) ) ).

DATA(lo_auth_change) = cl_abap_authorization=>check_authorization(
  authorization_object = 'Z_MY_AUTH'
  authorizations       = VALUE #(
    ( field = 'ACTVT' value = '02' )
    ( field = 'ZCARR' value = lv_carrier ) ) ).

IF lo_auth_display->is_authorized( ) = abap_false.
  "Handle display authorization failure
ELSEIF lo_auth_change->is_authorized( ) = abap_true.
  "Enable edit functionality
ENDIF.
```

### Pattern 3: Classic Authorization Check (On-Premise)
```abap
AUTHORITY-CHECK OBJECT 'Z_MY_AUTH'
  ID 'ACTVT' FIELD '03'
  ID 'ZCARR' FIELD lv_carrier.

IF sy-subrc <> 0.
  MESSAGE e001(z_msg) WITH lv_carrier.
  RETURN.
ENDIF.
```

## CDS Access Control Patterns

### Pattern 1: Simple Role-Based Access
```cds
@EndUserText.label: 'Access Control for Travel'
@MappingRole: true
define role ZI_Travel {
  grant select on ZI_Travel
    where ( carrier_id ) =
      aspect pfcg_auth ( Z_MY_AUTH, ZCARR, ACTVT = '03' );
}
```

### Pattern 2: Multiple Conditions
```cds
define role ZI_Travel {
  grant select on ZI_Travel
    where ( carrier_id ) =
      aspect pfcg_auth ( Z_MY_AUTH, ZCARR, ACTVT = '03' )
      and ( agency_id ) =
      aspect pfcg_auth ( Z_AGENCY_AUTH, ZAGENCY, ACTVT = '03' );
}
```

### Pattern 3: Unrestricted Access
```cds
define role ZI_Travel_Admin {
  grant select on ZI_Travel
    where _unrestrictedAccess;
}
```

### Pattern 4: User-Based Restriction
```cds
define role ZI_MyOrders {
  grant select on ZI_Travel
    where CreatedBy = aspect user;
}
```

### Pattern 5: Inherited Access Control
```cds
"Child entity inherits access control from parent
define role ZI_Booking {
  grant select on ZI_Booking
    where inheriting conditions from entity ZI_Travel
      association _Order;
}
```

## RAP Authorization Patterns

### Pattern 1: Instance Authorization
```abap
METHOD get_instance_authorizations.
  READ ENTITIES OF zr_travel IN LOCAL MODE
    ENTITY Travel
    FIELDS ( carrier_id )
    WITH CORRESPONDING #( keys )
    RESULT DATA(lt_travels).

  LOOP AT lt_travels INTO DATA(ls_travel).
    DATA(lo_auth) = cl_abap_authorization=>check_authorization(
      authorization_object = 'Z_MY_AUTH'
      authorizations       = VALUE #(
        ( field = 'ZCARR' value = ls_travel-carrier_id )
        ( field = 'ACTVT' value = COND #(
            WHEN requested_authorizations-%update = if_abap_behv=>mk-on
              THEN '02'
            WHEN requested_authorizations-%delete = if_abap_behv=>mk-on
              THEN '06'
            ELSE '03' ) )
      ) ).

    APPEND VALUE #(
      %tky = ls_travel-%tky
      %update = COND #( WHEN lo_auth->is_authorized( ) THEN if_abap_behv=>auth-allowed
                        ELSE if_abap_behv=>auth-unauthorized )
      %delete = COND #( WHEN lo_auth->is_authorized( ) THEN if_abap_behv=>auth-allowed
                        ELSE if_abap_behv=>auth-unauthorized )
    ) TO result.
  ENDLOOP.
ENDMETHOD.
```

### Pattern 2: Global Authorization
```abap
METHOD get_global_authorizations.
  DATA(lo_auth) = cl_abap_authorization=>check_authorization(
    authorization_object = 'Z_MY_AUTH'
    authorizations       = VALUE #(
      ( field = 'ACTVT' value = '01' ) ) ).  "Create

  IF lo_auth->is_authorized( ).
    result-%create = if_abap_behv=>auth-allowed.
  ELSE.
    result-%create = if_abap_behv=>auth-unauthorized.
  ENDIF.
ENDMETHOD.
```

## IAM Configuration Patterns

### Pattern 1: Basic IAM App Setup
```
ADT: New → Other → IAM App
Name: Z_TRAVEL_IAM
Type: EXT - External App
Service Binding: ZUI_TRAVEL_O4
Authorization Objects: Z_MY_AUTH, Z_AGENCY_AUTH
```

### Pattern 2: Business Catalog Structure
```
Business Catalog: Z_BC_TRAVEL_MGMT
Description: Travel Management
IAM Apps: 
  - Z_TRAVEL_IAM
  - Z_BOOKING_IAM
  - Z_CUSTOMER_IAM
```

### Pattern 3: Business Role with Restrictions
```
Business Role: Z_BR_TRAVEL_MANAGER
Business Catalogs: Z_BC_TRAVEL_MGMT
Restriction Types:
  - ZCARR: Restricted to 'LH', 'AA'
  - ZAGENCY: Unrestricted
  - ACTVT: Display and Change
```

## Custom Authorization Object Patterns

### Pattern 1: Simple Authorization Object
```
Authorization Object: Z_MY_AUTH
Authorization Class: Z_TRAVEL
Fields:
  - ACTVT (Activity) - Domain: ACTIV_AUTH
  - ZCARR (Carrier) - Type: S_CARR_ID
  - ZREGN (Region) - Type: CHAR4
```

### Pattern 2: Hierarchical Authorization
```
Authorization Object: Z_ORG_AUTH
Authorization Class: Z_ORG
Fields:
  - ACTVT (Activity)
  - ZCOMP (Company) - Type: CHAR4
  - ZDEPT (Department) - Type: CHAR6
  - ZTEAM (Team) - Type: CHAR8
```

## Common Authorization Scenarios

### Scenario 1: Field-Level Security
```abap
"Restrict access based on organizational hierarchy
DATA(lo_auth) = cl_abap_authorization=>check_authorization(
  authorization_object = 'Z_ORG_AUTH'
  authorizations       = VALUE #(
    ( field = 'ACTVT' value = '03' )
    ( field = 'ZCOMP' value = lv_company )
    ( field = 'ZDEPT' value = lv_department )
    ( field = 'ZTEAM' value = lv_team ) ) ).
```

### Scenario 2: Time-Based Authorization
```abap
"Check if user has authorization within time window
IF lv_start_date <= cl_abap_context_info=>get_system_date( ) AND
   lv_end_date >= cl_abap_context_info=>get_system_date( ).
  "Perform authorization check
ENDIF.
```

### Scenario 3: Dynamic Authorization Values
```abap
"Build authorization values dynamically
DATA(lt_auth_values) = VALUE #(
  ( field = 'ACTVT' value = lv_activity )
  ( field = 'ZCARR' value = COND #(
      WHEN lv_user_type = 'ADMIN' THEN '*'
      ELSE lv_carrier ) ) ).
```

## Error Handling Patterns

### Pattern 1: Authorization Exception
```abap
CLASS zcx_not_authorized DEFINITION
  INHERITING FROM cx_static_check.
  PUBLIC SECTION.
    METHODS constructor
      IMPORTING
        iv_text        TYPE string
        iv_authority   TYPE string
        iv_user        TYPE string OPTIONAL.
ENDCLASS.

"Usage
IF lo_auth->is_authorized( ) = abap_false.
  RAISE EXCEPTION TYPE zcx_not_authorized
    EXPORTING
      iv_text      = 'User not authorized for this operation'
      iv_authority = 'Z_MY_AUTH'
      iv_user      = cl_abap_context_info=>get_user_technical_name( ).
ENDIF.
```

### Pattern 2: Graceful Degradation
```abap
"Provide limited functionality when authorization fails
IF lo_auth_read->is_authorized( ) = abap_true.
  "Full read access
  SELECT * FROM zi_travel INTO TABLE @DATA(lt_all_travels).
ELSEIF lo_auth_limited->is_authorized( ) = abap_true.
  "Limited access - own records only
  SELECT * FROM zi_travel
    WHERE created_by = @cl_abap_context_info=>get_user_technical_name( )
    INTO TABLE @lt_all_travels.
ELSE.
  "No access - return empty
  lt_all_travels = VALUE #( ).
ENDIF.
```

## Performance Considerations

### Optimization Tips
- Cache authorization checks where possible
- Use connection pooling for authorization checks
- Batch authorization checks for multiple objects
- Consider authorization checks in database layer (CDS DCL)
- Use `PRIVILEGED ACCESS` sparingly in background jobs

### Common Performance Issues
- Authorization checks in tight loops
- Redundant authorization checks
- Complex authorization object structures
- Missing indexes on authorization fields

## Testing Authorization

### Unit Test Pattern
```abap
CLASS ltc_authorization DEFINITION FINAL FOR TESTING
  DURATION SHORT RISK LEVEL HARMLESS.
  PRIVATE SECTION.
    METHODS test_authorized_user FOR TESTING.
    METHODS test_unauthorized_user FOR TESTING.
ENDCLASS.

CLASS ltc_authorization IMPLEMENTATION.
  METHOD test_authorized_user.
    "Arrange
    DATA(lo_auth) = cl_abap_authorization=>check_authorization(
      authorization_object = 'Z_MY_AUTH'
      authorizations       = VALUE #(
        ( field = 'ACTVT' value = '03' )
        ( field = 'ZCARR' value = 'LH' ) ) ).

    "Act & Assert
    cl_abap_unit_assert=>assert_true(
      act = lo_auth->is_authorized( )
      msg = 'User should be authorized' ).
  ENDMETHOD.

  METHOD test_unauthorized_user.
    "Arrange
    DATA(lo_auth) = cl_abap_authorization=>check_authorization(
      authorization_object = 'Z_MY_AUTH'
      authorizations       = VALUE #(
        ( field = 'ACTVT' value = '03' )
        ( field = 'ZCARR' value = 'XX' ) ) ).

    "Act & Assert
    cl_abap_unit_assert=>assert_false(
      act = lo_auth->is_authorized( )
      msg = 'User should not be authorized' ).
  ENDMETHOD.
ENDCLASS.
```

## Migration Patterns

### On-Premise to ABAP Cloud Migration
```abap
"Before (On-Premise)
AUTHORITY-CHECK OBJECT 'Z_MY_AUTH'
  ID 'ACTVT' FIELD '03'
  ID 'ZCARR' FIELD lv_carrier.
IF sy-subrc <> 0.
  "Handle error
ENDIF.

"After (ABAP Cloud)
DATA(lo_auth) = cl_abap_authorization=>check_authorization(
  authorization_object = 'Z_MY_AUTH'
  authorizations       = VALUE #(
    ( field = 'ACTVT' value = '03' )
    ( field = 'ZCARR' value = lv_carrier ) ) ).
IF lo_auth->is_authorized( ) = abap_false.
  "Handle error
ENDIF.
```

## Security Best Practices

### Principle of Least Privilege
- Grant minimum required permissions
- Use specific field values instead of wildcards
- Regular audit of authorizations
- Implement time-based restrictions where appropriate

### Defense in Depth
- Implement authorization at multiple layers
- Use CDS DCL for data-level security
- Implement application-level checks
- Log authorization failures for audit trails

### Audit and Compliance
- Log all authorization checks
- Implement regular authorization reviews
- Monitor for unusual access patterns
- Maintain authorization documentation