# RAP Business Event Patterns Reference

Common event-driven patterns and implementations for RAP business events in ABAP Cloud.

## Event Definition Patterns

### Pattern 1: Simple Event (No Payload)
```abap
"Behavior Definition
managed implementation in class zbp_r_travel unique;
strict ( 2 );

define behavior for ZR_Travel alias Travel
persistent table ztravel_tab
lock master
authorization master ( instance )
{
  create;
  update;
  delete;

  "Simple event with no payload
  event travel_created;
  event travel_accepted;
  event travel_rejected;
}
```

### Pattern 2: Event with Parameters
```abap
"Behavior Definition
event travel_created parameter ZD_TravelCreatedEvt;
event status_changed parameter ZD_StatusChangedEvt;

"Event Parameter Structure (CDS Abstract Entity)
@EndUserText.label: 'Travel Created Event'
define abstract entity ZD_TravelCreatedEvt
{
  travel_id   : /dmo/travel_id;
  agency_id   : /dmo/agency_id;
  customer_id : /dmo/customer_id;
  description : /dmo/description;
  total_price : /dmo/total_price;
  currency    : /dmo/currency_code;
}
```

### Pattern 3: Complex Event Structure
```abap
"Event with nested structure
define abstract entity ZD_ComplexEvent
{
  header_id   : abap.char(10);
  header_data : ZD_HeaderData;
  items       : ZD_EventItems;
}

define abstract entity ZD_HeaderData
{
  field1 : abap.char(10);
  field2 : abap.char(20);
}

define abstract entity ZD_EventItems
{
  item_id  : abap.char(10);
  quantity : abap.int4;
}
```

## Event Raising Patterns

### Pattern 1: Event in Handler Method
```abap
METHOD on_travel_accept.
  "Read travel data
  READ ENTITIES OF zr_travel IN LOCAL MODE
    ENTITY Travel
    ALL FIELDS WITH CORRESPONDING #( keys )
    RESULT DATA(lt_travels).

  "Update status
  MODIFY ENTITIES OF zr_travel IN LOCAL MODE
    ENTITY Travel
    UPDATE FIELDS ( status )
    WITH VALUE #( FOR travel IN lt_travels
      ( %tky = travel-%tky
        status = 'A' ) )
    REPORTED DATA(lt_reported).

  "Raise event for each accepted travel
  RAISE ENTITY EVENT zr_travel~travel_accepted
    FROM VALUE #( FOR travel IN lt_travels
      ( %key = travel-%key ) ).
ENDMETHOD.
```

### Pattern 2: Event with Parameters
```abap
METHOD on_travel_create.
  "After successful creation
  RAISE ENTITY EVENT zr_travel~travel_created
    FROM VALUE #( FOR travel IN lt_created_travels
      ( %key = travel-%key
        %param = VALUE #(
          travel_id   = travel-travel_id
          agency_id   = travel-agency_id
          customer_id = travel-customer_id
          description = travel-description
          total_price = travel-total_price
          currency    = travel-currency_code ) ) ).
ENDMETHOD.
```

### Pattern 3: Event in Saver Method
```abap
METHOD save_modified.
  "Raise events in the save phase for committed data
  IF create-travel IS NOT INITIAL.
    RAISE ENTITY EVENT zr_travel~travel_created
      FROM VALUE #( FOR travel IN create-travel
        ( %key = travel-%key
          %param = VALUE #(
            travel_id = travel-travel_id ) ) ).
  ENDIF.
ENDMETHOD.
```

## Event Consumption Patterns

### Pattern 1: Local Event Handler
```abap
CLASS zcl_travel_event_handler DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    "Event handler method
    METHODS on_travel_created
      FOR ENTITY EVENT
      travel_created FOR Travel~travel_created.
ENDCLASS.

CLASS zcl_travel_event_handler IMPLEMENTATION.
  METHOD on_travel_created.
    "React to travel creation
    LOOP AT travel_created INTO DATA(ls_event).
      "Process event data
      DATA(lv_travel_id) = ls_event-travel_id.
      "e.g., send notification, update related records
    ENDLOOP.
  ENDMETHOD.
ENDCLASS.
```

