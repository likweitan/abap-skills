---
name: abap
description: Check and improve ABAP code quality using abaplint and Clean ABAP principles. Use this skill when users ask to check, lint, validate, review, or analyze ABAP code for syntax errors, clean code compliance, code quality, best practices, or adherence to Clean ABAP guidelines. Also use when users ask to set up abaplint, configure abaplint.json, or run abaplint on their ABAP project. Triggers include requests like "check this ABAP code", "lint my ABAP", "run abaplint", "configure abaplint", "is this clean ABAP", "review my ABAP", or "analyze ABAP code quality".
---

# ABAP

Check and improve ABAP code quality using two complementary approaches:

- **abaplint**: Automated static analysis via CLI, checking syntax, types, and configurable rules
- **Clean ABAP**: Manual review against Clean ABAP style guide principles

## Workflow

1. **Determine check type** based on user request:
   - If the user asks to lint, run abaplint, or check syntax: use **abaplint**
   - If the user asks for clean code review, best practices, or code quality: use **Clean ABAP review**
   - If unclear or the user asks for a full check: use **both**

2. **For abaplint checks**:
   - Verify `abaplint` is installed (`npx @abaplint/cli --version` or `abaplint --version`)
   - If not installed, install with: `npm install @abaplint/cli -g`
   - Check if `abaplint.json` exists in the project root
   - If no config exists, help the user create one (see starter configs in `references/abaplint.md`)
   - Run `abaplint` in the project root directory
   - Parse and present findings to the user

3. **For Clean ABAP reviews**:
   - Read the ABAP code provided by the user
   - Check against Clean ABAP categories: Names, Language, Constants, Variables, Tables, Strings, Booleans, Conditions, Ifs, Classes, Methods, Error Handling, Comments, Formatting, Testing
   - Identify violations with specific line references
   - Provide actionable recommendations with code examples
   - Prioritize issues by impact (critical, major, minor)

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

## abaplint Findings
[abaplint output, grouped by severity]

## Clean ABAP Review

### Summary
- Total Issues: [count]
- Critical: [count] | Major: [count] | Minor: [count]

### Critical Issues
#### [Category] - [Issue Title]
**Location:** Line [X] / Method [name]
**Problem:** [description]
**Recommendation:** [how to fix]

### Major Issues
[Same format]

### Minor Issues
[Same format]

### Positive Observations
- [Things done well]
```

## References

- **abaplint config & setup**: Read `references/abaplint.md` for installation, configuration options, and starter configs
- **Complete Clean ABAP guide**: Read `references/CleanABAP.md` for full style guide with rationale and examples
- **Quick patterns**: Read `references/quick-reference.md` for condensed good/bad code examples
- **Review checklist**: Read `references/checklist.md` for systematic review checklist
