---
name: abap
description: Comprehensive ABAP code quality checking using abaplint (automated static analysis) and Clean ABAP principles (manual code review). Use when users ask to check, lint, validate, review, or analyze ABAP code for syntax errors, clean code compliance, code quality, best practices, or adherence to Clean ABAP guidelines. Also use for abaplint setup, configuration, and execution. Triggers include "check this ABAP code", "lint my ABAP", "run abaplint", "configure abaplint", "is this clean ABAP", "review my ABAP", "analyze ABAP code quality", "code quality check", or "ABAP best practices".
---

# ABAP

Check and improve ABAP code quality using two complementary approaches:

- **abaplint**: Automated static analysis via CLI, checking syntax, types, and configurable rules
- **Clean ABAP**: Manual review against Clean ABAP style guide principles

Keep code quality and SAP clean core compliance separate. Clean ABAP and abaplint assess code quality; they do not establish which SAP APIs or extension points an application uses. For clean core levels, released API status, or ABAP Cloud compliance, use the `abap-cloud` skill and relevant ATC checks.

## Workflow

1. **Establish the code context** before assessing syntax or API compatibility:
   - Identify the target ABAP platform/release and language version (for example, Standard ABAP or ABAP for Cloud Development) when provided.
   - For abaplint, inspect the existing `abaplint.json` and its configured syntax version; do not silently change it.
   - If the context is missing and a finding depends on it, ask a focused question or label the finding as context-dependent. Do not call syntax or an API invalid based on an unstated target.
   - A style-only review can proceed without release details; note assumptions only where they affect the finding.

2. **Determine check type** based on user request:
   - If the user asks to lint, run abaplint, or check syntax: use **abaplint**
   - If the user asks for clean code review, best practices, or code quality: use **Clean ABAP review**
   - If unclear or the user asks for a full check: use **both**

3. **For abaplint checks**:
   - Look for a project-local `node_modules/.bin/abaplint` first, then an already available `abaplint` command.
   - If neither is installed, explain that and ask before installing or changing project files. Prefer a project-local dev dependency (`npm install --save-dev @abaplint/cli`) when the user approves; install globally only when specifically requested.
   - Check if `abaplint.json` exists in the project root
   - If no config exists, explain the tradeoffs and offer a starter config (see `references/abaplint.md`); do not create or alter config without user approval.
   - Run the project-local binary or already-installed command from the project root. Do not use a command that silently downloads or installs a tool.
   - Report the configured syntax version and preserve abaplint's own severity and rule identifiers in results.

4. **For Clean ABAP reviews**:
   - Read the ABAP code provided by the user
   - Use the Clean ABAP categories below as review lenses, not unconditional rules. Consider the target release, local conventions, readability, and tradeoffs; report a recommendation only when it materially improves this code.
   - Tie each finding to a line, statement, or method and explain the observable impact. If line numbers are unavailable, quote a short identifying snippet.
   - Give a minimal, actionable fix; do not rewrite unrelated code.
   - Separate confirmed defects from context-dependent risks and style preferences.

## Finding severity

Use severity to communicate impact, not how strongly a style rule is worded:

- **Critical** — clear risk of incorrect results, data loss, security exposure, or production failure that needs immediate attention.
- **Major** — a confirmed defect or substantial performance, reliability, or maintainability problem that should be addressed.
- **Minor** — a localized, low-impact improvement or style inconsistency.

Do not label a preference (such as method length, naming style, or string-literal style) critical. If impact or release compatibility cannot be established, say what context is missing instead of overstating severity. Keep abaplint's reported severity separate from this manual review scale; do not silently translate one into the other.

## abaplint Quick Start

Run in project root:

```bash
abaplint
```

Generate default config (all rules):

```bash
abaplint -d > abaplint.json
```

For detailed abaplint configuration including starter configs for On-Premise, Steampunk/BTP, and HANA compatibility, read `references/abaplint.md`.

## Clean ABAP Check Categories

### Names

- Use descriptive names, snake*case, no Hungarian notation (iv*, lv*, lt*)
- Nouns for classes, verbs for methods, no noise words

### Language

- Prefer OO over procedural, functional over imperative
- Use modern syntax: NEW, inline declarations, table expressions

### Constants

- No magic numbers, use ENUM or grouped constants

### Variables

- Prefer inline declarations, no chained DATA

### Tables

- No DEFAULT KEY, use INSERT INTO TABLE, LINE_EXISTS, WHERE clauses

### Strings

- Backticks for literals, pipes for string templates

### Booleans

- Use ABAP_BOOL, ABAP_TRUE/ABAP_FALSE, XSDBOOL

### Conditions

- Positive conditions, IS NOT over NOT IS, predicative method calls

### Ifs

- No empty IF branches, CASE over ELSE IF, nesting depth <= 3

### Methods

- Instance over static, RETURNING over EXPORTING, <= 3 parameters, <= 20 lines

### Error Handling

- Exceptions over return codes, class-based exceptions, no catching CX_ROOT

### Comments

- Explain why not what, " over \*, no commented-out code

### Formatting

- One statement per line, <= 120 chars, consistent indentation

### Testing

- Given-when-then structure, focused assertions, dependency injection

## Output Format

Structure analysis results as:

```
# ABAP Check Results

## Context
- Platform/release: [provided value or not specified]
- Language version: [provided value or not specified]
- abaplint syntax version: [configured value or not run]

## abaplint Findings
[Preserve each finding's abaplint severity and rule identifier]

## Clean ABAP Review

### Summary
- Total Issues: [count]
- Critical: [count] | Major: [count] | Minor: [count]

### Findings
For each finding, include:
- **Severity and category:** [impact-based severity] / [Clean ABAP category]
- **Location:** [line, statement, or method]
- **Evidence:** [short quote or observed pattern]
- **Impact:** [concrete consequence; state when context-dependent]
- **Recommendation:** [minimal actionable fix]

### Positive Observations
- [Things done well]
```

## References

- **abaplint config & setup**: Read `references/abaplint.md` for installation, configuration options, and starter configs
- **Complete Clean ABAP guide**: Read `references/CleanABAP.md` for full style guide with rationale and examples
- **Quick patterns**: Read `references/quick-reference.md` for condensed good/bad code examples
- **Review checklist**: Read `references/checklist.md` for systematic review checklist

## Related Skills

- **abap-cloud**: Use for clean core levels and ABAP Cloud compliance
- **abap-unit-testing**: Use for writing unit tests that follow Clean ABAP principles
- **abap-sql-amdp**: Use for modernizing ABAP SQL during code quality improvements