### Pattern 2: External Event Consumption
```abap
"Using event consumption model
"1. Create event consumption model in ADT
"   (imports AsyncAPI spec or defines events manually)

"2. Implement the event handler
CLASS zcl_ext_event_handler DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_event_handler.
ENDCLASS.

CLASS zcl_ext_event_handler IMPLEMENTATION.
  METHOD if_event_handler~handle.
    "Parse event payload
    DATA(lv_payload) = io_event->get_text( ).
    "Process the event
  ENDMETHOD.
ENDCLASS.
```

## Event Binding Patterns

### Pattern 1: Basic Event Binding
```
ADT: New → Other → Event Binding
Name: Z_EVT_BIND_TRAVEL

Properties:
- Namespace: sap.s4.beh
- Business Object: ZR_Travel
- Event: travel_created
- Topic: sap/s4/beh/travel/created/v1
```

### Pattern 2: Custom Namespace
```
Properties:
- Namespace: z.custom
- Business Object: ZR_Travel
- Event: travel_created
- Topic: z/custom/travel/created/v1
```

## Event Architecture Patterns

### Pattern 1: Fire and Forget
```abap
"Producer raises event → Event Mesh delivers → Consumer processes independently
RAISE ENTITY EVENT zr_travel~travel_created
  FROM VALUE #( ( %key = ls_travel-%key ) ).

"No response expected
"Loose coupling between systems
```

### Pattern 2: Event-Carried State Transfer
```abap
"Include full entity data in event payload
RAISE ENTITY EVENT zr_travel~travel_created
  FROM VALUE #( ( %key = ls_travel-%key
                  %param = CORRESPONDING #( ls_travel ) ) ).

"Consumers don't need to call back for data
```

### Pattern 3: Event Sourcing
```abap
"Record every state change as an event
"Full audit trail
"Rebuild state from event stream
```

## Integration Patterns

### Pattern 1: SAP Event Mesh Integration
```abap
"Communication Arrangement for SAP_COM_0092
"Enterprise Event Enablement scenario
"Channel binding in Enterprise Event Enablement Fiori app
```

### Pattern 2: Direct Integration
```abap
"Direct event handler registration
"Local event consumption only
"No external system involvement
```

## Common Event Scenarios

### Scenario 1: Status Change Events
```abap
"Event: status_changed
"Payload: old_status, new_status, changed_by, changed_at
"Use Case: Notify stakeholders, trigger workflows
```

### Scenario 2: Data Validation Events
```abap
"Event: validation_failed
"Payload: field_name, error_message, validation_rule
"Use Case: Error tracking, alerting
```

### Scenario 3: Business Process Events
```abap
"Event: process_completed
"Payload: process_id, completion_status, duration
"Use Case: Process monitoring, SLA tracking
```

## Error Handling Patterns

### Pattern 1: Event Failure Handling
```abap
TRY.
    RAISE ENTITY EVENT zr_travel~travel_created
      FROM VALUE #( ( %key = ls_travel-%key ) ).
  CATCH cx_root INTO DATA(lx_error).
    "Log event failure
    DATA(lo_log) = cl_bali_log=>create( ).
    lo_log->set_header( i_object = 'Z_EVENT' i_subobj = 'ERROR' ).
    lo_log->add_exception( lx_error ).
    lo_log->save( ).
ENDTRY.
```

### Pattern 2: Retry Logic
```abap
"Implement retry for event delivery
DATA(lv_retry_count) = 0.
WHILE lv_retry_count < 3.
  TRY.
      RAISE ENTITY EVENT zr_travel~travel_created
        FROM VALUE #( ( %key = ls_travel-%key ) ).
      EXIT.
    CATCH cx_root.
      lv_retry_count = lv_retry_count + 1.
      WAIT UP TO 2 SECONDS.
  ENDWHILE.
ENDWHILE.
```

