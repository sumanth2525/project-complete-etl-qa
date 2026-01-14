# How to Fix the Amount Column Overflow Error

## Quick Fix (Automatic - Recommended)

The code has been updated to automatically fix this issue. Just run the ETL process again:

```bash
python app.py
```

The application will:
1. ✅ Automatically detect the old column size
2. ✅ Automatically alter it to `DECIMAL(18,2)`
3. ✅ Filter out unrealistic amounts
4. ✅ Process your transactions successfully

**That's it!** The fix is automatic.

---

## Manual Fix (If Automatic Doesn't Work)

If you prefer to fix it manually or the automatic fix doesn't work, follow these steps:

### Option 1: Fix via SQL Server Management Studio (SSMS)

1. **Open SQL Server Management Studio (SSMS)**
2. **Connect to your server:**
   - Server name: `SUMANTH\SQLEXPRESS`
   - Authentication: Windows Authentication
3. **Run this SQL script:**

```sql
USE BankStatementDB;
GO

-- Check current column size
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    NUMERIC_PRECISION,
    NUMERIC_SCALE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'BankTransactions' 
AND COLUMN_NAME = 'Amount';
GO

-- Fix the Amount column
ALTER TABLE BankTransactions
ALTER COLUMN Amount DECIMAL(18,2);
GO

-- Verify the fix
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    NUMERIC_PRECISION,
    NUMERIC_SCALE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'BankTransactions' 
AND COLUMN_NAME = 'Amount';
GO

PRINT 'Amount column fixed successfully!';
GO
```

4. **Verify:** You should see `NUMERIC_PRECISION = 18` after running the script

### Option 2: Run the SQL Script File

1. **Open SSMS** and connect to `SUMANTH\SQLEXPRESS`
2. **Open the file:** `fix_amount_column.sql`
3. **Execute the script** (F5 or Execute button)
4. **Done!**

### Option 3: Use Python Script

Run this Python command to fix it programmatically:

```bash
python -c "
from sqlalchemy import create_engine, text
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    try:
        conn.execute(text('ALTER TABLE BankTransactions ALTER COLUMN Amount DECIMAL(18,2)'))
        conn.commit()
        print('Amount column fixed successfully!')
    except Exception as e:
        print(f'Error: {e}')
engine.dispose()
"
```

---

## Verify the Fix

After applying the fix, verify it worked:

### In SSMS:
```sql
USE BankStatementDB;
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    NUMERIC_PRECISION,
    NUMERIC_SCALE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'BankTransactions' 
AND COLUMN_NAME = 'Amount';
```

**Expected Result:**
- `NUMERIC_PRECISION` should be **18** (not 10)
- `NUMERIC_SCALE` should be **2**

### Test the Application:
```bash
python app.py
```

Then try uploading a file again. The error should be gone!

---

## What Was Fixed?

1. **Column Size:** `DECIMAL(10,2)` → `DECIMAL(18,2)`
   - Old: Max value = 99,999,999.99
   - New: Max value = 999,999,999,999,999,999.99

2. **Data Validation:** Added filtering for unrealistic amounts
   - Filters out values > $10 million (likely data extraction errors)
   - Logs warnings when filtering occurs

3. **Auto-Migration:** Code automatically fixes existing tables

---

## Troubleshooting

### If you get "Cannot alter column" error:
The table might have data that conflicts. Try:

```sql
-- Option A: Clear the table first (WARNING: Deletes all data!)
TRUNCATE TABLE BankTransactions;
ALTER TABLE BankTransactions ALTER COLUMN Amount DECIMAL(18,2);

-- Option B: Drop and recreate (WARNING: Deletes all data!)
DROP TABLE BankTransactions;
-- Then run the ETL process again - it will create the table with correct schema
```

### If the automatic fix doesn't work:
1. Check the logs for error messages
2. Try the manual fix (Option 1 above)
3. Verify the column was updated using the verification query

---

## Summary

**Easiest Method:** Just run `python app.py` again - the fix is automatic!

**Manual Method:** Run the SQL script in SSMS to alter the column.

**Status:** ✅ Issue is fixed in the code. Just need to update the existing table.

