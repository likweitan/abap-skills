# OData Annotation Examples

Common OData annotations and examples for ABAP Cloud development.

## OData V4 Annotations

### Basic Service Annotations
```cds
@EndUserText.label: 'Travel Service'
define service ZUI_TRAVEL_O4 {
  expose ZC_Travel as Travel;
  expose ZC_Booking as Booking;
}
```

### Entity Set Annotations
```cds
@UI.headerInfo: {
  typeName: 'Travel',
  typeNamePlural: 'Travels',
  title: { type: #STANDARD, value: 'TravelID' }
}
```

## RAP Service Binding Annotations

### OData V4 UI Binding
```cds
@EndUserText.label: 'Travel Service'
define service ZUI_TRAVEL_O4 {
  expose ZC_Travel as Travel;
  expose ZC_Booking as Booking;
}
```

### OData V2 UI Binding
```cds
@EndUserText.label: 'Travel Service V2'
define service ZUI_TRAVEL_O2 {
  expose ZC_Travel as Travel;
  expose ZC_Booking as Booking;
}
```

## Common OData Annotations

### Capabilities
```cds
@Capabilities.insertable: true
@Capabilities.updatable: true
@Capabilities.deletable: true
@Capabilities.searchable: true
```

### Search Capabilities
```cds
@Search.searchable: true
@Search.defaultSearchElement: true
description as Description,
```

### Filter Restrictions
```cds
@Consumption.filter.valueSelection: #SINGLE
status as Status,
```

## Navigation Properties

### Association Navigation
```cds
@UI.identification: [{ position: 30 }]
_Customer as Customer,
```

### Navigation Property Binding
```cds
"Automatically exposed via association
association [0..1] to ZI_Customer as _Customer
  on $projection.CustomerId = _Customer.CustomerId
```

## Draft Annotations

### Draft Handling
```cds
@UI.draftIndicator: true
@UI.hidden: true
 IsActiveEntity as IsActiveEntity,
```

### Draft Actions
```cds
"Automatically provided with draft-enabled BO
"Draft actions: Edit, Activate, Discard, Resume
```

## Action Annotations

### Bound Actions
```cds
@UI.identification: [{ position: 40, type: #FOR_ACTION }]
action acceptTravel result [1] $self;
```

### Static Actions
```cds
@UI.identification: [{ position: 50, type: #FOR_ACTION }]
static action createFromTemplate parameter ZD_Template result [1] $self;
```

## Common Patterns

### Complete Service Definition
```cds
@EndUserText.label: 'Travel Management Service'
define service ZUI_TRAVEL_MGMT {
  expose ZC_Travel as Travel;
  expose ZC_Booking as Booking;
  expose I_Currency as Currency;
  expose I_Country as Country;
  
  "Value help entities
  expose I_BookingStatus as BookingStatus;
  expose I_TravelStatus as TravelStatus;
}
```

### Metadata Extension for UI
```cds
@Metadata.layer: #CUSTOMER
annotate view ZC_Travel with
{
  @UI.facet: [{
    id: 'GeneralInfo',
    type: #IDENTIFICATION_REFERENCE,
    label: 'General Information',
    position: 10
  }]
  
  @UI.lineItem: [{ position: 10, importance: #HIGH }]
  @UI.identification: [{ position: 10 }]
  @UI.selectionField: [{ position: 10 }]
  TravelID;
  
  @UI.lineItem: [{ position: 20 }]
  @UI.identification: [{ position: 20 }]
  @UI.selectionField: [{ position: 20 }]
  CustomerID;
  
  @UI.lineItem: [{ position: 30 }]
  @UI.identification: [{ position: 30 }]
  BeginDate;
  
  @UI.lineItem: [{ position: 40 }]
  @UI.identification: [{ position: 40 }]
  EndDate;
  
  @UI.lineItem: [{ position: 50 }]
  @UI.identification: [{ position: 50 }]
  TotalPrice;
};
```

## Error Handling Annotations

### Error Response
```cds
"Automatic error response via RAP framework
"No specific annotations needed
```

