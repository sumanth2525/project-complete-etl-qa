# Test Cases Documentation

## Overview

This test suite includes comprehensive tests for the ETL pipeline, with specific test cases based on Chase bank statement PDF format.

## Test Structure

### 1. TestExtract Class
Tests extraction functionality from various file formats.

#### Key Tests:
- **test_extract_merchant_name**: Tests merchant name extraction from descriptions
- **test_parse_date**: Tests date parsing with various formats (including Chase MM/DD/YYYY)
- **test_extract_csv**: Tests CSV file extraction
- **test_extract_excel**: Tests Excel file extraction
- **test_extract_pdf_chase_format**: Tests PDF extraction logic for Chase format
- **test_extract_chase_pdf_real**: Tests extraction from actual "july chase statement.pdf" file
- **test_full_etl_chase_pdf**: Tests full ETL pipeline with Chase PDF

### 2. TestTransform Class
Tests data transformation and standardization.

#### Key Tests:
- **test_transform_schema**: Verifies output schema matches requirements
- **test_transform_credit_debit**: Tests credit/debit classification
- **test_transform_merchant_extraction**: Tests merchant name extraction
- **test_transform_chase_descriptions**: Tests Chase-specific transaction descriptions
- **test_transform_chase_date_formats**: Tests Chase date format (MM/DD/YYYY) handling
- **test_transform_amount_formats**: Tests various amount formats

### 3. TestIntegration Class
Tests end-to-end integration scenarios.

#### Key Tests:
- **test_full_pipeline_schema**: Tests complete pipeline schema consistency
- **test_chase_statement_simulation**: Simulates a full Chase statement with various transaction types
- **test_chase_pdf_end_to_end**: End-to-end test with actual Chase PDF file

### 4. TestDataQuality Class
Tests data quality and validation rules.

#### Key Tests:
- **test_no_duplicate_transactions**: Ensures duplicates are removed
- **test_amount_always_positive**: Ensures all amounts are positive
- **test_description_length_limit**: Ensures descriptions are ≤255 chars
- **test_merchant_name_length_limit**: Ensures merchant names are ≤100 chars

## Running Tests

### Run All Tests
```bash
pytest tests/test_etl.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_etl.py::TestExtract -v
pytest tests/test_etl.py::TestTransform -v
pytest tests/test_etl.py::TestIntegration -v
pytest tests/test_etl.py::TestDataQuality -v
```

### Run Tests with Chase PDF (requires file)
```bash
pytest tests/test_etl.py::TestExtract::test_extract_chase_pdf_real -v
pytest tests/test_etl.py::TestExtract::test_full_etl_chase_pdf -v
pytest tests/test_etl.py::TestIntegration::test_chase_pdf_end_to_end -v
```

### Run Tests Without PDF (skip PDF tests)
```bash
pytest tests/test_etl.py -v -m "not skipif"
```

## Chase Statement Format

The tests are designed to handle Chase bank statement format which typically includes:

### Date Format
- **Format**: MM/DD/YYYY (e.g., 07/15/2024)
- **Variations**: M/D/YYYY (e.g., 7/5/2024)

### Transaction Types
- **Credits**: Direct deposits, transfers in, refunds
- **Debits**: Purchases, ATM withdrawals, transfers out, checks

### Common Descriptions
- `DIRECT DEPOSIT SALARY`
- `AMAZON MARKETPLACE`
- `CHASE CREDIT CRD AUTOPAY`
- `STARBUCKS STORE #1234`
- `ATM WITHDRAWAL`
- `ONLINE TRANSFER TO SAVINGS`
- `CHECK #5678`

### Amount Format
- Currency symbol: $ (e.g., $1,234.56)
- Negative amounts for debits (in some formats)
- Positive amounts for credits

## Expected Test Results

### With Chase PDF File
- All extraction tests should pass
- End-to-end tests should process transactions
- Data quality tests should validate all records

### Without Chase PDF File
- PDF-specific tests will be skipped
- All other tests should pass
- Mock data tests validate functionality

## Test Coverage

✅ **File Format Support**
- PDF extraction (Chase format)
- CSV extraction
- Excel extraction

✅ **Data Transformation**
- Date parsing (multiple formats)
- Amount normalization
- Credit/Debit classification
- Merchant name extraction

✅ **Data Quality**
- Duplicate removal
- Data type validation
- Length constraints
- Null value handling

✅ **Integration**
- Full pipeline testing
- Real PDF file processing
- Schema validation

## Troubleshooting

### PDF Tests Skipped
If you see "Chase PDF file not found", ensure:
- File `july chase statement.pdf` exists in project root
- File is not corrupted
- File has readable text/tables

### Date Parsing Failures
- Check date format in PDF matches expected formats
- Verify transform.py date parsing logic handles your format

### Amount Parsing Issues
- Ensure amounts are numeric
- Check for currency symbols that need removal
- Verify negative amounts are handled correctly

