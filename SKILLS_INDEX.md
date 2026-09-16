# ABAP Skills Index

Comprehensive index of all ABAP development skills available in this repository.

## Code Quality & Testing

### [abap](skills/abap/)
Comprehensive ABAP code quality checking using abaplint (automated static analysis) and Clean ABAP principles (manual code review). Use for linting, code validation, and best practices review.

### [abap-unit-testing](skills/abap-unit-testing/)
Comprehensive ABAP Unit testing guidance including test class setup, assertions, test doubles, mocking frameworks, and test environments for CDS, SQL, and RAP.

## ABAP Cloud & Migration

### [abap-cloud](skills/abap-cloud/)
Guide for ABAP Cloud development including the clean core level concept (Levels A/B/C/D), ABAP Cloud language version restrictions, wrapper patterns, and clean core principles.

### [abap-cloud-migration](skills/abap-cloud-migration/)
Systematic guidance for migrating classic ABAP custom code to ABAP Cloud including custom code adaptation, unreleased API replacements, and ATC Cloud Readiness checks.

### [atc-cloudification](skills/atc-cloudification/)
Configure ATC Cloud Readiness and Clean Core checks using the SAP Cloudification Repository for Released APIs validation.

## Data Modeling & Business Logic

### [cds-view-entities](skills/cds-view-entities/)
Guide for building semantic data models using ABAP CDS view entities including annotations, associations, compositions, access controls, and expressions.

### [abap-sql-amdp](skills/abap-sql-amdp/)
Modern ABAP SQL features and AMDP (ABAP Managed Database Procedures) including window functions, CTEs, aggregates, and database procedures.

### [rap](skills/rap/)
RESTful ABAP Programming Model (RAP) development including behavior definitions, EML statements, managed/unmanaged BOs, draft handling, and business logic.

### [rap-business-events](skills/rap-business-events/)
RAP business events and enterprise eventing including event definitions, raising events, event bindings, SAP Event Mesh integration, and event-driven patterns.

## Authorization & Security

### [authorization-iam](skills/authorization-iam/)
ABAP authorization and IAM (Identity and Access Management) including authorization objects, CDS access control, IAM apps, business catalogs, and role-based access.

## Integration & Extensibility

### [badi-enhancement](skills/badi-enhancement/)
BAdI (Business Add-In) development and the ABAP enhancement framework including new BAdIs, fallback classes, filter-based BAdIs, and enhancement spots.

### [odata](skills/odata/)
OData service development in ABAP including OData V2/V4 services via RAP service bindings, SEGW-based services, and OData annotations.

### [abapgit](skills/abapgit/)
abapGit workflows for managing ABAP development objects in Git repositories including setup, serialization, branching strategies, and CI/CD integration.

## Platform & Infrastructure

### [btp-abap-environment](skills/btp-abap-environment/)
SAP BTP ABAP Environment setup and development including service instance creation, ADT connectivity, communication arrangements, and software components.

### [btp-diagram-generator](skills/btp-diagram-generator/)
Generate SAP BTP solution architecture diagrams as native draw.io files following official SAP BTP Solution Diagram guidelines.

## Utilities & References

### [released-abap-classes](skills/released-abap-classes/)
Quick reference for released ABAP classes available in ABAP for Cloud Development for email, UUID generation, time/date handling, JSON/XML processing, and more.

### [sap-fiori-url-generator](skills/sap-fiori-url-generator/)
Generate SAP Fiori Launchpad URLs from app names using AppList.json for proper FLP navigation with required parameters.

## Skill Categories

### Core Development Skills
- **abap** - Code quality and linting
- **cds-view-entities** - Data modeling
- **abap-sql-amdp** - Database operations
- **rap** - Business object development
- **abap-unit-testing** - Testing

### Cloud Migration Skills
- **abap-cloud** - Cloud concepts and principles
- **abap-cloud-migration** - Migration guidance
- **atc-cloudification** - Cloud readiness checks

### Integration Skills
- **odata** - Service exposure
- **badi-enhancement** - SAP standard extensions
- **abapgit** - Version control
- **rap-business-events** - Event-driven architecture

### Platform Skills
- **btp-abap-environment** - BTP setup
- **btp-diagram-generator** - Architecture diagrams
- **authorization-iam** - Security and access control

