# ABAP Cloud Migration Checklist

Step-by-step checklist for raising the **clean core level** of classic ABAP custom code — eliminating Level D, minimizing Level C, and moving toward Level A (ABAP Cloud).

> The former 3-tier model is superseded by the clean core level concept. Success is no longer "everything in Tier 1" but "no Level D, minimal Level C, stable Level B, Level A for new work".

## Pre-Migration Assessment

### 1. System Readiness Check
- [ ] Verify target system supports ABAP for Cloud Development
- [ ] Check SAP Cloud ERP version compatibility
- [ ] Ensure required SAP Notes are implemented
- [ ] Verify ATC Cloud Readiness check variant is available

### 2. Code Inventory
- [ ] Identify all custom code packages to migrate
- [ ] List all custom database tables
- [ ] Document all function modules used
- [ ] Catalog all BAPI calls
- [ ] Identify all dynpro/screen transactions
- [ ] List all classic BAdI implementations
- [ ] Document all external system integrations

## ATC Clean Core Analysis

### 3. Set up ATC governance
- [ ] Set up a central ATC system (SAP BTP recommended, or private cloud/on-premise)
- [ ] Create one global check variant from `ABAP_CLEAN_CORE_DEVELOPMENT` or `ABAP_CLOUD_DEVELOPMENT_DEFAULT`
- [ ] Include `SYCM_USAGE_OF_APIS` (released/classic API classification, SQL on SAP tables, form routines)
- [ ] Include `SYCM_ALLOWED_ENH_TECHNOLOGY` (enhancement technology compliance)
- [ ] Include `CI_SEARCH_CUST_MODIFICATIONS` (modifications)
- [ ] Include `CI_CRITICAL_STATEMENTS` (critical statements)
- [ ] Include `SLIN_SEC` (Code Vulnerability Analyzer — additionally recommended)
- [ ] Implement SAP Note 3565942 if clean core checks are missing
- [ ] Configure ATC transport settings to block release on priority 1 and 2 findings

### 4. Run initial ATC check
- [ ] Execute the global clean core check variant on the entire package
- [ ] Export findings to Excel/CSV
- [ ] Map ATC priority to clean core level: P1 → Level D, P2 → Level C, P3 → Level B
- [ ] Determine the current overall level (the lowest level used)
- [ ] Assess overall remediation complexity

### 5. Findings analysis by level
- [ ] **Level D (P1)**: count modifications, implicit/explicit enhancements, table writes, `noAPI` usages, critical statements, form routine calls
- [ ] **Level C (P2)**: count direct table reads, SAP internal API usages
- [ ] **Level B (P3)**: count deprecated API usages, classic API usages
- [ ] Identify incompatible language constructs
- [ ] Document all SAP GUI-dependent statements
- [ ] Cross-reference objects against the Cloudification Repository for successor information

### 6. Import and analyze the changelog for SAP objects
- [ ] Download the Simplification Database file from the SAP Software Download Center
- [ ] Import it via transaction `SYCM`
- [ ] Run the changelog ATC check to detect incompatibly changed internal objects
- [ ] List Level C usages affected by upcoming incompatible changes
- [ ] Prioritize those usages for refactoring before the next upgrade

## Migration Planning

### 7. Choose a transformation option per object
- [ ] **Retire**: unused code (collect usage data with `SUSG`/`SCMON`, analyze in Custom Code Migration app)
- [ ] **Renovate side-by-side**: loosely coupled extensions → SAP Business AI Platform
- [ ] **Renovate on-stack**: tightly coupled extensions worth reimplementing in ABAP Cloud
- [ ] **Adapt**: minimum viable action via ATC quick fixes and Simplification Database

### 8. Prioritization
- [ ] Prioritize **all Level D findings first** — these must be eliminated
- [ ] Then prioritize Level C findings by business criticality and changelog exposure
- [ ] Estimate effort for each finding type
- [ ] Identify dependencies between objects
- [ ] Plan remediation in logical phases

### 9. Replacement strategy
- [ ] Map each non-released API to a released API (Level A) where available
- [ ] Where no released API exists, map to a nominated classic API (Level B)
- [ ] Identify objects requiring wrappers, and record the resulting wrapper level (B or C)
- [ ] Plan alternative approaches for unavailable features
- [ ] Document the target level per object

