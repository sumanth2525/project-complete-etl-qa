# Bank Statement ETL Project

A complete ETL (Extract, Transform, Load) pipeline built with Python and Flask that processes bank statement files and loads transaction data into SQL Server.

## Features

- 📄 **Multi-format Support**: Process PDF, CSV, and Excel bank statements
- 🔄 **Automated ETL Pipeline**: Extract, transform, and load data with a single click
- 🗄️ **SQL Server Integration**: Direct connection to SQL Server (SSMS) using `pyodbc` with Windows Authentication support
- 🎨 **Modern Web UI**: Clean Bootstrap-based interface for file upload
- ✅ **Data Validation**: Automatic data cleaning and standardization
- 🧪 **Unit Tests**: Comprehensive test suite for all components

## Project Structure

```
bank_etl_ui/
├── app.py                 # Flask application main file
├── config.py              # Configuration and database settings
├── etl/
│   ├── extract.py         # File extraction module
│   ├── transform.py       # Data transformation module
│   └── load.py            # Database loading module
├── templates/
│   └── index.html         # Web UI template
├── tests/
│   └── test_etl.py        # Unit tests
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Prerequisites

- Python 3.8 or higher
- SQL Server (SSMS) with instance `SUMANTH\SQLEXPRESS`
- pip package manager

## Installation

1. **Clone or download this project**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database connection** (if needed):
   - Edit `config.py` to adjust SQL Server credentials
   - Default connection: `SUMANTH\SQLEXPRESS` with user `sumanth`
   - Add password if required in `config.py`

## Usage

### Starting the Application

1. **Run the Flask application**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Upload a bank statement file**:
   - Supported formats: PDF, CSV, Excel (.xlsx, .xls)
   - Click "Choose File" and select your statement
   - Click "Process ETL" button

4. **View results in SQL Server**:
   - Open SQL Server Management Studio (SSMS)
   - Connect to `SUMANTH\SQLEXPRESS`
   - Run query:
     ```sql
     USE BankStatementDB;
     SELECT * FROM BankTransactions;
     ```

## Database Schema

The application automatically creates the following table:

```sql
CREATE TABLE BankTransactions (
    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
    TxnDateTime DATETIME,
    Amount DECIMAL(10,2),
    Description NVARCHAR(255),
    MerchantName NVARCHAR(100),
    IsCredit BIT
);
```

## ETL Pipeline Details

### 1. Extract Phase
- **PDF**: Uses `pdfplumber` to extract tables and text
- **CSV**: Uses `pandas` with multiple encoding support
- **Excel**: Supports both `.xlsx` and `.xls` formats
- Handles missing data and various column name formats

### 2. Transform Phase
- Standardizes date formats to SQL DATETIME
- Extracts merchant names from descriptions
- Converts transaction types to IsCredit (BIT)
- Cleans and normalizes all data fields
- Removes duplicates

### 3. Load Phase
- Automatically creates database if missing
- Creates table with proper schema
- Bulk inserts data using pandas `to_sql()`
- Returns count of inserted records

## Testing

Run the test suite:

```bash
pytest tests/test_etl.py -v
```

Or run specific test classes:

```bash
pytest tests/test_etl.py::TestExtract -v
pytest tests/test_etl.py::TestTransform -v
```

## Configuration

Edit `config.py` to customize:

- SQL Server instance name
- Database name
- User credentials
- Upload folder location
- File size limits
- Allowed file extensions

## Troubleshooting

### Connection Issues
- Verify SQL Server instance name: `SUMANTH\SQLEXPRESS`
- Check SQL Server is running
- Verify Windows Authentication or SQL Authentication credentials
- Check firewall settings

### File Upload Issues
- Ensure file size is under 16MB
- Check file format is supported (PDF, CSV, Excel)
- Verify file is not corrupted

### Data Extraction Issues
- PDF files should have readable text/tables
- CSV files should have headers: Date, Description, Amount, Type
- Excel files should follow similar column structure

## Dependencies

- **Flask 3.0.3**: Web framework
- **pandas 2.2.3**: Data manipulation
- **pdfplumber 0.11.4**: PDF parsing
- **openpyxl 3.1.5**: Excel file handling
- **SQLAlchemy 2.0.36**: Database ORM
- **pyodbc 5.1.0**: SQL Server driver with native Windows Authentication support
- **pytest 8.3.3**: Testing framework

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in the Flask console
3. Verify database connection settings
4. Test with sample CSV/Excel files first

---

**Note**: This application automatically creates the database and table on first run. No manual SQL setup is required beyond having SQL Server running.

