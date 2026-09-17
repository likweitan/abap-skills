# CDS Annotations Reference

Comprehensive reference for ABAP CDS annotations used in ABAP Cloud development.

## Semantic Annotations

### Amount and Currency
```cds
@Semantics.amount.currencyCode: 'CurrencyCode'
net_amount as NetAmount,

currency_code as CurrencyCode,
```

### Quantity and Unit
```cds
@Semantics.quantity.unitOfMeasure: 'QuantityUnit'
quantity as Quantity,

quantity_unit as QuantityUnit,
```

### User Information
```cds
@Semantics.user.createdBy: true
created_by as CreatedBy,

@Semantics.user.lastChangedBy: true
last_changed_by as LastChangedBy,

@Semantics.user.localInstanceLastChangedBy: true
local_last_changed_by as LocalLastChangedBy,
```

### Date and Time
```cds
@Semantics.systemDateTime.createdAt: true
created_at as CreatedAt,

@Semantics.systemDateTime.localInstanceLastChangedAt: true
local_last_changed_at as LocalLastChangedAt,

@Semantics.systemDateTime.lastChangedAt: true
last_changed_at as LastChangedAt,
```

### Identity and Contact
```cds
@Semantics.identity.uuid: true
customer_uuid as CustomerUUID,

@Semantics.contact: { fullName: true, emailAddress: true }
contact_info as ContactInfo,
```

## UI Annotations

### Header Information
```cds
@UI.headerInfo: {
  typeName: 'Sales Order',
  typeNamePlural: 'Sales Orders',
  title: { type: #STANDARD, value: 'OrderId' },
  description: { type: #STANDARD, value: 'Description' }
}
```

### Line Item
```cds
@UI.lineItem: [{ position: 10, importance: #HIGH }]
@UI.selectionField: [{ position: 10 }]
@UI.identification: [{ position: 10 }]
order_id as OrderId,
```

### Facets
```cds
@UI.facet: [{
  id: 'GeneralInfo',
  type: #IDENTIFICATION_REFERENCE,
  label: 'General Information',
  position: 10
}]
```

### Field Group
```cds
@UI.fieldGroup: [{
  id: 'CustomerInfo',
  label: 'Customer Information',
  position: 10,
  importance: #HIGH
}]
```

### Hidden Fields
```cds
@UI.hidden: true
internal_field as InternalField,
```

### Read-Only Fields
```cds
@UI.readOnly: true
created_at as CreatedAt,
```

### Multi-Line Text
```cds
@UI.multiLineText: true
description as Description,
```

## Consumption Annotations

### Value Help
```cds
@Consumption.valueHelpDefinition: [{
  entity: { name: 'I_Currency', element: 'Currency' }
}]
currency_code as CurrencyCode,
```

### Filter Values
```cds
@Consumption.filter.valueSelection: #SINGLE
status as Status,
```

### Hidden in Filters
```cds
@Consumption.filter.hidden: true
internal_field as InternalField,
```

### Semantic Object
```cds
@Consumption.semanticObject: 'SalesOrder'
order_id as OrderId,
```

## Analytics Annotations

### Default Aggregation
```cds
@Analytics.defaultAggregation: #SUM
amount as Amount,
```

### Measures
```cds
@Analytics: { measure: true }
amount as Amount,
```

### Dimensions
```cds
@Analytics: { dimension: true }
category as Category,
```

### Calculated Measures
```cds
@Analytics: { calculated: true }
calculated_field as CalculatedField,
```

## Object Model Annotations

### Lifecycle
```cds
@ObjectModel.lifecycle.archiving.active: true
order_id as OrderId,
```

### Transactions
```cds
@ObjectModel.transaction: {
  enabled: true,
  consistency: #CONSISTENT
}
```

### Support
```cds
@ObjectModel.support.email: 'support@example.com'
```

## VDM Annotations

### Search
```cds
@Search.defaultSearchElement: true
description as Description,
```

### Data Loss
```cds
@ObjectModel.dataLossAnnotation.semanticKey: 'OrderId'
order_id as OrderId,
```

## Access Control Annotations

### Authorization Check
```cds
@AccessControl.authorizationCheck: #CHECK
```

### Privileged Access
```cds
@AccessControl.privilegedAccess: true
```

## Metadata Annotations

### Layer
```cds
@Metadata.layer: #CUSTOMER
```

### Allow Extensions
```cds
@Metadata.allowExtensions: true
```

## End User Text Annotations

### Label
```cds
@EndUserText.label: 'Sales Order'
```

### Quick Info
```cds
@EndUserText.quickInfo: 'Order Information'
```

## Common Annotation Patterns

### Complete Field Annotation Set
```cds
@UI.lineItem: [{ position: 10, importance: #HIGH }]
@UI.identification: [{ position: 10 }]
@UI.selectionField: [{ position: 10 }]
@Consumption.valueHelpDefinition: [{
  entity: { name: 'I_Currency', element: 'Currency' }
}]
@Semantics.amount.currencyCode: 'CurrencyCode'
amount as Amount,
```

