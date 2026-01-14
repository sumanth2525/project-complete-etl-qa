# Fix for Amount Column Overflow Error

## Problem

**Error Message:**
```
Arithmetic overflow error converting float to data type numeric.
```

**Root Cause:**
1. The `Amount` column was defined as `DECIMAL(10,2)` which can only store values up to **99,999,999.99**
2. The data contained a value of **9,000,142,693.0** (over 9 billion), which exceeded the column limit
3. This large value is likely a data extraction error (account number or reference number, not an actual transaction amount)

## Solution Applied

### 1. Increased Column Size
- Changed `Amount` column from `DECIMAL(10,2)` to `DECIMAL(18,2)`
- `DECIMAL(18,2)` supports values up to **999,999,999,999,999,999.99** (999 quadrillion)
- This is more than sufficient for any realistic bank transaction

### 2. Automatic Table Migration
- The code now automatically detects if the table has the old column size
- If found, it automatically alters the column to `DECIMAL(18,2)`
- No manual intervention needed for existing tables

### 3. Data Validation
- Added validation to filter out unrealistic amounts
- Transactions outside the range of **$0.01 to $10,000,000** are filtered out
- These are likely data extraction errors (account numbers, reference IDs, etc.)
- A warning is logged when transactions are filtered

## Files Modified

1. **etl/load.py**
   - Updated table creation to use `DECIMAL(18,2)`
   - Added automatic column alteration for existing tables

2. **etl/transform.py**
   - Added amount validation (filters unrealistic values)
   - Added logging for filtered transactions

3. **fix_amount_column.sql**
   - Manual SQL script if you need to fix the table manually

## How to Apply the Fix

### Automatic (Recommended)
The fix is automatic! Just run the ETL process again:
```bash
python app.py
```

The code will:
1. Detect the old column size
2. Automatically alter it to `DECIMAL(18,2)`
3. Filter out unrealistic amounts during transformation

### Manual (If Needed)
If you prefer to fix it manually in SSMS:

1. Open SQL Server Management Studio
2. Connect to `SUMANTH\SQLEXPRESS`
3. Run the script: `fix_amount_column.sql`

Or run this SQL directly:
```sql
USE BankStatementDB;
ALTER TABLE BankTransactions
ALTER COLUMN Amount DECIMAL(18,2);
```

## Testing

After applying the fix, test with:
```bash
# Test the connection
python test_connection.py

# Run the application
python app.py
```

## Expected Behavior

- ✅ Large amounts (up to 999 quadrillion) can now be stored
- ✅ Unrealistic amounts (>$10M) are automatically filtered out
- ✅ Warning messages logged for filtered transactions
- ✅ No more overflow errors

## Notes

- The value **9,000,142,693.0** was likely an account number or reference ID that was incorrectly extracted as an amount
- The validation filter (max $10M) should catch these types of errors in the future
- If you need to support transactions larger than $10M, you can adjust `MAX_REALISTIC_AMOUNT` in `etl/transform.py`

