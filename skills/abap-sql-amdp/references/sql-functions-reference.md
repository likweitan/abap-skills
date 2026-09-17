# ABAP SQL Functions Reference

Comprehensive reference for ABAP SQL built-in functions and expressions.

## String Functions

### Basic String Operations
```abap
-- Concatenation
CONCAT( string1, string2 )          -- Concatenate two strings
CONCAT_WITH_SPACE( s1, s2 )         -- Concatenate with space
STRING_AGG( field, separator )      -- Aggregate values into string

-- Case conversion
UPPER( string )                     -- Convert to uppercase
LOWER( string )                     -- Convert to lowercase

-- Length and substring
LENGTH( string )                    -- String length
SUBSTRING( string, offset, length )  -- Extract substring
LEFT( string, length )              -- Leftmost characters
RIGHT( string, length )             -- Rightmost characters

-- Trimming
LTRIM( string )                     -- Remove leading spaces
RTRIM( string )                     -- Remove trailing spaces
```

### String Search and Replace
```abap
-- Search
INSTR( string, substring )          -- Find substring position
REPLACE( string, old, new )         -- Replace occurrences

-- Pattern matching
LIKE pattern                        -- Wildcard pattern matching
REGEX expression                    -- Regular expression match
```

## Numeric Functions

### Basic Math Operations
```abap
ABS( number )                       -- Absolute value
CEIL( number )                      -- Round up to integer
FLOOR( number )                     -- Round down to integer
ROUND( number, decimals )           -- Round to specified decimals
MOD( dividend, divisor )            -- Modulo (remainder)
DIV( dividend, divisor )            -- Integer division
DIVISION( numerator, denominator )  -- Division with decimal result
```

### Advanced Math
```abap
SQRT( number )                      -- Square root
POWER( base, exponent )             -- Power function
EXP( number )                       -- Exponential function
LOG( number )                       -- Natural logarithm
LOG10( number )                     -- Base-10 logarithm
```

## Date and Time Functions

### Date Operations
```abap
-- Current date
DATS_DAYS_BETWEEN( date1, date2 )   -- Days between two dates
DATS_ADD_DAYS( date, days )         -- Add days to date
DATS_ADD_MONTHS( date, months )     -- Add months to date

-- Date components
EXTRACT( YEAR FROM date )           -- Extract year
EXTRACT( MONTH FROM date )          -- Extract month
EXTRACT( DAY FROM date )            -- Extract day
```

### Time Operations
```abap
-- Current time
TSTMP_CURRENT_UTCTIMESTAMP( )       -- Current UTC timestamp
TSTMP_ADD_SECONDS( timestamp, secs )-- Add seconds to timestamp

-- Time components
EXTRACT( HOUR FROM time )           -- Extract hour
EXTRACT( MINUTE FROM time )         -- Extract minute
EXTRACT( SECOND FROM time )         -- Extract second
```

### Time Zone Conversion
```abap
-- Convert time zones
TSTMP_IS_VALID( timestamp )         -- Check if timestamp is valid
TSTMP_SECONDS_BETWEEN( ts1, ts2 )  -- Seconds between timestamps
```

## Conversion Functions

### Type Casting
```abap
CAST( value AS target_type )         -- Explicit type conversion
-- Target types: ABAP.DEC, ABAP.INT4, ABAP.CHAR, ABAP.STRING, etc.
```

### Data Type Conversions
```abap
-- Numeric conversions
TO_DEC( value, precision, scale )   -- Convert to decimal
TO_INT( value )                     -- Convert to integer
TO_FLOAT( value )                   -- Convert to float

-- String conversions
TO_CHAR( value, format )            -- Convert to string
TO_NCHAR( value )                  -- Convert to national character
```

### Unit and Currency Conversion
```abap
CURRENCY_CONVERSION( amount, 
                     source_currency, 
                     target_currency, 
                     exchange_rate_date )
UNIT_CONVERSION( quantity, 
                 source_unit, 
                 target_unit )
```

## Aggregate Functions

### Basic Aggregates
```abap
COUNT( * )                          -- Count rows
COUNT( DISTINCT field )             -- Count distinct values
SUM( field )                        -- Sum of values
AVG( field )                        -- Average of values
MIN( field )                        -- Minimum value
MAX( field )                        -- Maximum value
```

### Statistical Functions
```abap
STDDEV( field )                     -- Standard deviation
VARIANCE( field )                  -- Variance
```

## Conditional Functions

### CASE Expressions
```abap
-- Simple CASE
CASE field
  WHEN value1 THEN result1
  WHEN value2 THEN result2
  ELSE default_result
END

-- Searched CASE
CASE WHEN condition1 THEN result1
     WHEN condition2 THEN result2
     ELSE default_result
END
```