## Implementation

### 10. Eliminate Level D (mandatory)
- [ ] Remove all modifications → use released or classic BAdIs instead
- [ ] Delete all implicit and explicit enhancement implementations → use BAdIs
- [ ] Remove all direct **write** access to SAP database tables → released or classic APIs
- [ ] Replace all `noAPI` object usages → use successor information from the Cloudification Repository
- [ ] Remove all critical ABAP statements (kernel/system/editor calls, `EXEC SQL`, DB hints, report/Dynpro generation, nametab import/export)
- [ ] Remove all calls to form routines inside SAP programs
- [ ] Replace implementations of SAP-internal-flagged BAdIs
- [ ] Reset modifications from SAP Notes once the correction is part of the core

### 11. Minimize Level C
- [ ] Replace direct **read** access to SAP tables → released or classic CDS views
- [ ] Replace SAP internal function modules and classes → released or classic APIs
- [ ] Migrate classic appends to released extension includes where available
- [ ] For unavoidable internal usage: wrap the object and create a single fine-grained ATC exemption
- [ ] Monitor the changelog for SAP objects for the remaining internal usages

### 12. API replacements (toward Level A)
- [ ] Replace direct table access with released CDS views
- [ ] Replace function modules with released classes
- [ ] Update BAPI calls to RAP APIs, or keep as Level B classic APIs with justification
- [ ] Replace classic language constructs with modern syntax

### 13. Wrapper creation (classic ABAP component)
- [ ] Create wrapper interfaces for non-released APIs
- [ ] Implement wrapper classes in the classic ABAP software component (`HOME`)
- [ ] Wrap non-released data types via `TYPES` in the wrapper's public section — do not copy them
- [ ] For CDS: create a custom CDS view on top of the non-released SAP view; wrap association targets and value help views as needed
- [ ] Release wrappers with the C1 contract (ADT → API State tab)
- [ ] Provide `SU22` data for the wrapper and create `SU22` variants per designated usage
- [ ] Create one fine-grained ATC exemption per wrapper instead of one per call site
- [ ] Record the wrapper's level: B if wrapping a classic API, C if wrapping an internal object
- [ ] Test wrapper functionality
- [ ] Register wrappers for retirement once SAP releases the equivalent API

### 14. UI migration
- [ ] Replace dynpro transactions with Fiori apps (Level B → Level A)
- [ ] Convert selection screens to Fiori Elements
- [ ] Migrate ALV reports to Fiori List Reports
- [ ] Replace classic list output with Fiori UI
- [ ] Migrate SEGW/BOPF/UI5 Fiori app extensions to the newly delivered RAP app where available
- [ ] Consider the RAP generator or the Fiori Business Configuration app wizard for low-effort conversions
- [ ] Keep existing classic UI apps (Level B) until a major change is required

### 15. Language construct updates
- [ ] Replace `CALL TRANSACTION` with RAP actions
- [ ] Convert `SUBMIT` to Application Jobs
- [ ] Remove `WRITE` statements
- [ ] Replace `MESSAGE` with exception handling
- [ ] Convert `CALL FUNCTION ... IN UPDATE TASK` to RAP save
- [ ] Replace `EXEC SQL` with ABAP SQL or AMDP (also a Level D critical statement)

### 16. Stepwise language version transformation
- [ ] Run `ABAP_CLOUD_READINESS` on candidate objects
- [ ] Switch individual objects to ABAP for Cloud Development (code objects: S/4HANA 2019+; DDIC/CDS: 2022+)
- [ ] Move fully compliant objects to the ABAP Cloud software component

## Validation

### 17. Post-remediation ATC verification
- [ ] Re-run the global clean core check variant
- [ ] Verify **zero priority 1 (Level D)** findings remain
- [ ] Verify priority 2 (Level C) findings are minimized and justified
- [ ] Review remaining priority 3 (Level B) findings — no exemptions needed
- [ ] Verify all exemptions are fine-grained and documented
- [ ] Review exemptions in the ATC exemption browser
- [ ] Confirm the new overall clean core level