### Reference Skills
- **released-abap-classes** - API reference
- **sap-fiori-url-generator** - Fiori URL generation

## Quick Reference Matrix

| Task | Recommended Skill |
|------|------------------|
| Check code quality | `abap` |
| Write unit tests | `abap-unit-testing` |
| Create CDS data model | `cds-view-entities` |
| Build RAP business object | `rap` |
| Migrate to ABAP Cloud | `abap-cloud-migration` |
| Setup BTP ABAP Environment | `btp-abap-environment` |
| Implement authorization | `authorization-iam` |
| Create OData service | `odata` |
| Extend SAP standard | `badi-enhancement` |
| Version control with Git | `abapgit` |
| Find released APIs | `released-abap-classes` |
| Generate BTP diagrams | `btp-diagram-generator` |

## Learning Paths

### Beginner Path
1. Start with `abap` for code quality basics (includes both abaplint and Clean ABAP)
2. Learn `cds-view-entities` for data modeling
3. Practice with `abap-unit-testing` for testing
4. Explore `abap-cloud` for cloud concepts

### Cloud Migration Path
1. Understand `abap-cloud` principles
2. Run `atc-cloudification` checks
3. Follow `abap-cloud-migration` guidance
4. Use `released-abap-classes` for API replacements

### RAP Development Path
1. Master `cds-view-entities` data modeling
2. Learn `rap` behavior definitions
3. Implement with `abap-sql-amdp` for complex logic
4. Add `rap-business-events` for event patterns
5. Expose via `odata` services
6. Secure with `authorization-iam`

### BTP Development Path
1. Setup with `btp-abap-environment`
2. Develop with `rap` and `cds-view-entities`
3. Document with `btp-diagram-generator`
4. Version control with `abapgit`

## Skill Relationships

### Core Dependencies
- `rap` depends on `cds-view-entities` (data modeling)
- `odata` depends on `rap` (service exposure)
- `abap-cloud-migration` depends on `atc-cloudification` (readiness checks)

### Complementary Skills
- `abap` - comprehensive code quality (abaplint + Clean ABAP)
- `abap-cloud` and `abap-cloud-migration` - concepts vs. implementation
- `authorization-iam` and `rap` - security implementation in RAP

### Advanced Combinations
- `rap` + `rap-business-events` + `odata` = complete event-driven RAP application
- `abap-cloud-migration` + `released-abap-classes` + `atc-cloudification` = migration workflow
- `btp-abap-environment` + `rap` + `authorization-iam` = BTP RAP application

## Maintenance Notes

### Skill Structure
Each skill follows a consistent structure:
- `SKILL.md` - Main skill documentation with frontmatter
- `references/` - Detailed reference materials (optional)
- `scripts/` - Automation scripts (optional)
- `examples/` - Code examples (optional)

### Skill Frontmatter
Each skill includes standardized frontmatter:
- `name` - Skill identifier
- `description` - When to use the skill
- Triggers - Keywords that activate the skill

### Best Practices
- Skills should be focused on specific topics
- Cross-reference related skills
- Include practical code examples
- Provide SAP documentation links
- Maintain consistent formatting

## Contributing

When adding new skills:
1. Follow the established directory structure
2. Include proper frontmatter with triggers
3. Add cross-references to related skills
4. Create reference files for complex topics
5. Update this index

When updating existing skills:
1. Maintain consistency with other skills
2. Update cross-references if relationships change
3. Verify external links are current
4. Test skill triggers work correctly
5. Update this index if skill scope changes

## Additional Resources

### SAP Documentation
- [SAP Help Portal](https://help.sap.com/)
- [SAP Community](https://community.sap.com/)
- [SAP Developers](https://developers.sap.com/)

### ABAP Resources
- [ABAP Cheat Sheets](https://github.com/SAP-samples/abap-cheat-sheets)
- [Clean ABAP Guide](https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md)
- [ABAP Cloud API Release Info](https://help.sap.com/docs/abap-cloud/abap-rap/released-abap-objects)

### Community Resources
- [abapGit](https://docs.abapgit.org/)
- [abaplint](https://abaplint.org/)
- [SAP BTP Documentation](https://help.sap.com/docs/btp/)

---

**Last Updated**: 2024-09-16  
**Total Skills**: 17  
**Categories**: 8