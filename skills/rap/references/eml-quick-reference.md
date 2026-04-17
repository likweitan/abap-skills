# EML (Entity Manipulation Language) Quick Reference

Detailed EML syntax examples for all standard operations.

## Create

```abap
" Short form
MODIFY ENTITY zr_root
  CREATE FIELDS ( Description Status )
  WITH VALUE #( ( %cid = 'cid1'
                  Description = 'New Item'
                  Status = 'NEW' ) )
  MAPPED DATA(mapped)
  FAILED DATA(failed)
  REPORTED DATA(reported).

" Long form
MODIFY ENTITIES OF zr_root
  ENTITY Root
  CREATE FROM VALUE #(
    ( %cid = 'cid1'
      Description = 'New Item'
      %control = VALUE #(
        Description = if_abap_behv=>mk-on
        Status = if_abap_behv=>mk-on ) ) )
  MAPPED DATA(mapped)
  FAILED DATA(failed)
  REPORTED DATA(reported).
```

## Read

```abap
READ ENTITIES OF zr_root
  ENTITY Root
  ALL FIELDS WITH VALUE #( ( RootUUID = some_uuid ) )
  RESULT DATA(result)
  FAILED DATA(failed)
  REPORTED DATA(reported).
```

## Update

```abap
MODIFY ENTITY zr_root
  UPDATE FIELDS ( Description )
  WITH VALUE #( ( %tky = entity-%tky
                  Description = 'Updated' ) )
  FAILED DATA(failed)
  REPORTED DATA(reported).
```

## Delete

```abap
MODIFY ENTITY zr_root
  DELETE FROM VALUE #( ( %tky = entity-%tky ) )
  FAILED DATA(failed)
  REPORTED DATA(reported).
```

## Execute Action

```abap
MODIFY ENTITY zr_root
  EXECUTE doSomething FROM VALUE #( ( %tky = entity-%tky ) )
  RESULT DATA(action_result)
  FAILED DATA(failed)
  REPORTED DATA(reported).
```

## Create-by-Association (Deep Create)

```abap
MODIFY ENTITIES OF zr_root
  ENTITY Root
  CREATE FIELDS ( Description ) WITH VALUE #(
    ( %cid = 'cid_root' Description = 'Parent' ) )
  CREATE BY \_Child
  FIELDS ( ItemDesc Amount ) WITH VALUE #(
    ( %cid_ref = 'cid_root'
      %target = VALUE #(
        ( %cid = 'cid_child1' ItemDesc = 'Item 1' Amount = 100 )
        ( %cid = 'cid_child2' ItemDesc = 'Item 2' Amount = 200 ) ) ) )
  MAPPED DATA(mapped)
  FAILED DATA(failed)
  REPORTED DATA(reported).
```

## Commit & Rollback

```abap
" Persist changes to database
COMMIT ENTITIES.
IF sy-subrc <> 0.
  " Handle error
ENDIF.

" Discard all changes
ROLLBACK ENTITIES.
```

## Draft EML Example

```abap
" Create a draft instance
MODIFY ENTITY zr_root
  CREATE AUTO FILL CID
  FIELDS ( Description )
  WITH VALUE #( ( %is_draft = if_abap_behv=>mk-on
                  Description = 'Draft Item' ) )
  MAPPED DATA(mapped)
  FAILED DATA(failed)
  REPORTED DATA(reported).
```
