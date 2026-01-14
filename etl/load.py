"""
Load module for ETL pipeline
Handles database operations and data loading
"""
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from config import DATABASE_URL, DATABASE_NAME, SQL_SERVER_INSTANCE
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_database_if_not_exists():
    """
    Create database if it doesn't exist
    Connects to master database first, then creates BankStatementDB
    """
    try:
        # Connect to master database to create new database
        master_url = DATABASE_URL.replace(f"/{DATABASE_NAME}", "/master")
        engine = create_engine(master_url, echo=False)
        
        with engine.connect() as conn:
            # Check if database exists
            check_db_query = text(f"SELECT name FROM sys.databases WHERE name = '{DATABASE_NAME}'")
            result = conn.execute(check_db_query)
            
            if not result.fetchone():
                # Create database
                create_db_query = text(f"CREATE DATABASE [{DATABASE_NAME}]")
                conn.execute(create_db_query)
                conn.commit()
                logger.info(f"Database '{DATABASE_NAME}' created successfully")
            else:
                logger.info(f"Database '{DATABASE_NAME}' already exists")
        
        engine.dispose()
    
    except Exception as e:
        logger.warning(f"Could not create database (may already exist): {str(e)}")


def create_table_if_not_exists(engine):
    """
    Create BankTransactions table if it doesn't exist
    Also alter existing table if Amount column is too small
    
    Args:
        engine: SQLAlchemy engine connected to BankStatementDB
    """
    try:
        with engine.connect() as conn:
            # Check if table exists
            inspector = inspect(engine)
            if 'BankTransactions' in inspector.get_table_names():
                logger.info("Table 'BankTransactions' already exists")
                
                # Check if Amount column needs to be altered
                try:
                    # Get column info
                    columns = inspector.get_columns('BankTransactions')
                    amount_col = next((col for col in columns if col['name'] == 'Amount'), None)
                    
                    if amount_col:
                        col_type = str(amount_col['type'])
                        # Check if it's DECIMAL(10,2) or smaller
                        if 'DECIMAL' in col_type.upper() and '10' in col_type:
                            logger.info("Altering Amount column to DECIMAL(18,2) to support larger values")
                            alter_sql = text("""
                                ALTER TABLE BankTransactions
                                ALTER COLUMN Amount DECIMAL(18,2)
                            """)
                            conn.execute(alter_sql)
                            conn.commit()
                            logger.info("Amount column updated successfully")
                except Exception as e:
                    logger.warning(f"Could not alter Amount column (may already be correct): {str(e)}")
                
                return
            
            # Create table
            # Amount: DECIMAL(18,2) supports up to 999,999,999,999,999,999.99
            # This is sufficient for any realistic bank transaction
            create_table_sql = text("""
                CREATE TABLE BankTransactions (
                    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
                    TxnDateTime DATETIME,
                    Amount DECIMAL(18,2),
                    Description NVARCHAR(255),
                    MerchantName NVARCHAR(100),
                    IsCredit BIT
                )
            """)
            
            conn.execute(create_table_sql)
            conn.commit()
            logger.info("Table 'BankTransactions' created successfully")
    
    except Exception as e:
        logger.error(f"Error creating table: {str(e)}")
        raise


def load_data(df: pd.DataFrame) -> int:
    """
    Load transformed data into SQL Server
    
    Args:
        df: Transformed DataFrame with standard columns
        
    Returns:
        Number of records inserted
    """
    if df.empty:
        raise ValueError("DataFrame is empty, nothing to load")
    
    try:
        # Ensure database exists
        create_database_if_not_exists()
        
        # Create engine for the target database
        engine = create_engine(DATABASE_URL, echo=False)
        
        # Create table if not exists
        create_table_if_not_exists(engine)
        
        # Load data using pandas to_sql
        # Use if_exists='append' to add new records
        rows_inserted = df.to_sql(
            name='BankTransactions',
            con=engine,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=1000
        )
        
        logger.info(f"Successfully inserted {rows_inserted} records into BankTransactions")
        
        engine.dispose()
        
        return rows_inserted
    
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error during load: {str(e)}")
        raise Exception(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise Exception(f"Load error: {str(e)}")


def get_record_count() -> int:
    """
    Get total number of records in BankTransactions table
    
    Returns:
        Total record count
    """
    try:
        engine = create_engine(DATABASE_URL, echo=False)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) as cnt FROM BankTransactions"))
            count = result.fetchone()[0]
        
        engine.dispose()
        return count
    
    except Exception as e:
        logger.warning(f"Could not get record count: {str(e)}")
        return 0