### 18. Functional testing
- [ ] Execute functional regression tests
- [ ] Test integration points
- [ ] Validate Fiori UI functionality
- [ ] Test wrapper behaviour against original API behaviour

### 19. Performance testing
- [ ] Compare performance with the classic version
- [ ] Optimize CDS views if needed
- [ ] Test database access patterns
- [ ] Use SQL Monitor to detect optimization candidates
- [ ] Apply code pushdown (CDS, AMDP, ABAP SQL) for performance-critical queries
- [ ] Validate response times

## Deployment

### 20. Deployment
- [ ] Move migrated objects to the ABAP for Cloud Development software component
- [ ] Keep remaining classic objects in `HOME` or the existing classic component
- [ ] Update transport requests
- [ ] Verify priority 1 and 2 findings block transport release
- [ ] Deploy to target system
- [ ] Configure IAM apps and business catalogs (or PFCG roles on SAP Cloud ERP Private)
- [ ] Assign business roles to users
- [ ] Configure `S_ABPLNGVS` authorization and the `SAP_BC_ABAP_DEVELOPER_5` role for ABAP Cloud developers

### 21. Documentation
- [ ] Document all changes made
- [ ] Record the clean core level per object/package (before and after)
- [ ] Document every wrapper, its wrapped object, and its level
- [ ] Document every ATC exemption with justification and review date
- [ ] Update technical specifications
- [ ] Create a remediation report
- [ ] Update operational procedures

## Post-Migration

### 22. Monitoring
- [ ] Monitor system performance
- [ ] Track error rates
- [ ] Track clean core level distribution as a KPI
- [ ] Re-import the changelog for SAP objects before each upgrade
- [ ] Monitor when SAP releases APIs that allow wrappers to be retired
- [ ] Monitor Cloudification Repository reclassifications (C → B, or C → D)
- [ ] Gather user feedback
- [ ] Plan future enhancements

### 23. Optimization
- [ ] Identify performance bottlenecks
- [ ] Optimize frequently accessed CDS views
- [ ] Refactor complex business logic
- [ ] Implement caching where appropriate
- [ ] Retire wrappers whose APIs have since been released

## Common Finding Types and Solutions

### Level D findings — must fix (ATC priority 1)
| Finding | Solution |
|---------|----------|
| Object is modified | Remove modification; use a released or classic BAdI |
| Enhancement technology not allowed | Delete enhancement implementation; use a BAdI |
| Implicit or explicit enhancement | Delete enhancement implementation; use a BAdI |
| Direct **write** access to SAP tables | Use released or classic APIs |
| Call of form routines in SAP program | Use released or classic APIs |
| Usage of `noAPI` object (e.g., `RFC_READ_TABLE`) | Use released or classic APIs; check successor info |
| Critical ABAP statements (`EXEC SQL`, kernel calls, …) | Use released or classic APIs |
| Implementation of SAP-internal-flagged BAdI | Find an alternative extension point |

### Level C findings — minimize (ATC priority 2)
| Finding | Solution |
|---------|----------|
| Direct **read** access to SAP table/view | Use released CDS view or classic API |
| Usage of SAP internal object (not classified, not released) | Use released or classic APIs; else wrap + exempt |
| Custom field on DB table via classic append | Migrate to released extension include when available |
| Wrapper around an internal object | Acceptable interim; monitor for released successor |

### Level B findings — monitor (ATC priority 3)
| Finding | Solution |
|---------|----------|
| Usage of deprecated API | Adopt the successor |
| Usage of classic API (e.g., `CL_GUI_ALV_GRID`, `BAPI_*`) | No action required; monitor for released successor |

### Database access
| Finding | Level | Solution |
|---------|-------|----------|
| Direct SAP table **write** | D | Use released or classic APIs |
| Direct SAP table **read** | C | Use released CDS view (`I_*`) or classic API |
| Direct custom table access | A | Allowed within the same software component |
| `SELECT *` usage | — | Specify explicit fields (code quality, not level) |

