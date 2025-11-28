"""
Database connection manager for MySQL/XAMPP
"""

import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    """Manages MySQL database connections"""
    
    def __init__(self, host="localhost", port=3306, user="root", password="", database=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    
    def connect(self):
        """Establish connection to MySQL server"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                print(f"✓ Successfully connected to MySQL server")
                db_info = self.connection.get_server_info()
                print(f"MySQL Server version: {db_info}")
                return True
                
        except Error as e:
            print(f"✗ Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ MySQL connection closed")
    
    def test_connection(self):
        """Test if connection is working"""
        try:
            if self.connect():
                cursor = self.connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                cursor.close()
                self.disconnect()
                return True, f"Connected! MySQL version: {version[0]}"
            else:
                return False, "Failed to connect to MySQL"
        except Error as e:
            return False, f"Connection error: {str(e)}"
    
    def get_databases(self):
        """Get list of all databases"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            cursor.close()
            
            # Filter out system databases
            system_dbs = ['information_schema', 'mysql', 'performance_schema', 'sys', 'phpmyadmin', 'test']
            user_databases = [db for db in databases if db not in system_dbs]
            
            return user_databases
            
        except Error as e:
            print(f"Error getting databases: {e}")
            return []
    
    def get_database_info(self, db_name):
        """Get information about a specific database"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            
            # Get table count
            cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{db_name}'")
            table_count = cursor.fetchone()[0]
            
            # Get database size
            cursor.execute(f"""
                SELECT 
                    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
                FROM information_schema.tables 
                WHERE table_schema = '{db_name}'
            """)
            size = cursor.fetchone()[0]
            size_str = f"{size}MB" if size else "0MB"
            
            cursor.close()
            
            return {
                "name": db_name,
                "tables": table_count,
                "size": size_str,
                "type": "MySQL",
                "status": "Active"
            }
            
        except Error as e:
            print(f"Error getting database info: {e}")
            return None
    
    def execute_query(self, query):
        """Execute a custom SQL query"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            # For SELECT queries
            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                cursor.close()
                return results
            
            # For INSERT, UPDATE, DELETE
            self.connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            print(f"Error executing query: {e}")
            return None
