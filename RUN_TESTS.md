# Commands to Run Test Cases

## Basic Commands

### Run All Tests
```bash
python -m pytest tests/test_etl.py -v
```

### Run All Tests with Detailed Output
```bash
python -m pytest tests/test_etl.py -v -s
```

### Run All Tests and Show Summary
```bash
python -m pytest tests/test_etl.py -v --tb=short
```

## Run Specific Test Classes

### Run Only Extract Tests
```bash
python -m pytest tests/test_etl.py::TestExtract -v
```

### Run Only Transform Tests
```bash
python -m pytest tests/test_etl.py::TestTransform -v
```

### Run Only Integration Tests
```bash
python -m pytest tests/test_etl.py::TestIntegration -v
```

### Run Only Data Quality Tests
```bash
python -m pytest tests/test_etl.py::TestDataQuality -v
```

## Run Specific Individual Tests

### Run Single Test
```bash
python -m pytest tests/test_etl.py::TestExtract::test_extract_merchant_name -v
```

### Run Multiple Specific Tests
```bash
python -m pytest tests/test_etl.py::TestExtract::test_extract_csv tests/test_etl.py::TestExtract::test_extract_excel -v
```

## Advanced Options

### Run Tests and Generate Coverage Report
```bash
python -m pytest tests/test_etl.py --cov=etl --cov-report=html -v
```

### Run Tests and Stop on First Failure
```bash
python -m pytest tests/test_etl.py -v -x
```

### Run Tests and Show Print Statements
```bash
python -m pytest tests/test_etl.py -v -s
```

### Run Tests and Skip PDF Tests (if PDF not available)
```bash
python -m pytest tests/test_etl.py -v -m "not skipif"
```

### Run Tests with Maximum Verbosity
```bash
python -m pytest tests/test_etl.py -vv
```

## Quick Test Commands

### Quick Test (Short Output)
```bash
pytest tests/test_etl.py
```

### Quick Test with Verbose Output
```bash
pytest tests/test_etl.py -v
```

## PowerShell Commands (Windows)

### Run All Tests in PowerShell
```powershell
python -m pytest tests/test_etl.py -v
```

### Run Tests from Project Directory
```powershell
Set-Location "C:\Users\suman\OneDrive\Desktop\Project Complete ETL_QA"
python -m pytest tests/test_etl.py -v
```

## Expected Output

When tests run successfully, you should see:
- ✅ 17 tests passing
- ⚠️ 3 tests may fail (PDF extraction tests if PDF format doesn't match)

## Troubleshooting

### If tests can't find modules:
```bash
# Make sure you're in the project root directory
cd "C:\Users\suman\OneDrive\Desktop\Project Complete ETL_QA"
python -m pytest tests/test_etl.py -v
```

### If pytest is not installed:
```bash
pip install pytest
```

### Run tests with Python directly:
```bash
python -m pytest tests/test_etl.py -v
```

