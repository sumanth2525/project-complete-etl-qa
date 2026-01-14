-- SQL Script to Fix Amount Column Size
-- Run this in SSMS if you need to manually fix the table

USE BankStatementDB;
GO

-- Check current column definition
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    NUMERIC_PRECISION,
    NUMERIC_SCALE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'BankTransactions' 
AND COLUMN_NAME = 'Amount';
GO

-- Alter the Amount column to support larger values
ALTER TABLE BankTransactions
ALTER COLUMN Amount DECIMAL(18,2);
GO

-- Verify the change
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    NUMERIC_PRECISION,
    NUMERIC_SCALE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'BankTransactions' 
AND COLUMN_NAME = 'Amount';
GO

PRINT 'Amount column updated to DECIMAL(18,2) successfully!';
GO

