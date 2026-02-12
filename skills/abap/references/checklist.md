# Clean ABAP Checklist

Use this checklist for systematic ABAP code review.

## Names Checklist

- [ ] All variables have descriptive, meaningful names
- [ ] No Hungarian notation (iv_, ev_, lv_, lt_, ls_, gt_)
- [ ] Consistent use of snake_case
- [ ] No abbreviations unless commonly understood
- [ ] Class names are nouns (e.g., account, reader, converter)
- [ ] Method names are verbs (e.g., read, calculate, validate)
- [ ] Boolean methods start with is_, has_, can_
- [ ] No noise words (data, info, object) unless meaningful
- [ ] Same abbreviations used consistently throughout
- [ ] No obscuring of built-in functions (lines, strlen, condense)

## Language Checklist

- [ ] Uses modern syntax (NEW instead of CREATE OBJECT)
- [ ] Uses functional style (VALUE, COND, SWITCH, FILTER)
- [ ] No obsolete constructs (MOVE, TRANSLATE, ADD)
- [ ] SELECT uses @ for host variables
- [ ] Inline declarations where appropriate
- [ ] Table expressions instead of READ TABLE
- [ ] Object-oriented (classes) instead of procedural (function modules)

## Constants Checklist

- [ ] No magic numbers or strings in code
- [ ] All constants have descriptive names
- [ ] Related constants are grouped (BEGIN OF/END OF)
- [ ] ENUM used for enumerations (if ABAP version supports)
- [ ] No constants named by value (c_01, c_x)

## Variables Checklist

- [ ] Inline declarations used (DATA(name) = ...)
- [ ] Variables not used outside declaration block
- [ ] No chained DATA declarations
- [ ] Field symbols only where necessary
- [ ] Appropriate loop targets (field-symbol vs reference vs value)

## Tables Checklist

- [ ] Appropriate table type (STANDARD, SORTED, HASHED)
- [ ] No DEFAULT KEY usage
- [ ] Explicit key or EMPTY KEY specified
- [ ] INSERT INTO TABLE instead of APPEND TO (except arrays)
- [ ] LINE_EXISTS instead of READ TABLE ... TRANSPORTING NO FIELDS
- [ ] READ TABLE instead of LOOP AT ... EXIT
- [ ] WHERE clause in LOOP AT instead of nested IF
- [ ] No double table reads (existence check then read)

## Strings Checklist