### Function modules
| Finding | Level | Solution |
|---------|-------|----------|
| `noAPI` function module | D | Replace using successor information |
| Internal (unclassified) function module | C | Find released or classic replacement, or wrap |
| Classic API function module (e.g., `BAPI_*`) | B | Acceptable; monitor for a released successor |
| Number range FM (`NUMBER_GET_NEXT`) | C | Use `CL_NUMBERRANGE_RUNTIME` (Level A) |

### UI elements
| Finding | Level | Solution |
|---------|-------|----------|
| Dynpro screens | B | Replace with Fiori Elements app when a major change is needed |
| Selection screens | B | Convert to Fiori filters |
| ALV reports (`CL_GUI_ALV_GRID`) | B | Acceptable classic API; migrate to Fiori List Report when feasible |
| Classic list output (`WRITE`) | B | Replace with Fiori UI |

## Estimation Guidelines

### Effort Estimation per Object Type
| Object Type | Low Complexity | Medium Complexity | High Complexity |
|-------------|----------------|-------------------|-----------------|
| Simple report | 2-4 hours | 4-8 hours | 8-16 hours |
| Function module | 1-2 hours | 2-4 hours | 4-8 hours |
| BAPI integration | 4-8 hours | 8-16 hours | 16-32 hours |
| Dynpro transaction | 8-16 hours | 16-32 hours | 32-64 hours |
| Complex report | 4-8 hours | 8-16 hours | 16-32 hours |

### Finding Complexity Indicators
- **Low**: Direct replacement available, no side effects
- **Medium**: Requires wrapper or minor refactoring
- **High**: Major architectural change, multiple dependencies

### Effort by target level transition
| Transition | Typical effort | Notes |
|------------|---------------|-------|
| D → B | Low to medium | Usually a BAdI or classic API swap |
| D → A | High | Requires released API or RAP reimplementation |
| C → B | Low | Swap internal object for a nominated classic API |
| C → A | Medium | Requires a released API or CDS view to exist |
| B → A | Medium to high | Often requires UI modernization to Fiori/RAP |
| C → C (wrapped) | Low | Interim mitigation: wrapper + single exemption |

## Rollback Plan

### Pre-Migration Backup
- [ ] Create full system backup
- [ ] Export all custom code to Git
- [ ] Document current state
- [ ] Prepare rollback procedures

### Rollback Triggers
- Critical business functionality broken
- Performance degradation > 50%
- Security vulnerabilities introduced
- Data corruption issues

## Success Criteria

- [ ] **Zero Level D findings** (ATC priority 1) — mandatory
- [ ] Level C findings minimized, each remaining one wrapped, exempted and justified
- [ ] Level B findings reviewed; deprecated APIs replaced by successors
- [ ] New development happens exclusively in the ABAP Cloud software component (Level A)
- [ ] Global ATC check variant active in development and transport release
- [ ] Priority 1 and 2 findings block transport release
- [ ] Changelog for SAP objects imported and reviewed
- [ ] All functional tests passing
- [ ] Performance within acceptable range
- [ ] User acceptance achieved
- [ ] Documentation complete (levels, wrappers, exemptions)
- [ ] Support team trained

## Clean Core KPIs

Track these to measure progress:

| KPI | Target |
|-----|--------|
| Number of Level D objects | 0 |
| Number of Level C objects | Decreasing trend |
| Share of new objects created at Level A | 100% |
| Number of active ATC exemptions | Decreasing trend |
| Number of modifications | 0 |
| Number of implicit/explicit enhancements | 0 |
| Number of direct SAP table writes | 0 |
| Unused custom code retired | Increasing (target ~60% of legacy) |
| Wrappers retired after API release | Increasing trend |

## References

- Clean Core Extensibility Whitepaper — clean core level concept and KPIs
- Extend SAP S/4HANA in the cloud and on premise with ABAP based extensions (Version 2.3, August 2025)
- Mapping your journey to SAP S/4HANA Cloud Private Edition — conversion-project custom code guidance
- Cloudification Repository: https://github.com/SAP/abap-atc-cr-cv-s4hc
- Cloudification Repository Viewer: https://sap.github.io/abap-atc-cr-cv-s4hc/
- SAP Note 3565942 — clean core ATC checks
- SAP Note 3578329 — classic technology classification