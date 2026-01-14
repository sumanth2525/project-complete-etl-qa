"""
Configuration file for ETL project
Contains database connection settings
"""
import os
from urllib.parse import quote_plus

# SQL Server connection settings
SQL_SERVER_INSTANCE = "SUMANTH\\SQLEXPRESS"
DATABASE_NAME = "BankStatementDB"
# For Windows Authentication, set both to empty string
# For SQL Authentication, provide username and password
SQL_SERVER_USER = ""  # Leave empty for Windows Authentication (uses current Windows user)
SQL_SERVER_PASSWORD = ""  # Leave empty for Windows Authentication

# ODBC Driver selection - try common drivers in order of preference
def get_odbc_driver():
    """Detect available ODBC driver for SQL Server"""
    try:
        import pyodbc
        drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
        # Prefer newer drivers
        preferred = [
            'ODBC Driver 17 for SQL Server',
            'ODBC Driver 18 for SQL Server',
            'ODBC Driver 13 for SQL Server',
            'SQL Server Native Client 11.0',
            'SQL Server'
        ]
        for pref in preferred:
            if pref in drivers:
                return pref
        # Return first available if no preferred found
        return drivers[0] if drivers else 'ODBC Driver 17 for SQL Server'
    except:
        # Default fallback
        return 'ODBC Driver 17 for SQL Server'

ODBC_DRIVER = get_odbc_driver()

# Construct connection string for pyodbc (better Windows Auth support)
# Format: mssql+pyodbc://username:password@server/instance/database?driver=ODBC+Driver+17+for+SQL+Server
# For Windows Authentication, use Trusted_Connection=yes
# Note: For named instances (server\instance), URL encode the backslash as %5C

# Build connection string for pyodbc
# For SQLAlchemy with pyodbc, we need to use a connection string format
# that properly handles named instances

def build_connection_string():
    """Build pyodbc connection string"""
    driver_str = ODBC_DRIVER.replace(' ', '+')
    
    if not SQL_SERVER_USER:
        # Windows Authentication
        # Format: DRIVER={...};SERVER=server\instance;DATABASE=db;Trusted_Connection=yes;
        conn_str = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={SQL_SERVER_INSTANCE};"
            f"DATABASE={DATABASE_NAME};"
            f"Trusted_Connection=yes;"
        )
    elif SQL_SERVER_PASSWORD:
        # SQL Authentication
        conn_str = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={SQL_SERVER_INSTANCE};"
            f"DATABASE={DATABASE_NAME};"
            f"UID={SQL_SERVER_USER};"
            f"PWD={SQL_SERVER_PASSWORD};"
        )
    else:
        # SQL Auth without password
        conn_str = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={SQL_SERVER_INSTANCE};"
            f"DATABASE={DATABASE_NAME};"
            f"UID={SQL_SERVER_USER};"
        )
    
    # For SQLAlchemy, encode the connection string
    from urllib.parse import quote_plus
    encoded_conn_str = quote_plus(conn_str)
    return f"mssql+pyodbc:///?odbc_connect={encoded_conn_str}"

DATABASE_URL = build_connection_string()

# Flask settings
UPLOAD_FOLDER = "uploads"
MAX_UPLOAD_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'pdf', 'csv', 'xlsx', 'xls'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

