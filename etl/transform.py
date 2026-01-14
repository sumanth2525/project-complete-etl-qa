"""
Transform module for ETL pipeline
Standardizes and cleans extracted data
"""
import pandas as pd
from datetime import datetime
from typing import Optional
import re
import logging

logger = logging.getLogger(__name__)


def extract_merchant_name(description: str) -> str:
    """
    Extract merchant name from transaction description
    
    Args:
        description: Transaction description string
        
    Returns:
        Extracted merchant name
    """
    if pd.isna(description) or not description:
        return ""
    
    desc = str(description).strip()
    
    # Common patterns to extract merchant name
    # Remove common prefixes/suffixes
    patterns_to_remove = [
        r'^PAYMENT\s+',
        r'^TXN\s+',
        r'^TRANSFER\s+',
        r'\s+REF\s+.*$',
        r'\s+ID\s+.*$',
        r'\s+\d{4,}.*$',  # Remove trailing long numbers
    ]
    
    for pattern in patterns_to_remove:
        desc = re.sub(pattern, '', desc, flags=re.IGNORECASE)
    
    # Extract first meaningful word/phrase (usually merchant name)
    # Split by common separators
    separators = [' - ', ' / ', ' AT ', ' FROM ', ' TO ']
    for sep in separators:
        if sep.lower() in desc.lower():
            parts = desc.split(sep, 1)
            desc = parts[0].strip()
            break
    
    # Take first 2-3 words as merchant name
    words = desc.split()
    if len(words) > 3:
        desc = ' '.join(words[:3])
    
    return desc.strip()[:100]  # Limit to 100 characters


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Parse date string into datetime object
    Handles multiple date formats
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        Datetime object or None if parsing fails
    """
    if pd.isna(date_str) or not date_str:
        return None
    
    date_str = str(date_str).strip()
    
    # Common date formats
    date_formats = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%Y/%m/%d',
        '%d-%m-%Y',
        '%m-%d-%Y',
        '%d.%m.%Y',
        '%Y.%m.%d',
        '%d/%m/%y',
        '%m/%d/%y',
        '%d-%m-%y',
        '%m-%d-%y',
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # Try pandas parsing as fallback
    try:
        return pd.to_datetime(date_str)
    except:
        return None


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform extracted data into standard format
    
    Args:
        df: DataFrame with columns: Date, Description, Amount, Type
        
    Returns:
        Transformed DataFrame with columns:
        - TxnDateTime (DATETIME)
        - Amount (DECIMAL)
        - Description (string)
        - MerchantName (string)
        - IsCredit (bool)
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty")
    
    # Create a copy to avoid modifying original
    transformed_df = df.copy()
    
    # Parse dates
    transformed_df['TxnDateTime'] = transformed_df['Date'].apply(parse_date)
    
    # Drop rows with invalid dates
    transformed_df = transformed_df.dropna(subset=['TxnDateTime'])
    
    # Ensure Amount is numeric
    transformed_df['Amount'] = pd.to_numeric(transformed_df['Amount'], errors='coerce')
    transformed_df = transformed_df.dropna(subset=['Amount'])
    
    # Ensure Amount is positive
    transformed_df['Amount'] = transformed_df['Amount'].abs()
    
    # Filter out unrealistic amounts (likely data extraction errors)
    # Typical bank transactions are between $0.01 and $10,000,000
    # Values larger than this are likely account numbers, reference numbers, etc.
    MAX_REALISTIC_AMOUNT = 10_000_000.00  # $10 million
    MIN_REALISTIC_AMOUNT = 0.01  # $0.01
    
    before_count = len(transformed_df)
    transformed_df = transformed_df[
        (transformed_df['Amount'] >= MIN_REALISTIC_AMOUNT) & 
        (transformed_df['Amount'] <= MAX_REALISTIC_AMOUNT)
    ]
    after_count = len(transformed_df)
    
    if before_count > after_count:
        logger.warning(f"Filtered out {before_count - after_count} transactions with unrealistic amounts (outside ${MIN_REALISTIC_AMOUNT:,.2f} - ${MAX_REALISTIC_AMOUNT:,.2f})")
    
    # Convert Type to IsCredit (BIT)
    if 'Type' in transformed_df.columns:
        transformed_df['IsCredit'] = transformed_df['Type'].apply(
            lambda x: 1 if str(x).strip().lower() in ['credit', 'cr', 'deposit', 'incoming'] else 0
        )
    else:
        # Default to Debit if Type not available
        transformed_df['IsCredit'] = 0
    
    # Clean Description
    transformed_df['Description'] = transformed_df['Description'].fillna('').astype(str)
    transformed_df['Description'] = transformed_df['Description'].str.strip()
    transformed_df['Description'] = transformed_df['Description'].str[:255]  # Limit to 255 chars
    
    # Extract MerchantName from Description
    transformed_df['MerchantName'] = transformed_df['Description'].apply(extract_merchant_name)
    transformed_df['MerchantName'] = transformed_df['MerchantName'].str[:100]  # Limit to 100 chars
    
    # Select and order final columns
    final_df = transformed_df[[
        'TxnDateTime',
        'Amount',
        'Description',
        'MerchantName',
        'IsCredit'
    ]].copy()
    
    # Ensure data types
    final_df['TxnDateTime'] = pd.to_datetime(final_df['TxnDateTime'])
    final_df['Amount'] = final_df['Amount'].astype(float)
    final_df['Description'] = final_df['Description'].astype(str)
    final_df['MerchantName'] = final_df['MerchantName'].astype(str)
    final_df['IsCredit'] = final_df['IsCredit'].astype(int)
    
    # Remove duplicates if any
    final_df = final_df.drop_duplicates(subset=['TxnDateTime', 'Amount', 'Description'])
    
    return final_df.reset_index(drop=True)

