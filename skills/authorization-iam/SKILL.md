---
name: authorization-iam
description: Help with ABAP authorization and IAM (Identity and Access Management) including authorization objects, authorization checks, IAM apps, business catalogs, business roles, restriction types, CDS access control (DCL), privilege access annotations, and role-based access in ABAP Cloud and on-premise. Use when users ask about authorization, AUTHORITY-CHECK, authorization object, IAM app, business catalog, business role, restriction type, CDS access control, DCL, access control, privilege annotation, role assignment, PFCG role, S_DEVELOP, or securing ABAP applications. Triggers include "authorization check", "create authorization object", "CDS access control", "IAM app", "business catalog", "business role", "PFCG", "restrict access", or "role-based security".
---

# Authorization & IAM

Guide for implementing authorization checks and identity/access management in ABAP Cloud and on-premise systems.

## Workflow

1. **Determine the user's goal**:
   - Implementing authorization checks in ABAP code
   - Creating CDS access controls (DCL)
   - Setting up IAM apps, business catalogs, and business roles (ABAP Cloud)
   - Managing PFCG roles (on-premise)
   - Defining custom authorization objects
   - Understanding restriction types

2. **Identify the platform**:
   - ABAP Cloud (BTP or S/4HANA embedded) → IAM apps + business catalogs + `CL_ABAP_AUTHORIZATION`
   - On-premise / Standard ABAP → PFCG roles + `AUTHORITY-CHECK`

3. **Guide implementation** with the appropriate authorization model

## Authorization Models

### ABAP Cloud (BTP / S/4HANA Cloud)

```
IAM App → Business Catalog → Business Role → Business User
                                    ↑
                            Restriction Type (field-level restrictions)
```

### On-Premise (Standard ABAP)

```
Authorization Object → PFCG Role → User Assignment
       ↑
Authorization Fields + Permitted Values
```

## Authorization Checks in Code

### ABAP Cloud — `CL_ABAP_AUTHORIZATION`

```abap
"Check authorization using released API
DATA(lo_auth) = cl_abap_authorization=>check_authorization(
  EXPORTING
    authorization_object = 'Z_MY_AUTH'
    authorizations       = VALUE #(
      ( field = 'ACTVT' value = '03' )    "Display
      ( field = 'ZCARR' value = lv_carrier )
    ) ).

IF lo_auth->is_authorized( ) = abap_false.
  "User not authorized
  RAISE EXCEPTION TYPE zcx_not_authorized.
ENDIF.
```

### On-Premise — `AUTHORITY-CHECK`

```abap
AUTHORITY-CHECK OBJECT 'Z_MY_AUTH'
  ID 'ACTVT' FIELD '03'
  ID 'ZCARR' FIELD lv_carrier.

IF sy-subrc <> 0.
  MESSAGE e001(z_msg) WITH lv_carrier.
  RETURN.
ENDIF.
```

### Activity Values (ACTVT)

| Value | Activity |
| ----- | -------- |
| `01`  | Create   |
| `02`  | Change   |
| `03`  | Display  |
| `06`  | Delete   |
| `16`  | Execute  |

## Authorization Objects

### Creating a Custom Authorization Object

In ADT or `SU21`:

```
Authorization Object: Z_MY_AUTH
  Fields:
    ACTVT  — Activity (standard field, linked to domain ACTIV_AUTH)
    ZCARR  — Carrier (custom field, type S_CARR_ID)
    ZREGN  — Region (custom field, type CHAR4)
```

#### Structure

- **Authorization Class**: Groups related objects (e.g., `Z_TRAVEL`)
- **Authorization Object**: Contains 1–10 authorization fields
- **Authorization Field**: Links to a data element; defines the check dimension

## CDS Access Control (DCL)

CDS access controls define row-level authorization for CDS view entities.

### Basic DCL

```cds
@EndUserText.label: 'Access Control for Travel'
@MappingRole: true
define role ZI_Travel {
  grant select on ZI_Travel
    where ( carrier_id ) =
      aspect pfcg_auth ( Z_MY_AUTH, ZCARR, ACTVT = '03' );
}
```

### Multiple Conditions