## Testing Patterns

### Pattern 1: Unit Test for Event Handler
```abap
CLASS ltc_event_handler DEFINITION FINAL FOR TESTING
  DURATION SHORT RISK LEVEL HARMLESS.
  PRIVATE SECTION.
    DATA mo_handler TYPE REF TO zcl_travel_event_handler.
    METHODS setup.
    METHODS test_travel_created FOR TESTING.
ENDCLASS.

CLASS ltc_event_handler IMPLEMENTATION.
  METHOD setup.
    mo_handler = NEW zcl_travel_event_handler( ).
  ENDMETHOD.

  METHOD test_travel_created.
    "Arrange
    DATA(lt_events) = VALUE #(
      ( travel_id = '001' agency_id = 'A001' ) ).

    "Act
    mo_handler->on_travel_created( lt_events ).

    "Assert
    "Verify event was processed correctly
  ENDMETHOD.
ENDCLASS.
```

### Pattern 2: Integration Test for Event Flow
```abap
"Test complete event flow
"1. Trigger business operation
"2. Verify event is raised
"3. Verify event handler is called
"4. Verify side effects
```

## Performance Considerations

### Optimization Tips
- Minimize event payload size
- Use event-carried state transfer to avoid callbacks
- Batch events when possible
- Monitor event delivery performance
- Use asynchronous processing for handlers

### Common Performance Issues
- Too many events in single transaction
- Large event payloads
- Synchronous event handlers blocking
- Missing event filters

## Security Considerations

### Event Security
- Implement authorization checks in event handlers
- Validate event payloads
- Use secure communication channels
- Audit event access
- Implement event filtering

### Data Privacy
- Sanitize sensitive data in event payloads
- Use encryption for sensitive events
- Implement data retention policies
- Comply with GDPR requirements

## Monitoring and Logging

### Event Monitoring
```abap
"Log event raising
DATA(lo_log) = cl_bali_log=>create( ).
lo_log->set_header( i_object = 'Z_EVENT' i_subobj = 'MONITORING' ).
lo_log->add_message(
  i_msgty = 'I'
  i_text  = |Event travel_created raised for travel { lv_travel_id }| ).
lo_log->save( ).
```

### Event Metrics
```abap
"Track event delivery times
DATA(lv_start_time) = cl_abap_context_info=>get_system_time( ).
"Raise event...
DATA(lv_end_time) = cl_abap_context_info=>get_system_time( ).
DATA(lv_duration) = lv_end_time - lv_start_time.
```

## Best Practices

### Event Design
- Use meaningful event names
- Keep event payloads focused
- Document event contracts
- Version event topics
- Use consistent naming conventions

### Event Implementation
- Raise events after validation
- Use appropriate event timing (handler vs saver)
- Implement proper error handling
- Test event handlers independently
- Monitor event delivery

### Event Consumption
- Implement idempotent handlers
- Handle event ordering
- Implement retry logic
- Monitor consumer performance
- Document event processing logic

## Common Pitfalls

### Pitfalls to Avoid
- Raising events before data is committed
- Including too much data in event payloads
- Implementing synchronous event handlers
- Missing error handling in event handlers
- Not considering event ordering

### Troubleshooting Tips
- Check event binding configuration
- Verify communication arrangement
- Test event handler in isolation
- Monitor Event Mesh logs
- Check authorization for event delivery

## Migration Patterns

### Classic to RAP Event Migration
```abap
"Classic: BAdI or user exit
"New: RAP business event

"Migration steps:
"1. Identify classic event points
"2. Create RAP events
"3. Implement event handlers
"4. Set up event bindings
"5. Test and validate
```

## Cross-Reference

### Related Skills
- Use `rap` skill for behavior definitions
- Use `authorization-iam` skill for event security
- Use `btp-abap-environment` skill for Event Mesh setup