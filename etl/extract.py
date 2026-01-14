"""
Extract module for ETL pipeline
Handles extraction from PDF, CSV, and Excel files
"""
import pandas as pd
import pdfplumber
import os
from typing import List, Dict, Optional
import re


def extract_from_pdf(file_path: str) -> pd.DataFrame:
    """
    Extract transaction data from PDF bank statement
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        DataFrame with columns: Date, Description, Amount, Type
    """
    transactions = []
    
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                
                # Try to extract table data
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        # Process table rows
                        for row in table[1:]:  # Skip header
                            if row and len(row) >= 3:
                                # Common patterns: Date, Description, Amount
                                try:
                                    date_str = str(row[0]).strip() if row[0] else ""
                                    desc = str(row[1]).strip() if len(row) > 1 and row[1] else ""
                                    amount_str = str(row[-1]).strip() if row[-1] else ""
                                    
                                    # Parse amount
                                    amount = None
                                    is_credit = None
                                    
                                    if amount_str:
                                        # Remove currency symbols and commas
                                        amount_clean = re.sub(r'[^\d.-]', '', amount_str)
                                        try:
                                            amount = float(amount_clean)
                                            is_credit = amount >= 0
                                        except ValueError:
                                            continue
                                    
                                    if date_str and amount is not None:
                                        transactions.append({
                                            'Date': date_str,
                                            'Description': desc,
                                            'Amount': abs(amount),
                                            'Type': 'Credit' if is_credit else 'Debit'
                                        })
                                except Exception as e:
                                    continue
                
                # Fallback: Extract from text using regex patterns
                if not transactions:
                    # Pattern for date, description, amount
                    pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(.+?)\s+([-]?\$?\d+\.?\d*)'
                    matches = re.findall(pattern, text)
                    
                    for match in matches:
                        try:
                            date_str = match[0]
                            desc = match[1].strip()
                            amount_str = match[2].replace('$', '').replace(',', '')
                            amount = float(amount_str)
                            
                            transactions.append({
                                'Date': date_str,
                                'Description': desc,
                                'Amount': abs(amount),
                                'Type': 'Credit' if amount >= 0 else 'Debit'
                            })
                        except Exception:
                            continue
    
    except Exception as e:
        raise Exception(f"Error extracting PDF: {str(e)}")
    
    if not transactions:
        raise ValueError("No transactions found in PDF file")
    
    return pd.DataFrame(transactions)


def extract_from_csv(file_path: str) -> pd.DataFrame:
    """
    Extract transaction data from CSV file
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        DataFrame with columns: Date, Description, Amount, Type
    """
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise ValueError("Could not read CSV file with any encoding")
        
        # Normalize column names (case-insensitive)
        df.columns = df.columns.str.strip().str.lower()
        
        # Map common column names
        column_mapping = {
            'date': 'Date',
            'transaction date': 'Date',
            'txn date': 'Date',
            'description': 'Description',
            'details': 'Description',
            'narration': 'Description',
            'amount': 'Amount',
            'credit': 'Amount',
            'debit': 'Amount',
            'type': 'Type',
            'transaction type': 'Type'
        }
        
        # Find and rename columns
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df.rename(columns={old_name: new_name}, inplace=True)
        
        # Ensure required columns exist
        required_cols = ['Date', 'Description', 'Amount']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Handle Type column (Credit/Debit)
        if 'Type' not in df.columns:
            # Infer from Amount
            df['Type'] = df['Amount'].apply(lambda x: 'Credit' if pd.notna(x) and float(x) >= 0 else 'Debit')
        
        # Clean data
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df = df.dropna(subset=['Date', 'Amount'])
        df['Amount'] = df['Amount'].abs()
        
        return df[['Date', 'Description', 'Amount', 'Type']]
    
    except Exception as e:
        raise Exception(f"Error extracting CSV: {str(e)}")


def extract_from_excel(file_path: str) -> pd.DataFrame:
    """
    Extract transaction data from Excel file
    
    Args:
        file_path: Path to Excel file
        
    Returns:
        DataFrame with columns: Date, Description, Amount, Type
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Normalize column names (case-insensitive)
        df.columns = df.columns.str.strip().str.lower()
        
        # Map common column names
        column_mapping = {
            'date': 'Date',
            'transaction date': 'Date',
            'txn date': 'Date',
            'description': 'Description',
            'details': 'Description',
            'narration': 'Description',
            'amount': 'Amount',
            'credit': 'Amount',
            'debit': 'Amount',
            'type': 'Type',
            'transaction type': 'Type'
        }
        
        # Find and rename columns
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df.rename(columns={old_name: new_name}, inplace=True)
        
        # Handle separate Credit/Debit columns
        if 'credit' in df.columns and 'debit' in df.columns:
            df['Amount'] = df['credit'].fillna(0) - df['debit'].fillna(0)
            df['Type'] = df['Amount'].apply(lambda x: 'Credit' if x >= 0 else 'Debit')
            df['Amount'] = df['Amount'].abs()
        
        # Ensure required columns exist
        required_cols = ['Date', 'Description', 'Amount']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Handle Type column
        if 'Type' not in df.columns:
            df['Type'] = df['Amount'].apply(lambda x: 'Credit' if pd.notna(x) and float(x) >= 0 else 'Debit')
        
        # Clean data
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df = df.dropna(subset=['Date', 'Amount'])
        df['Amount'] = df['Amount'].abs()
        
        return df[['Date', 'Description', 'Amount', 'Type']]
    
    except Exception as e:
        raise Exception(f"Error extracting Excel: {str(e)}")


def extract(file_path: str) -> pd.DataFrame:
    """
    Main extraction function that routes to appropriate extractor based on file type
    
    Args:
        file_path: Path to uploaded file
        
    Returns:
        DataFrame with transaction data
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.pdf':
        return extract_from_pdf(file_path)
    elif file_ext == '.csv':
        return extract_from_csv(file_path)
    elif file_ext in ['.xlsx', '.xls']:
        return extract_from_excel(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")

