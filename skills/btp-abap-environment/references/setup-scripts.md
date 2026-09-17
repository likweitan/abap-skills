# BTP ABAP Environment Setup Scripts

Reference scripts and commands for setting up and configuring SAP BTP ABAP Environment.

## Service Instance Creation

### JSON Configuration Template
```json
{
  "admin_email": "admin@example.com",
  "description": "Development ABAP System",
  "is_development_allowed": true,
  "sapsystemname": "DEV",
  "size_of_runtime": 1,
  "size_of_persistence": 4,
  "size_of_licenses": 1,
  "whitelisted_domains": ["example.com"],
  "users": [
    {
      "email": "developer@example.com",
      "roles": ["Developer"]
    }
  ]
}
```

### Cloud Foundry CLI Commands
```bash
# Login to Cloud Foundry
cf login -a https://api.cf.us10.hana.ondemand.com -o <org> -s <space>

# Create ABAP Environment service instance
cf create-service abap standard my-abap-instance -c config.json

# Create service key for ADT connectivity
cf create-service-key my-abap-instance my-key

# View service key
cf service-key my-abap-instance my-key

# Delete service instance
cf delete-service my-abap-instance
```

## Software Component Management

### Software Component Creation
```abap
"Via Fiori App: Manage Software Components
"Alternatively, via ABAP code
DATA(lo_component) = cl_swbm_component=>create_instance( ).
lo_component->create(
  iv_name        = 'Z_MY_COMPONENT'
  iv_description  = 'My Custom Component'
  iv_type        = 'DEVELOPMENT' ).
```

### Component Cloning
```bash
# Clone component for use in ADT
# Via Fiori app: Manage Software Components
# Select component → Clone
```

## Communication Arrangement Setup

### Communication Scenario Definition
```abap
"Via ADT: New → Other → Communication Scenario
"Name: Z_MY_COMM_SCENARIO
"Type: Managed by Customer

"Properties:
"- Scenario ID: Z_MY_COMM_SCENARIO
"- Scenario Type: Managed by Customer
"- Inbound Services: List of OData services
"- Outbound Services: List of HTTP services
"- Allowed Auth Methods: Basic, OAuth 2.0, x.509
```

### Communication System Configuration
```abap
"Via Fiori app: Communication Systems
"System ID: Z_EXT_SYSTEM
"Host Name: api.example.com
"Port: 443
"Protocol: HTTPS
```

### Communication Arrangement Creation
```abap
"Via Fiori app: Communication Arrangements
"Scenario: Z_MY_COMM_SCENARIO
"Communication System: Z_EXT_SYSTEM
"Communication User: Z_COMM_USER
"Service IDs: Z_MY_OUTBOUND_SERVICE
```

## IAM Setup Scripts

### IAM App Creation
```abap
"Via ADT: New → Other → IAM App
"Name: Z_MY_APP_IAM
"Type: EXT - External App
"Service Binding: Z_MY_SERVICE_BINDING
"Authorization Objects: Z_MY_AUTH
```

### Business Catalog Creation
```abap
"Via ADT: New → Other → Business Catalog
"Name: Z_BC_MY_APP
"Description: My Application Catalog
"IAM Apps: Z_MY_APP_IAM, Z_OTHER_APP_IAM
```

### Business Role Setup
```abap
"Via Fiori app: Maintain Business Roles
"Role Name: Z_BR_MY_APP_USER
"Business Catalogs: Z_BC_MY_APP
"Restriction Types:
"  - Field: ZCARR, Type: Restricted, Values: 'LH', 'AA'
"  - Field: ACTVT, Type: Restricted, Values: '03', '02'
```

## Outbound Communication Setup

### HTTP Destination Configuration
```abap
"Using Communication Arrangement
DATA(lo_dest) = cl_http_destination_provider=>create_by_comm_arrangement(
  comm_scenario  = 'Z_MY_COMM_SCENARIO'
  service_id     = 'Z_MY_HTTP_SERVICE' ).

"Alternative: Direct URL
DATA(lo_dest) = cl_http_destination_provider=>create_by_url(
  'https://api.example.com' ).
```

### HTTP Client Example
```abap
DATA(lo_client) = cl_web_http_client_manager=>create_by_http_destination( lo_dest ).
DATA(lo_request) = lo_client->get_http_request( ).

"Set request properties
lo_request->set_uri_path( '/api/resource' ).
lo_request->set_header_field( i_name = 'Content-Type' i_value = 'application/json' ).
lo_request->set_text( '{"key":"value"}' ).

"Execute request
DATA(lo_response) = lo_client->execute( if_web_http_client=>get ).
DATA(lv_status) = lo_response->get_status( ).
DATA(lv_body) = lo_response->get_text( ).

lo_client->close( ).
```

## Inbound Communication Setup

### OData Service Binding
```abap
"Via ADT: New → Other ABAP Repository Object → Business Services → Service Binding
"Service Definition: Z_MY_SERVICE
"Binding Type: OData V4 - UI
"Activate and Publish
```

### Service Testing
```bash
# Test OData service
curl -X GET "https://<host>/sap/opu/odata4/sap/z_my_service/0001/EntitySet" \
  -H "Authorization: Basic <base64-encoded-credentials>"
```

## User and Role Assignment

### User Creation
```abap
"Via Fiori app: Maintain Business Users
"User: <email@example.com>
"Type: Business User
"Authentication: Default
```

### Role Assignment
```abap
"Via Fiori app: Assign Business Roles
"User: <email@example.com>
"Roles: Z_BR_MY_APP_USER, Z_BR_OTHER_ROLE
```

