# SQL Server Connection Information

## Server Name for SSMS Login

**Server Name:** `SUMANTH\SQLEXPRESS`

### How to Connect in SSMS:

1. Open **SQL Server Management Studio (SSMS)**
2. In the "Connect to Server" dialog:
   - **Server type:** Database Engine
   - **Server name:** `SUMANTH\SQLEXPRESS`
   - **Authentication:** Windows Authentication
   - Click **Connect**

### Database Information:

- **Database Name:** `BankStatementDB` (created automatically on first ETL run)
- **Table Name:** `BankTransactions`
- **Authentication:** Windows Authentication (uses your current Windows user)

### After Connecting, Run This Query:

```sql
USE BankStatementDB;
SELECT * FROM BankTransactions;
```

---

## Code Review Summary

### ✅ Configuration (config.py)
- **Status:** Fixed and verified
- **Changes Made:**
  - Switched from `pytds` to `pyodbc` for better Windows Auth support
  - Added automatic ODBC driver detection
  - Fixed connection string to properly URL-encode named instances (backslash → %5C)
  - Configured for Windows Authentication with `Trusted_Connection=yes`

### ✅ Flask Application (app.py)
- **Status:** Good
- **Features:**
  - File upload handling
  - ETL pipeline orchestration
  - Error handling and user feedback
  - File cleanup after processing

### ✅ ETL Modules

#### Extract (etl/extract.py)
- **Status:** Good
- **Supports:** PDF, CSV, Excel files
- **Features:** Multiple encoding support, flexible column mapping

#### Transform (etl/transform.py)
- **Status:** Good
- **Features:**
  - Date parsing with multiple formats
  - Merchant name extraction
  - Credit/Debit conversion
  - Data cleaning and validation

#### Load (etl/load.py)
- **Status:** Good
- **Features:**
  - Automatic database creation
  - Automatic table creation
  - Bulk data insertion
  - Error handling

### ✅ Connection String Format

The connection string is now properly formatted for SQLAlchemy 2.0 with pyodbc:

```
mssql+pyodbc://@SUMANTH%5CSQLEXPRESS/BankStatementDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes
```

Key points:
- Named instance backslash is URL-encoded as `%5C`
- Uses Windows Authentication (`Trusted_Connection=yes`)
- Automatically detects available ODBC driver

### ⚠️ Potential Issues to Watch:

1. **ODBC Driver:** Ensure you have an ODBC driver installed (ODBC Driver 17/18 for SQL Server)
2. **SQL Server Service:** Make sure SQL Server service is running
3. **Firewall:** Check Windows Firewall if connection fails
4. **Permissions:** Ensure your Windows user has permissions to create databases

---

## Quick Test

1. Start Flask app: `python app.py`
2. Open browser: `http://localhost:5000`
3. Upload `sample_bank_statement.csv`
4. Click "Process ETL"
5. Check SSMS: `SELECT * FROM BankTransactions;`