```cds
define role ZI_Travel {
  grant select on ZI_Travel
    where ( carrier_id ) =
      aspect pfcg_auth ( Z_MY_AUTH, ZCARR, ACTVT = '03' )
      and ( agency_id ) =
      aspect pfcg_auth ( Z_AGENCY_AUTH, ZAGENCY, ACTVT = '03' );
}
```

### Unrestricted Access

```cds
define role ZI_Travel_Admin {
  grant select on ZI_Travel
    where _unrestrictedAccess;
}
```

### Inherited Access Control

```cds
"Child entity inherits access control from parent
define role ZI_Booking {
  grant select on ZI_Booking
    where ( carrier_id ) =
      aspect pfcg_auth ( Z_MY_AUTH, ZCARR, ACTVT = '03' );
}
```

### DCL and PRIVILEGED ACCESS

```abap
"Bypass DCL access control when needed (e.g., in background jobs)
SELECT FROM zi_travel
  FIELDS travel_id, description
  INTO TABLE @DATA(lt_all)
  PRIVILEGED ACCESS.
```

## IAM in ABAP Cloud

### IAM App

Created in ADT, links a service binding to the authorization model:

```
ADT: New → Other → IAM App
Name: Z_TRAVEL_IAM
Type: EXT - External App (for OData services)
Service Binding: ZUI_TRAVEL_O4
```

Assign authorization objects to the IAM App to define which checks apply.

### Business Catalog

Groups IAM Apps into logical bundles:

```
ADT: New → Other → Business Catalog
Name: Z_BC_TRAVEL_MGMT
Description: Travel Management
IAM Apps: Z_TRAVEL_IAM, Z_BOOKING_IAM
```

### Business Role

Created in Fiori app "Maintain Business Roles":

1. Create new business role (e.g., `Z_BR_TRAVEL_MANAGER`)
2. Add business catalogs
3. Configure restriction types (field-level access)
4. Assign business users

### Restriction Types

Define field-level restrictions in business roles:

| Restriction Type | Description                               |
| ---------------- | ----------------------------------------- |
| **Unrestricted** | Full access to all values                 |
| **Restricted**   | Access limited to specified values        |
| **No Access**    | No access to the associated functionality |

Example: A travel manager role might restrict `ZCARR` to only `LH` and `AA`.

## On-Premise: PFCG Roles

### Creating a PFCG Role

1. Open `PFCG` transaction
2. Enter role name (e.g., `Z_TRAVEL_DISPLAY`)
3. **Menu tab**: Add transaction codes, Fiori tiles, or apps
4. **Authorizations tab**: Maintain authorization values
   - Set authorization objects and field values
   - Generate the authorization profile
5. **User tab**: Assign users to the role

### Composite Roles

Bundle multiple single roles:

```
Z_TRAVEL_COMPOSITE (Composite Role)
├── Z_TRAVEL_DISPLAY (Single Role — display only)
├── Z_TRAVEL_EDIT (Single Role — create/change)
└── Z_TRAVEL_ADMIN (Single Role — full access)
```

## RAP Authorization

### Instance Authorization in RAP

```abap
"In behavior definition:
define behavior for ZR_Travel alias Travel
  authorization master ( instance )
{
  ...
}
```

```abap
"In behavior implementation:
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

### Global Authorization in RAP

```abap
"In behavior definition:
define behavior for ZR_Travel alias Travel
  authorization master ( global )
{
  ...
}
```

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

## Output Format

When helping with authorization/IAM topics, structure responses as:

```markdown
## Authorization Guidance

### Platform

- [ABAP Cloud / On-Premise]
- Approach: [CDS DCL / AUTHORITY-CHECK / CL_ABAP_AUTHORIZATION / IAM]

### Implementation

[Step-by-step with code examples]

### Role Configuration

[How to set up roles and assign access]
```

## References

- ABAP Authorization Cheat Sheet: https://github.com/SAP-samples/abap-cheat-sheets
- CDS Access Control: https://help.sap.com/docs/abap-cloud/abap-development-tools-user-guide/access-controls
- IAM Guide: https://help.sap.com/docs/btp/sap-business-technology-platform/identity-and-access-management-iam