## Troubleshooting Scripts

### Connection Test
```abap
"Test HTTP destination
TRY.
    DATA(lo_dest) = cl_http_destination_provider=>create_by_url( 'https://api.example.com' ).
    DATA(lo_client) = cl_web_http_client_manager=>create_by_http_destination( lo_dest ).
    DATA(lo_response) = lo_client->execute( if_web_http_client=>get ).
    WRITE: / 'Connection successful:', lo_response->get_status( ).
    lo_client->close( ).
  CATCH cx_web_http_client_error INTO DATA(lx_error).
    WRITE: / 'Connection failed:', lx_error->get_text( ).
ENDTRY.
```

### Service Instance Status Check
```bash
# Check service instance status
cf service my-abap-instance

# Check service instance logs
cf logs my-abap-instance --recent

# Check service instance health
cf health my-abap-instance
```

## Common Configuration Files

### abaplint.json for BTP
```json
{
  "global": {
    "files": "/src/**/*.*",
    "skip": []
  },
  "syntax": {
    "version": "Cloud",
    "errorNamespace": "^(Z|Y|LCL_|LIF_)"
  },
  "rules": {
    "description": "ABAP lint configuration for BTP"
  }
}
```

### .abapgit.xml for BTP
```xml
<?xml version="1.0" encoding="utf-8"?>
<asx:abap xmlns:asx="http://www.sap.com/abapxml" version="1.0">
 <asx:values>
  <DATA>
   <MASTER_LANGUAGE>E</MASTER_LANGUAGE>
   <STARTING_FOLDER>/src/</STARTING_FOLDER>
   <FOLDER_LOGIC>PREFIX</FOLDER_LOGIC>
   <IGNORE>
    <item>/.gitignore</item>
    <item>/LICENSE</item>
    <item>/README.md</item>
   </IGNORE>
   <REQUIREMENTS/>
  </DATA>
 </asx:values>
</asx:abap>
```

## Security Configuration

### SSL Certificate Setup
```bash
# Import SSL certificates via STRUST transaction
# Navigate to: SSL Client (Anonymous) or SSL Client (Standard)
# Import root certificates for Git providers
```

### OAuth 2.0 Configuration
```abap
"Via Communication Arrangement
"Auth Method: OAuth 2.0
"Token Service URL: https://oauth.example.com/oauth/token
"Client ID: <client-id>
"Client Secret: <client-secret>
```

## Monitoring and Logging

### Application Log Setup
```abap
"Create application log
DATA(lo_log) = cl_bali_log=>create( ).
lo_log->set_header( 
  i_object = 'Z_BTP_APP'
  i_subobj  = 'MONITORING' ).
```

### Error Monitoring
```abap
"Error handling with logging
TRY.
    "Your code here
  CATCH cx_root INTO DATA(lx_error).
    DATA(lo_log) = cl_bali_log=>create( ).
    lo_log->set_header( i_object = 'Z_BTP_APP' i_subobj = 'ERRORS' ).
    lo_log->add_exception( lx_error ).
    lo_log->save( ).
ENDTRY.
```

## Performance Optimization

### Connection Pooling
```abap
"Use connection pooling for HTTP clients
DATA(lo_client) = cl_web_http_client_manager=>create_by_http_destination(
  lo_dest )->keep_alive( ).
```

### Caching Strategy
```abap
"Implement caching for frequently accessed data
DATA(lo_cache) = cl_abap_memory_utilities=>get_instance( ).
DATA(lv_cached) = lo_cache->get( 'MY_CACHE_KEY' ).
```

## Backup and Recovery

### Export Configuration
```bash
# Export service configuration
cf export-service my-abap-instance

# Export service key
cf service-key my-abap-instance my-key > service-key.json
```

### Import Configuration
```bash
# Import service configuration
cf import-service my-abap-instance -c config.json

# Import service key
cf update-service-key my-abap-instance my-key -c service-key.json
```

## Development Workflow

### Local Development Setup
```bash
# Set up local development environment
# 1. Install ADT (ABAP Development Tools) in Eclipse
# 2. Configure connection to BTP ABAP system
# 3. Clone abapGit repository
# 4. Set up project structure
```

### Deployment Pipeline
```yaml
# Example CI/CD pipeline
stages:
  - lint
  - build
  - deploy

lint:
  script:
    - abaplint

build:
  script:
    - abap build

deploy:
  script:
    - abap deploy
    - cf push
```

## Maintenance Tasks

### Regular Maintenance
```bash
# Check service instance health
cf service my-abap-instance

# Update service instance
cf update-service my-abap-instance -c new-config.json

# Rotate service keys
cf delete-service-key my-abap-instance old-key
cf create-service-key my-abap-instance new-key
```

### Monitoring
```abap
"Check system status
SELECT * FROM i_systemhealth
  WHERE component = 'ABAP Environment'
  INTO TABLE @DATA(lt_health).
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: Connection Timeout
```abap
"Solution: Increase timeout
DATA(lo_dest) = cl_http_destination_provider=>create_by_url( 'https://api.example.com' ).
DATA(lo_client) = cl_web_http_client_manager=>create_by_http_destination( lo_dest ).
lo_client->set_timeout( 300 ). "5 minutes
```

#### Issue: Authorization Failure
```abap
"Solution: Check communication arrangement
"Verify: Scenario, System, User configuration
"Check: Authorizations, OAuth tokens
```

#### Issue: Service Binding Not Working
```abap
"Solution: Re-publish service binding
"1. Check service binding is active
"2. Click 'Publish' again
"3. Verify ICF nodes are active
"4. Check authorizations
```