### NULL Handling
```abap
COALESCE( field1, field2, ... )    -- First non-null value
NULLIF( field1, field2 )            -- NULL if values are equal
```

### Conditional Expressions
```abap
IF( condition, true_value, false_value )  -- Conditional expression
```

## Window Functions

### Ranking Functions
```abap
ROW_NUMBER( ) OVER ( ... )          -- Sequential row number
RANK( ) OVER ( ... )                -- Rank with ties
DENSE_RANK( ) OVER ( ... )           -- Dense rank (no gaps)
NTILE( buckets ) OVER ( ... )       -- Divide into buckets
```

### Aggregate Window Functions
```abap
SUM( field ) OVER ( ... )           -- Running total
AVG( field ) OVER ( ... )           -- Moving average
COUNT( * ) OVER ( ... )             -- Running count
MIN( field ) OVER ( ... )           -- Running minimum
MAX( field ) OVER ( ... )           -- Running maximum
```

### Offset Functions
```abap
LAG( field, offset, default ) OVER ( ... )   -- Value from previous row
LEAD( field, offset, default ) OVER ( ... )  -- Value from next row
FIRST_VALUE( field ) OVER ( ... )            -- First value in partition
LAST_VALUE( field ) OVER ( ... )             -- Last value in partition
```

### Window Frame Clauses
```abap
-- Frame specification
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
```

## Set Operations

### Union Operations
```abap
UNION          -- Combine result sets (remove duplicates)
UNION ALL      -- Combine result sets (keep duplicates)
INTERSECT      -- Intersection of result sets
EXCEPT         -- Difference of result sets
```

## Special Functions

### UUID Generation
```abap
-- In AMDP or via released class
CL_SYSTEM_UUID=>CREATE_UUID_X16_STATIC( )
CL_SYSTEM_UUID=>CREATE_UUID_C36_STATIC( )
```

### System Fields
```abap
-- Session variables
$session.user           -- Current user
$session.client         -- Current client
$session.system_date    -- Current system date
$session.system_time    -- Current system time
$session.system_language -- Current logon language
```

### Technical Fields
```abap
-- Special expressions
@abap_catalog.sqlViewType                 -- View type annotation
@abap_catalog.view.entityEnhancementType  -- Enhancement type
```

## Performance Considerations

### Index Usage
- Use functions on indexed columns can prevent index usage
- Consider computed columns or function-based indexes
- Use `WHERE` clause with simple column comparisons when possible

### String Operations
- `LIKE` with leading wildcards (`%value`) prevents index usage
- Use `INSTR` or full-text search for better performance
- Consider `SUBSTRING` vs `LEFT`/`RIGHT` for readability

### Aggregations
- Use `COUNT(*)` instead of `COUNT(column)` when counting rows
- Use `DISTINCT` sparingly - it's expensive
- Consider materialized views for complex aggregations

### Window Functions
- Window functions can be resource-intensive
- Limit partition size when possible
- Consider alternative approaches for large datasets

## ABAP Cloud Restrictions

### Not Available in ABAP Cloud
- Native SQL (`EXEC SQL`)
- Database-specific functions
- Some legacy string functions
- Direct table access (use CDS views instead)

### Cloud-Compatible Alternatives
- Use ABAP SQL instead of native SQL
- Use released CDS views instead of direct table access
- Use `CL_ABAP_*` classes instead of legacy functions
- Use AMDP for complex database operations

## Common Patterns

### String Manipulation
```abap
-- Build formatted string
CONCAT( first_name, 
        CONCAT( ' ', 
                CONCAT( last_name, 
                        CONCAT( ' (', 
                                CONCAT( department, ')' ) ) ) ) )
```

### Date Calculations
```abap
-- Age calculation
DATS_DAYS_BETWEEN( birth_date, 
                   DATS_ADD_DAYS( $session.system_date, 0 ) ) / 365
```

### Conditional Aggregation
```abap
-- Pivot-like aggregation
SUM( CASE WHEN status = 'A' THEN amount ELSE 0 END ) AS active_amount,
SUM( CASE WHEN status = 'I' THEN amount ELSE 0 END ) AS inactive_amount
```

### Running Totals
```abap
-- Cumulative sum
SUM( amount ) OVER ( 
  PARTITION BY customer_id 
  ORDER BY order_date 
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW 
) AS running_total
```

## Debugging Tips

### Function Testing
- Test functions in small datasets first
- Verify data types match expected formats
- Check for NULL handling in functions
- Use `EXPLAIN` plans for performance analysis

### Common Issues
- Date format mismatches
- NULL value handling
- Type conversion errors
- Overflow in numeric calculations
- Character set encoding issues