- [ ] Backticks (`) used for string literals
- [ ] String templates (|text|) used for assembly
- [ ] No concatenation with && for simple cases

## Booleans Checklist

- [ ] ABAP_BOOL used as type
- [ ] ABAP_TRUE and ABAP_FALSE for values
- [ ] XSDBOOL for assignments
- [ ] No CHAR1 or 'X' and space
- [ ] No comparison with INITIAL
- [ ] Predicative method calls where appropriate
- [ ] Consider if enumeration better than boolean

## Conditions Checklist

- [ ] Conditions are positive where possible
- [ ] IS NOT instead of NOT IS
- [ ] Predicative calls for boolean methods
- [ ] Complex conditions decomposed
- [ ] Very complex conditions extracted to methods

## Ifs Checklist

- [ ] No empty IF branches
- [ ] CASE used instead of multiple ELSE IF
- [ ] Nesting depth <= 3 levels
- [ ] Complex IFs extracted to methods

## Regular Expressions Checklist

- [ ] Simple methods preferred to regex where possible
- [ ] Built-in checks used instead of reinventing
- [ ] Complex regex assembled from parts with documentation

## Classes - Object Orientation Checklist

- [ ] Instance classes preferred to static classes
- [ ] Composition preferred to inheritance
- [ ] No mixing stateful and stateless in same class
- [ ] Clear single responsibility

## Classes - Scope Checklist

- [ ] Global classes by default
- [ ] Local classes only where appropriate
- [ ] FINAL if not designed for inheritance
- [ ] Members PRIVATE by default
- [ ] PROTECTED only if needed for inheritance
- [ ] READ-ONLY used appropriately (public immutables)

## Constructors Checklist

- [ ] NEW used instead of CREATE OBJECT
- [ ] CONSTRUCTOR public if class is CREATE PRIVATE
- [ ] Multiple static creation methods instead of OPTIONAL params
- [ ] Descriptive names for creation methods
- [ ] Singleton only where it makes sense

## Methods - Calls Checklist

- [ ] Static methods called via class (not instance)
- [ ] Types accessed via class/interface (not instance)
- [ ] Functional call style used
- [ ] No RECEIVING keyword
- [ ] No EXPORTING keyword (unless needed)
- [ ] Parameter name omitted for single parameter
- [ ] No unnecessary me-> references

## Methods - Object Orientation Checklist

- [ ] Instance methods preferred to static
- [ ] Public instance methods implement interfaces
- [ ] Interfaces used for dependency inversion

## Methods - Parameters Checklist

- [ ] <= 3 IMPORTING parameters
- [ ] No OPTIONAL parameters (split methods instead)
- [ ] No PREFERRED PARAMETER
- [ ] Exactly one output (RETURNING, EXPORTING, or CHANGING)
- [ ] RETURNING preferred to EXPORTING
- [ ] Not mixing RETURNING with EXPORTING/CHANGING
- [ ] CHANGING used sparingly
- [ ] No boolean input parameters (split method instead)

## Methods - Body Checklist

- [ ] Method does one thing
- [ ] Method length <= 20 lines (ideally 3-5)
- [ ] Focus on happy path OR error handling (not both)
- [ ] One level of abstraction
- [ ] Fail fast pattern used
- [ ] CHECK only at start of method
- [ ] RETURN used for guards

## Error Handling Checklist

- [ ] Exceptions used instead of return codes
- [ ] Class-based exceptions (not message classes)
- [ ] CX_STATIC_CHECK for manageable errors
- [ ] CX_NO_CHECK for unrecoverable errors
- [ ] RAISE EXCEPTION NEW instead of RAISE EXCEPTION TYPE
- [ ] Foreign exceptions wrapped
- [ ] No catching CX_ROOT (too generic)
- [ ] No silent catches

## Comments Checklist

- [ ] Code is self-explanatory (minimal comments needed)
- [ ] Comments explain WHY, not WHAT
- [ ] No commented-out code
- [ ] " used instead of *
- [ ] TODO/FIXME includes user ID
- [ ] No method signature comments
- [ ] No duplicated message texts
- [ ] ABAP Doc only for public APIs
- [ ] Pragmas used instead of pseudo comments

## Formatting Checklist

- [ ] Consistent formatting throughout
- [ ] ABAP Formatter applied
- [ ] One statement per line
- [ ] Line length <= 120 characters
- [ ] Single blank lines (not multiple)
- [ ] Brackets closed at line end
- [ ] Single parameter calls on one line
- [ ] Proper indentation
- [ ] No chained assignments
- [ ] No alignment of different objects

## Testing Checklist

- [ ] Code is testable (dependency injection)
- [ ] Public methods have tests
- [ ] Test class names describe purpose
- [ ] Test method names describe scenario
- [ ] Given-When-Then structure used
- [ ] One When per test method
- [ ] Few, focused assertions
- [ ] Right assert type used
- [ ] Content assertions, not quantity
- [ ] No unnecessary test doubles
- [ ] Tests don't access private members

## Priority Assessment

### Critical Issues (Must Fix)
- Magic numbers without constants
- Deep nesting (>3 levels)
- Methods with >5 parameters
- Multiple output parameters
- Empty IF branches
- Static classes without good reason
- Return codes instead of exceptions
- DEFAULT KEY usage
- Silent exception catching
- Commented-out code in production

### Major Issues (Should Fix)
- Hungarian notation
- Non-descriptive names
- Long methods (>20 lines)
- Up-front declarations where inline is clearer
- APPEND TO instead of INSERT INTO TABLE
- Old-style READ TABLE
- EXPORTING instead of RETURNING
- Methods doing multiple things
- No interfaces for public methods
- Non-FINAL classes not designed for inheritance

### Minor Issues (Nice to Have)
- Single quotes instead of backticks for strings
- Unnecessary me-> references
- Concatenation instead of string templates
- RECEIVING keyword usage
- Multiple blank lines
- Minor formatting inconsistencies
- Could use more functional constructs