### Custom Error Messages
```abap
"In behavior implementation
APPEND VALUE #(
  %tky = ls_travel-%tky
  %msg = new_message_with_text(
    severity = if_abap_behv_message=>severity-error
    text = 'Travel dates are invalid' )
  %element-BeginDate = if_abap_behv=>mk-on
) TO reported-travel.
```

## Pagination Annotations

### Server-Driven Pagination
```cds
"Automatically handled by OData service
"No specific annotations needed
```

### Custom Pagination
```cds
"Use $top and $skip query parameters
"Example: /Travel?$top=10&$skip=20
```

## Performance Annotations

### Optimized Loading
```cds
@UI.hidden: true
internal_field as InternalField,
```

### Lazy Loading
```cds
"Associations are lazily loaded by default
"Use $expand to load related entities
"Example: /Travel?$expand=_Customer
```

## Security Annotations

### Authorization
```cds
@AccessControl.authorizationCheck: #CHECK
```

### Restricted Fields
```cds
@UI.hidden: true
sensitive_field as SensitiveField,
```

## Testing Annotations

### Test Data
```cds
"No specific annotations for testing
"Use test environments with mock data
```

## Common OData Query Options

### $select
```abap
"Select specific fields
/Travel?$select=TravelID,CustomerID,BeginDate
```

### $filter
```abap
"Filter results
/Travel?$filter=Status eq 'A'
/Travel?$filter=BeginDate ge 20240101
```

### $orderby
```abap
"Sort results
/Travel?$orderby=BeginDate desc
```

### $top and $skip
```abap
"Pagination
/Travel?$top=10&$skip=20
```

### $expand
```abap
"Expand navigation properties
/Travel?$expand=_Customer
/Travel?$expand=_Customer,_Booking
```

### $search
```abap
"Full-text search
/Travel?$search='vacation'
```

## Service Binding Types

### OData V4 - UI
```cds
"Recommended for Fiori Elements apps
define service ZUI_TRAVEL_O4 {
  expose ZC_Travel as Travel;
}
```

### OData V2 - UI
```cds
"For legacy Fiori apps
define service ZUI_TRAVEL_O2 {
  expose ZC_Travel as Travel;
}
```

### OData V4 - Web API
```cds
"For API consumption (A2X scenarios)
define service ZAPI_TRAVEL_O4 {
  expose ZC_Travel as Travel;
}
```

## Common Issues and Solutions

### Issue: Navigation Not Working
```cds
"Solution: Ensure association is exposed
association [0..1] to ZI_Customer as _Customer
  on $projection.CustomerId = _Customer.CustomerId

"Expose in service definition
expose ZC_Travel as Travel;
"Include _Customer in projection
```

### Issue: Value Help Not Showing
```cds
"Solution: Add value help annotation
@Consumption.valueHelpDefinition: [{
  entity: { name: 'I_Currency', element: 'Currency' }
}]
currency_code as CurrencyCode,

"Expose value help entity in service
expose I_Currency as Currency;
```

### Issue: Actions Not Visible
```cds
"Solution: Add UI identification for actions
@UI.identification: [{ position: 40, type: #FOR_ACTION }]
action acceptTravel result [1] $self;
```

## Best Practices

### Service Design
- Expose projection views, not root views
- Include necessary value help entities
- Use descriptive service names
- Group related entities together

### Performance
- Limit number of exposed entities
- Use appropriate binding types
- Consider field selection in UI annotations
- Optimize CDS views for performance

### Security
- Implement access control on CDS views
- Use authorization checks in behavior
- Hide sensitive fields with UI annotations
- Test with different user roles

## Migration Patterns

### Classic SEGW to RAP Migration
```cds
"Classic SEGW data model
"Entity Types, Associations in SEGW

"RAP equivalent
"Define CDS view entities with associations
"Create behavior definition
"Expose via service definition
```

## Cross-Reference

### Related Skills
- Use `rap` skill for behavior definitions
- Use `cds-view-entities` skill for data modeling
- Use `authorization-iam` skill for security