### Admin Field Pattern
```cds
@UI.hidden: true
@Semantics.user.createdBy: true
created_by as CreatedBy,

@UI.hidden: true
@Semantics.systemDateTime.createdAt: true
created_at as CreatedAt,

@UI.hidden: true
@Semantics.user.localInstanceLastChangedBy: true
last_changed_by as LastChangedBy,

@UI.hidden: true
@Semantics.systemDateTime.localInstanceLastChangedAt: true
local_last_changed_at as LocalLastChangedAt,

@UI.hidden: true
@Semantics.systemDateTime.lastChangedAt: true
last_changed_at as LastChangedAt,
```

### Key Field Pattern
```cds
@UI.identification: [{ position: 10 }]
@ObjectModel.key.element: 'OrderId'
order_id as OrderId,
```

## Metadata Extension Patterns

### Basic Metadata Extension
```cds
@Metadata.layer: #CUSTOMER
annotate view ZC_SalesOrder with
{
  @UI.lineItem: [{ position: 10, importance: #HIGH }]
  @UI.identification: [{ position: 10 }]
  OrderId;

  @UI.lineItem: [{ position: 20 }]
  @UI.identification: [{ position: 20 }]
  CustomerId;
};
```

### Complex Metadata Extension
```cds
@Metadata.layer: #CUSTOMER
annotate view ZC_SalesOrder with
{
  @UI.facet: [{
    id: 'GeneralInfo',
    type: #IDENTIFICATION_REFERENCE,
    label: 'General Information',
    position: 10
  }]

  @UI.identification: [{ position: 10 }]
  OrderId;

  @UI.fieldGroup: [{
    id: 'CustomerInfo',
    label: 'Customer Information',
    position: 10
  }]
  CustomerId;
};
```

## Best Practices

### Annotation Placement
- Place semantic annotations in the view definition
- Place UI annotations in metadata extensions for better maintainability
- Use consistent positioning numbers (10, 20, 30, etc.)
- Group related annotations together

### Naming Conventions
- Use descriptive facet IDs
- Use meaningful label text
- Follow SAP's naming patterns for standard fields
- Keep annotation keys consistent

### Performance Considerations
- Avoid excessive annotations that aren't used
- Use `@UI.hidden` for fields that shouldn't be displayed
- Consider `@Consumption.filter.hidden` for fields that shouldn't be filtered
- Use `@Analytics` annotations judiciously for large datasets

## Migration Patterns

### Classic to CDS Annotation Migration
```cds
"Classic DDIC labels
"Label: 'Sales Order'
"Description: 'Sales Order Number'

"CDS annotations
@EndUserText.label: 'Sales Order'
@EndUserText.quickInfo: 'Sales Order Number'
order_id as OrderId,
```

## Tool-Specific Annotations

### SAP Fiori Elements
```cds
@UI.lineItem: [{ position: 10 }]
@UI.identification: [{ position: 10 }]
@UI.selectionField: [{ position: 10 }]
```

### SAP Analytics Cloud
```cds
@Analytics.defaultAggregation: #SUM
@Analytics: { measure: true }
amount as Amount,
```

### SAP BusinessObjects
```cds
@ObjectModel.lifecycle.archiving.active: true
@ObjectModel.support.email: 'support@example.com'
```

## Common Mistakes

### Incorrect Annotation Syntax
```cds
"Wrong
@UI.lineItem: position: 10

"Correct
@UI.lineItem: [{ position: 10 }]
```

### Missing Required Fields
```cds
"Wrong - missing currency code reference
@Semantics.amount.currencyCode: 'Currency'
amount as Amount,

"Correct
@Semantics.amount.currencyCode: 'CurrencyCode'
amount as Amount,
currency_code as CurrencyCode,
```

### Inconsistent Positioning
```cds
"Wrong - inconsistent gaps
@UI.lineItem: [{ position: 1 }]
@UI.lineItem: [{ position: 5 }]
@UI.lineItem: [{ position: 12 }]

"Correct - consistent increments
@UI.lineItem: [{ position: 10 }]
@UI.lineItem: [{ position: 20 }]
@UI.lineItem: [{ position: 30 }]
```

## Validation and Testing

### Annotation Validation
```abap
"Check annotation syntax in ADT
"Right-click on CDS view → Validate
"Review annotation warnings
```

### Testing Annotations
```abap
"Test in Fiori Elements preview
"Check UI behavior
"Verify value help functionality
"Test filter behavior
```

## Performance Optimization

### Annotation Performance Tips
- Minimize complex annotations
- Use `@UI.hidden` for calculated fields that aren't needed in UI
- Consider using metadata extensions for UI annotations
- Avoid unnecessary `@Analytics` annotations on large datasets

## Future-Proofing

### Annotation Compatibility
- Use standard SAP annotations
- Avoid custom annotations when possible
- Consider future SAP Cloud releases
- Document custom annotation usage

## Cross-Reference

### Related Skills
- Use `rap` skill for behavior definitions
- Use `odata` skill for service binding
- Use `abap-cloud` skill for cloud-specific considerations