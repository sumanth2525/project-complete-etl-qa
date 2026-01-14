"""
Test SQL Server Connection
This script tests the database connection and helps diagnose connection issues
"""
import pyodbc
from config import SQL_SERVER_INSTANCE, DATABASE_NAME, SQL_SERVER_USER, SQL_SERVER_PASSWORD, ODBC_DRIVER
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def test_odbc_drivers():
    """List available ODBC drivers"""
    print("=" * 60)
    print("Available ODBC Drivers:")
    print("=" * 60)
    try:
        drivers = pyodbc.drivers()
        sql_drivers = [d for d in drivers if 'SQL Server' in d]
        if sql_drivers:
            for driver in sql_drivers:
                print(f"  [OK] {driver}")
        else:
            print("  [ERROR] No SQL Server drivers found!")
        print()
        return sql_drivers
    except Exception as e:
        print(f"  [ERROR] Error listing drivers: {e}")
        return []

def test_basic_connection():
    """Test basic connection to SQL Server instance"""
    print("=" * 60)
    print("Testing Basic Connection:")
    print("=" * 60)
    print(f"Server Instance: {SQL_SERVER_INSTANCE}")
    print(f"ODBC Driver: {ODBC_DRIVER}")
    print(f"Authentication: {'Windows Authentication' if not SQL_SERVER_USER else 'SQL Authentication'}")
    print()
    
    # Try different connection string formats
    connection_strings = []
    
    # Format 1: Windows Authentication with Trusted_Connection
    if not SQL_SERVER_USER:
        conn_str1 = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={SQL_SERVER_INSTANCE};"
            f"Trusted_Connection=yes;"
        )
        connection_strings.append(("Windows Auth (Trusted_Connection)", conn_str1))
        
        # Format 2: Windows Authentication without database
        conn_str2 = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={SQL_SERVER_INSTANCE};"
            f"Trusted_Connection=yes;"
            f"Database=master;"
        )
        connection_strings.append(("Windows Auth (master DB)", conn_str2))
    
    # Format 3: Try with different server name formats
    # Sometimes need to use comma instead of backslash
    server_alt = SQL_SERVER_INSTANCE.replace('\\', ',')
    if server_alt != SQL_SERVER_INSTANCE:
        conn_str3 = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={server_alt};"
            f"Trusted_Connection=yes;"
            f"Database=master;"
        )
        connection_strings.append(("Windows Auth (comma format)", conn_str3))
    
    # Try each connection string
    for name, conn_str in connection_strings:
        print(f"Trying: {name}")
        print(f"Connection String: {conn_str[:80]}...")
        try:
            conn = pyodbc.connect(conn_str, timeout=5)
            print(f"  [SUCCESS] Connected to SQL Server!")
            
            # Try a simple query
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"  [OK] SQL Server Version: {version[:50]}...")
            
            # Check if instance is correct
            cursor.execute("SELECT @@SERVERNAME")
            server_name = cursor.fetchone()[0]
            print(f"  [OK] Connected to: {server_name}")
            
            # List databases
            cursor.execute("SELECT name FROM sys.databases")
            databases = [row[0] for row in cursor.fetchall()]
            print(f"  [OK] Available databases: {', '.join(databases[:5])}...")
            
            conn.close()
            print()
            return True, conn_str
            
        except pyodbc.Error as e:
            print(f"  [FAILED] {e}")
            print()
        except Exception as e:
            print(f"  [ERROR] {e}")
            print()
    
    return False, None

def test_sql_server_service():
    """Check if SQL Server service is running"""
    print("=" * 60)
    print("SQL Server Service Status:")
    print("=" * 60)
    try:
        import subprocess
        # Check SQL Server service status
        result = subprocess.run(
            ['sc', 'query', 'MSSQL$SQLEXPRESS'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if 'RUNNING' in result.stdout:
            print("  [OK] SQL Server Express service is RUNNING")
        else:
            print("  [WARNING] SQL Server Express service status:")
            print(f"    {result.stdout}")
    except Exception as e:
        print(f"  [WARNING] Could not check service status: {e}")
        print("  Please check manually in Services (services.msc)")
    print()

def test_network_connectivity():
    """Test network connectivity to SQL Server"""
    print("=" * 60)
    print("Network Connectivity Test:")
    print("=" * 60)
    try:
        import socket
        # Extract server name (before backslash)
        server_name = SQL_SERVER_INSTANCE.split('\\')[0]
        print(f"Testing connection to: {server_name}")
        
        # Try to resolve hostname
        try:
            ip = socket.gethostbyname(server_name)
            print(f"  [OK] Hostname resolved to: {ip}")
        except:
            print(f"  [WARNING] Could not resolve hostname: {server_name}")
            print(f"  Try using IP address or 'localhost' if on same machine")
        
        # Try TCP connection on SQL Server default port (1433)
        # Note: Named instances use dynamic ports
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((server_name, 1433))
            sock.close()
            if result == 0:
                print(f"  [OK] Port 1433 is accessible")
            else:
                print(f"  [WARNING] Port 1433 is not accessible (may use dynamic port)")
        except Exception as e:
            print(f"  [WARNING] Could not test port 1433: {e}")
            
    except Exception as e:
        print(f"  [ERROR] {e}")
    print()

def main():
    """Run all connection tests"""
    print("\n" + "=" * 60)
    print("SQL Server Connection Diagnostic Tool")
    print("=" * 60)
    print()
    
    # Test 1: Check ODBC drivers
    drivers = test_odbc_drivers()
    if not drivers:
        print("ERROR: No SQL Server ODBC drivers found!")
        print("Please install ODBC Driver 17 for SQL Server")
        print("Download from: https://aka.ms/downloadmsodbcsql")
        return False
    
    # Test 2: Check SQL Server service
    test_sql_server_service()
    
    # Test 3: Network connectivity
    test_network_connectivity()
    
    # Test 4: Try connection
    success, conn_str = test_basic_connection()
    
    if success:
        print("=" * 60)
        print("[SUCCESS] CONNECTION SUCCESSFUL!")
        print("=" * 60)
        print("\nWorking connection string:")
        print(conn_str)
        print("\nYou can update config.py with this connection string format.")
        return True
    else:
        print("=" * 60)
        print("[FAILED] CONNECTION FAILED")
        print("=" * 60)
        print("\nTroubleshooting steps:")
        print("1. Verify SQL Server is running:")
        print("   - Open Services (services.msc)")
        print("   - Look for 'SQL Server (SQLEXPRESS)'")
        print("   - Ensure it's running")
        print()
        print("2. Check SQL Server Configuration Manager:")
        print("   - Enable TCP/IP protocol")
        print("   - Enable Named Pipes")
        print("   - Restart SQL Server service")
        print()
        print("3. Verify instance name:")
        print(f"   - Current: {SQL_SERVER_INSTANCE}")
        print("   - Try: localhost\\SQLEXPRESS")
        print("   - Try: .\\SQLEXPRESS")
        print("   - Try: (local)\\SQLEXPRESS")
        print()
        print("4. Check Windows Firewall:")
        print("   - Allow SQL Server through firewall")
        print("   - Allow port 1433 (or dynamic port)")
        print()
        print("5. Test with SQL Server Management Studio (SSMS):")
        print(f"   - Try connecting to: {SQL_SERVER_INSTANCE}")
        print("   - If SSMS works, the issue is with the connection string")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

